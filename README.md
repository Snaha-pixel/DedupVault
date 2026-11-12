🔐 DedupVault
Intelligent Duplicate File Detection & Storage Optimization System

DedupVault is a Python and MySQL-based project that helps identify duplicate files and manage storage more efficiently.

While working with files and backups, duplicate copies can take up unnecessary storage space. DedupVault aims to solve this problem by checking the actual content of files using **SHA-256 hashing**, instead of depending only on their filenames.

This means that even if two files have different names, the system can recognize them as duplicates if their contents are identical.

The main idea behind this project is simple: avoid storing the same file multiple times and make file management more efficient.

. What Does DedupVault Do?

DedupVault checks whether a file already exists in the database before adding its information as a new record.

Whenever a file is selected:
- Python reads the file and generates its SHA-256 hash.
- The generated hash is compared with the hashes already stored in MySQL.
- If a matching hash is found, the file is identified as a duplicate.
- If no match is found, the file information is saved in the database.

This approach helps maintain organized file records and reduces unnecessary duplicate entries.

. Features:

- File Hashing: Uses Python's `hashlib` library to generate SHA-256 hashes.
- Duplicate Detection: Finds identical files even if they have different filenames.
- MySQL Integration: Stores file information and retrieves existing records.
- Data Integrity:Uses unique hash constraints to prevent duplicate entries.
- File Metadata Management: Keeps track of filenames, file sizes, hashes, and storage locations.
- Modular Code: Keeps hashing and duplicate detection logic in separate Python files for easier maintenance.

. Technologies Used:
| Technology             | Purpose                                |
| ---------------------- | -------------------------------------- |
| Python                 | Main programming language              |
| MySQL                  | Database management                    |
| SQL                    | Creating and managing database records |
| SHA-256                | Identifying duplicate file contents    |
| mysql-connector-python | Connecting Python with MySQL           |
| python-dotenv          | Managing database configuration        |
| Git & GitHub           | Version control and project management |


⚙️How Does It Work?

Here is the basic workflow of DedupVault:

1. The user selects or enters the path of a file.
2. Python reads the file in binary mode.
3. A SHA-256 hash is generated based on the file's contents.
4. The system checks whether that hash already exists in the MySQL database.
5. If the hash is already present, the system recognizes the file as a duplicate.
6. Otherwise, the file's metadata is inserted into the database.
7. The stored information can then be used for future duplicate checks.

🏗️Project Structure

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
├── app.py
├── test_connection.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

 Database Design:

Database Name: backup_optimizer

The database is designed to maintain information about stored files and backup records.

 1. stored_files

This table stores details about unique files.

| Column          | Description                          |
| --------------- | ------------------------------------ |
| file_id       | Unique ID for each file              |
| file_hash     | SHA-256 hash of the file             |
| original_name | Original filename                    |
| file_size     | File size in bytes                   |
| storage_path  | Location of the stored file          |
| created_at   | Date and time the record was created |

2. backup_records

This table maintains information about backup-related file records.
| Column          | Description               |
| --------------- | ------------------------- |
| record_id  | Unique backup record ID   |
| uploaded_name | Name of the uploaded file |
| file_hash     | SHA-256 hash of the file  |
| file_size  | File size in bytes        |

 💻Getting Started

Follow these steps to set up DedupVault on your local system.

1. Clone the repository

bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd DedupVault


2. Create a virtual environment

bash
python -m venv venv


Activate it on Windows:

bash
venv\Scripts\activate


3. Install the required packages

bash
pip install -r requirements.txt


4. Configure database credentials

Create a .env file in the root directory and add your MySQL details:

ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=backup_optimizer
DB_PORT=3306

 5. Set up the database

Create the `backup_optimizer` database and execute the SQL script available inside the `database` folder.

 6. Check the database connection

bash
python test_connection.py

 7. Generate a file hash
bash
python src/file_hash.py

 8. Run duplicate detection

bash
python src/duplicate_check.py


Enter the file path when prompted to check whether the file already exists in the database.

📌Project Development Status

DedupVault is being developed step by step. The following areas are part of the project roadmap:

- [x] MySQL database creation and table design
- [x] Python environment configuration
- [x] Python–MySQL connectivity
- [x] SHA-256 hash generation
- [x] Duplicate file detection logic
- [x] Unique file metadata insertion
- [ ] Backup history integration
- [ ] Physical file storage management
- [ ] Storage space savings calculation
- [ ] User interface development
- [ ] End-to-end testing

🔮 What's Next?

There is still room to improve DedupVault. Some features I would like to work on in the future include:

- A simple web-based dashboard to make the system easier to use.
- A file upload interface for checking duplicates.
- Automated backup management.
- Storage analytics to show how much space has been saved.
- File restoration and recovery options.
- Better file management and reporting features.

🎓 What I'm Learning Through This Project

Building DedupVault gives me an opportunity to apply concepts I've learned during my BCA in Data Science to a practical problem.

Some of the key areas I'm working with are:

- Database design and management.
- SQL queries and database constraints.
- Python and MySQL integration.
- File handling and SHA-256 hashing.
- Data integrity and duplicate detection.
- Writing modular and maintainable code.
- Using Git and GitHub to manage project development.

👩‍💻About the Developer

Snaha Chaudhuri

BCA – Data Science

I'm currently exploring Python, SQL, database management, and software development through hands-on projects like DedupVault.
Connect with me:

GitHub: Snaha-pixel

LinkedIn: Snaha Chaudhuri

⭐ If you find this project interesting, feel free to explore the repository!

DedupVault – Store Smarter. Detect Duplicates. Optimize Storage.
