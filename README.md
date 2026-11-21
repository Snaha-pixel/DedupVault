🔐 DedupVault
Intelligent Duplicate File Detection & Storage Optimization System

DedupVault is a Python and MySQL-based project designed to identify duplicate files using SHA-256 hashing and maintain organized file and backup records.

When managing multiple files and backups, identical content may be saved under different filenames. This can create unnecessary duplicate records and make file management difficult.

DedupVault addresses this problem by comparing file contents rather than relying only on filenames. It uses SHA-256 hashing to identify files with identical content and stores metadata for unique files in a MySQL database.

DedupVault – Store Smarter. Detect Duplicates. Optimize Storage.

1. Problem Statement

Duplicate files are common when managing multiple backups and file collections. Files with identical content may have different names, making it difficult to identify duplicates through filenames alone.

This can result in unnecessary duplicate records and inefficient file management.

DedupVault aims to solve this problem by generating a unique SHA-256 hash for each file and comparing it with existing database records.

2. Project Objectives

- Identify duplicate files based on their actual content.
- Generate SHA-256 hashes using Python.
- Compare file hashes with existing MySQL records.
- Store metadata only for unique files.
- Maintain a history of file upload attempts.
- Improve file record organization and data integrity.
- Demonstrate the practical application of DBMS concepts using Python and MySQL.

 3. What Does DedupVault Do?

Whenever a user selects a file:

1. Python reads the file in binary mode.
2. A SHA-256 hash is generated from its contents.
3. The generated hash is compared with existing hashes in MySQL.
4. If a matching hash is found, the file is identified as a duplicate.
5. If no matching hash is found, its metadata is inserted into the `stored_files` table.
6. Every upload attempt is recorded in the `backup_records` table.

This allows the system to distinguish between unique files and duplicate upload attempts.

4. Features

- SHA-256 File Hashing: Generates file hashes using Python's `hashlib` library.
- Duplicate File Detection: Identifies identical file contents even when filenames differ.
- Web Dashboard: Upload files, search the unique-file inventory, and review duplicate upload history.
- Local File Storage: Keeps the first uploaded copy in the server's `storage/` directory; matching uploads are recorded without storing another copy.
- MySQL Integration: Connects Python with MySQL to store and retrieve file records.
- Unique File Management: Uses a unique constraint on file hashes to prevent duplicate metadata records.
- Backup History Tracking: Records every upload attempt, including duplicate files.
- File Metadata Management: Stores filenames, file sizes, hashes, and file paths.
- Modular Code Structure: Separates file hashing and duplicate detection logic into different Python modules.
- Menu-Driven Application: Provides options to upload files or exit the application.

5. Technologies Used

Here is your technology table in clean Markdown format. Copy and paste it directly into your `README.md` file.

| Technology             | Purpose                                |
| ---------------------- | -------------------------------------- |
| Python                 | Main programming language              |
| MySQL                  | Database management                    |
| SQL                    | Database creation and queries          |
| SHA-256                | File content identification            |
| hashlib                | Hash generation                        |
| mysql-connector-python | Python–MySQL connectivity              |
| python-dotenv          | Environment variable management        |
| Git & GitHub           | Version control and project management |
| VS Code                | Development environment                |
| MySQL Workbench        | Database design and management         |

6. System Architecture

DedupVault follows a simple Python–MySQL architecture.

 System Workflow

```text
        USER
          |
          v
     app.py
  (Main Application)
          |
          v
   Select File Path
          |
          v
   File Hashing Module
     (SHA-256)
          |
          v
   Duplicate Check Module
          |
          v
    MySQL Database
          |
     +----+----+
     |         |
     v         v
  Duplicate   New File
  Detected    Detected
     |         |
     v         v
  Existing   Insert File
  File ID    Metadata
     |         |
     +----+----+
          |
          v
   Record Upload Attempt
    (backup_records)
          |
          v
     Display Result
```
7. Database Design

Database Name:backup_optimizer

The database contains two main tables.

 7.1 stored_files

This table stores metadata for unique files.

Column	Description
file_id	Unique ID for each file
file_hash	SHA-256 hash of the file
original_name	Original filename
file_size	File size in bytes
storage_path	Location of the original file
created_at	Date and time the record was created

Important: The `file_hash` column has a UNIQUE constraint to prevent duplicate file metadata records.

 7.2 backup_records

This table maintains the history of file upload attempts.

Column	Description
record_id	Unique backup record ID
uploaded_name	Name of the uploaded file
file_hash	SHA-256 hash of the file
file_size	File size in bytes

Every upload attempt is recorded, whether the file is new or a duplicate.

8. Project Structure

text
DedupVault/
│
├── database/
│   └── database.sql
│
├── src/
│   ├── file_hash.py
│   └── duplicate_check.py
│
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── styles.css
├── app.py
├── web_app.py
├── test_connection.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

Note:The `.env` file contains local database credentials. It should remain private and must not be uploaded to GitHub.

9. Getting Started

Follow these steps to run DedupVault on your local system.

Prerequisites

- Python installed
- MySQL Server installed
- MySQL Workbench (recommended)
- Git installed

Step 1: Clone the Repository

bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd DedupVault

Step 2: Create a Virtual Environment

bash
python -m venv venv

Activate it on Windows:

bash
venv\Scripts\activate

Step 3: Install Required Packages

bash
pip install -r requirements.txt

Step 4: Configure Database Credentials

Step 5: Set Up the Database

Open MySQL Workbench and execute the SQL script available at:

`database/database.sql`

This creates the database and its required tables.

Step 6: Test the Database Connection

python test_connection.py

Step 7: Run the web dashboard

```bash
python web_app.py
```

Open `http://127.0.0.1:5000` in your browser. The dashboard reads its file inventory and upload history from MySQL. The first upload of a file is stored in the local `storage/` directory; an upload with matching SHA-256 content is recorded as a duplicate and is not stored again. Uploads are limited to 512 MB per file.

To use the original command-line interface instead:

```bash
python app.py
```

The command-line application displays a menu:

text
=============================================
                 DEDUPVAULT
       Duplicate Backup Detection System
=============================================

1. Upload a file
2. Exit


Select option 1 and enter the file path when prompted.

10. Testing and Results

The application is tested using different file upload scenarios.

Test Case 1: New File Detection

Input: A file that does not already exist in the database.

Expected Result:
- SHA-256 hash is generated.
- The database is checked for an existing hash.
- New file metadata is inserted into `stored_files`.
- An upload attempt is recorded in `backup_records`.
- The application displays `NEW FILE DETECTED!`.

 Test Case 2: Duplicate File Detection

Input: The same file is uploaded again.

Expected Result:
- The generated hash matches an existing hash.
- The application displays `DUPLICATE FILE DETECTED!`.
- No additional unique file metadata record is inserted.
- A new upload attempt is recorded in `backup_records`.

 Test Case 3: File Not Found

Input: An invalid or unavailable file path.

Expected Result:
- The application displays `File not found!`.
- No database upload record is created.

 Database Verification

The following SQL queries can be used to verify the results:

sql

USE backup_optimizer;

SELECT * FROM stored_files;

SELECT * FROM backup_records;

Testing Summary:

The new-file and duplicate-file detection workflows have been tested. Database records can be inspected using MySQL Workbench.

11. Project Development Status

Here is your properly spaced Markdown table. Copy and paste it directly into your `README.md`.

| Feature                              | Status             |
| ------------------------------------ | ------------------ |
| MySQL database creation              | Completed          |
| Database table design                | Completed          |
| Python environment configuration     | Completed          |
| Python–MySQL connectivity            | Completed          |
| SHA-256 hash generation              | Completed          |
| Duplicate detection logic            | Completed          |
| Unique file metadata insertion       | Completed          |
| Backup history integration           | Completed          |
| Menu-driven application              | Completed          |
| Basic new-file and duplicate testing | Completed          |
| Physical file storage management      | Completed          |
| Duplicate bytes prevented calculation | Completed          |
| Web-based user interface              | Completed          |
| File restoration and recovery        | Future Enhancement |

12. Future Enhancements

Future improvements may include:

- Adding automated backup management.
- Implementing file restoration and recovery.
- Providing detailed storage analytics and reports.

13. Learning Outcomes

Through this project, I have gained practical experience in:

- Database design and management.
- SQL queries and database constraints.
- Python programming and file handling.
- Python–MySQL integration.
- SHA-256 hashing and data integrity.
- Duplicate detection techniques.
- Modular programming.
- Git and GitHub version control.

14. About the Developer

Snaha Chaudhuri

BCA – Data Science

Interested in Python, SQL, Data Science, Database Management, and Software Development.

- GitHub: [Snaha-pixel](https://github.com/Snaha-pixel)
- LinkedIn: [Snaha Chaudhuri](https://www.linkedin.com/in/sn aha-chaudhuri-89634832a/)

---

⭐ If you find this project interesting, feel free to explore the repository!

DedupVault – Store Smarter. Detect Duplicates. Optimize Storage.
