
import hashlib
import logging
import os
import tempfile
import uuid
from datetime import date, datetime
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024

STORAGE_DIR = Path(__file__).resolve().parent / "storage"
STAGING_DIR = STORAGE_DIR / ".staging"
logger = logging.getLogger(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", "3306")),
    )


def json_value(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def get_dashboard_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT COUNT(*) AS total_uploads
            FROM backup_records
            """
        )
        activity_totals = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS unique_files,
                   COALESCE(SUM(file_size), 0) AS stored_bytes
            FROM stored_files
            """
        )
        storage_totals = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS duplicate_uploads,
                   COALESCE(SUM(b.file_size), 0) AS bytes_prevented
            FROM backup_records AS b
            JOIN (
                SELECT file_hash, MIN(record_id) AS first_record_id
                FROM backup_records
                GROUP BY file_hash
            ) AS first_upload
            ON first_upload.file_hash = b.file_hash
            WHERE b.record_id > first_upload.first_record_id
            """
        )
        duplicate_totals = cursor.fetchone()

        cursor.execute(
            """
            SELECT s.file_id, s.original_name, s.file_size, s.file_hash,
                   s.created_at, COUNT(b.record_id) AS upload_count
            FROM stored_files AS s
            LEFT JOIN backup_records AS b
            ON b.file_hash = s.file_hash
            GROUP BY s.file_id, s.original_name, s.file_size,
                     s.file_hash, s.created_at
            ORDER BY s.created_at DESC
            LIMIT 200
            """
        )
        files = cursor.fetchall()

        cursor.execute(
            """
            SELECT b.record_id, b.uploaded_name, b.file_size, b.file_hash,
                   CASE
                       WHEN b.record_id > first_upload.first_record_id
                       THEN TRUE
                       ELSE FALSE
                   END AS duplicate
            FROM backup_records AS b
            JOIN (
                SELECT file_hash, MIN(record_id) AS first_record_id
                FROM backup_records
                GROUP BY file_hash
            ) AS first_upload
            ON first_upload.file_hash = b.file_hash
            ORDER BY b.record_id DESC
            LIMIT 20
            """
        )
        activity = cursor.fetchall()

        for item in files + activity:
            for key, value in item.items():
                item[key] = json_value(value)

        return {
            "stats": {
                "unique_files": int(storage_totals["unique_files"]),
                "stored_bytes": int(storage_totals["stored_bytes"]),
                "total_uploads": int(activity_totals["total_uploads"]),
                "duplicate_uploads": int(
                    duplicate_totals["duplicate_uploads"]
                ),
                "bytes_prevented": int(
                    duplicate_totals["bytes_prevented"]
                ),
            },
            "files": files,
            "activity": activity,
        }

    finally:
        cursor.close()
        connection.close()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/dashboard")
def dashboard():
    try:
        return jsonify(get_dashboard_data())

    except mysql.connector.Error:
        logger.exception("Could not load dashboard data from MySQL")

        return jsonify(
            error="Could not connect to the database. Check your .env settings and MySQL service."
        ), 503


@app.post("/api/upload")
def upload():

    uploaded_file = request.files.get("file")

    if uploaded_file is None or not uploaded_file.filename:
        return jsonify(error="Choose a file to upload."), 400

    filename = secure_filename(uploaded_file.filename)

    if not filename:
        return jsonify(error="The file name is not valid."), 400

    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    temporary_path = None
    stored_path = None
    committed = False
    connection = None
    cursor = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=STAGING_DIR,
            delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)

        uploaded_file.save(temporary_path)

        file_hash = hashlib.sha256()
        file_size = 0

        with temporary_path.open("rb") as file_stream:
            for chunk in iter(
                lambda: file_stream.read(1024 * 1024), b""
            ):
                file_size += len(chunk)
                file_hash.update(chunk)

        digest = file_hash.hexdigest()

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT file_id, original_name, file_size, storage_path
            FROM stored_files
            WHERE file_hash = %s
            """,
            (digest,),
        )

        existing_file = cursor.fetchone()

        if existing_file:

            storage_path = existing_file["storage_path"]

            cursor.execute(
                """
                INSERT INTO backup_records
                    (uploaded_name, file_hash, file_size)
                VALUES (%s, %s, %s)
                """,
                (filename, digest, file_size),
            )

            result = {
                "duplicate": True,
                "filename": filename,
                "file_size": file_size,
                "file_hash": digest,
                "file_id": existing_file["file_id"],
                "original_name": existing_file["original_name"],
            }

        else:

            stored_path = (
                STORAGE_DIR
                / digest[:2]
                / (
                    digest
                    + "_"
                    + uuid.uuid4().hex
                    + "_"
                    + filename
                )
            )

            stored_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            os.replace(temporary_path, stored_path)
            temporary_path = None

            cursor.execute(
                """
                INSERT INTO stored_files
                    (file_hash, original_name, file_size, storage_path)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    digest,
                    filename,
                    file_size,
                    str(stored_path),
                ),
            )

            file_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO backup_records
                    (uploaded_name, file_hash, file_size)
                VALUES (%s, %s, %s)
                """,
                (filename, digest, file_size),
            )

            result = {
                "duplicate": False,
                "filename": filename,
                "file_size": file_size,
                "file_hash": digest,
                "file_id": file_id,
                "original_name": filename,
            }

        result["record_id"] = cursor.lastrowid

        connection.commit()
        committed = True

        return jsonify(result), 201

    except mysql.connector.Error:

        if connection and connection.is_connected():
            connection.rollback()

        logger.exception(
            "Database error while processing uploaded file"
        )

        return jsonify(
            error="The upload could not be recorded. Check your database connection and schema."
        ), 503

    except OSError:

        if connection and connection.is_connected():
            connection.rollback()

        logger.exception(
            "File storage error while processing uploaded file"
        )

        return jsonify(
            error="The file could not be saved to local storage."
        ), 500

    except Exception:

        if connection and connection.is_connected():
            connection.rollback()

        logger.exception(
            "Unexpected error while processing uploaded file"
        )

        return jsonify(
            error="An unexpected error prevented the upload from completing."
        ), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

        if temporary_path and temporary_path.exists():
            temporary_path.unlink()

        if stored_path and stored_path.exists() and not committed:
            stored_path.unlink()


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(_error):
    return jsonify(
        error="Files must be 512 MB or smaller."
    ), 413


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
        debug=False
    )
