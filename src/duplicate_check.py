

import mysql.connector
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()


# Step 1: Generate SHA-256 hash
def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for data in iter(lambda: file.read(4096), b""):
            sha256.update(data)

    return sha256.hexdigest()


# Step 2: Check whether the file is a duplicate
def check_duplicate(file_path):

    if not os.path.isfile(file_path):
        print("File not found!")
        return

    file_hash = calculate_file_hash(file_path)
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    print("\nFile Name:", file_name)
    print("File Size:", file_size, "bytes")
    print("SHA-256 Hash:", file_hash)

    connection = None
    cursor = None

    try:
        # Step 3: Connect to MySQL
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )

        cursor = connection.cursor()

        # Step 4: Search for existing file hash
        query = """
        SELECT file_id
        FROM stored_files
        WHERE file_hash = %s
        """

        cursor.execute(query, (file_hash,))
        result = cursor.fetchone()

        # Step 5: Identify duplicate or new file
        if result:

            print("\nDUPLICATE FILE DETECTED!")
            print("This file already exists in DedupVault.")
            print("Existing File ID:", result[0])

        else:

            # Step 6: Store new file information
            insert_query = """
            INSERT INTO stored_files
            (file_hash, original_name, file_size, storage_path)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                insert_query,
                (file_hash, file_name, file_size, file_path)
            )

            connection.commit()

            print("\nNEW FILE DETECTED!")
            print("File information saved successfully.")
            print("New File ID:", cursor.lastrowid)

    except mysql.connector.Error as error:

        print("Database error:", error)

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# Step 7: Main program
if __name__ == "__main__":

    path = input("Enter file path: ").strip().strip('"').strip("'")

    check_duplicate(path)
