
USE backup_optimizer;

-- View stored unique files
SELECT * FROM stored_files;

-- View backup history
SELECT * FROM backup_records;

-- Count unique files
SELECT COUNT(*) AS total_unique_files
FROM stored_files;

-- Count total upload attempts
SELECT COUNT(*) AS total_upload_attempts
FROM backup_records;
