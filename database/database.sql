CREATE DATABASE IF NOT EXISTS backup_optimizer;

USE backup_optimizer;

CREATE TABLE IF NOT EXISTS stored_files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    file_hash CHAR(64) NOT NULL UNIQUE,
    original_name VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS backup_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    uploaded_name VARCHAR(255) NOT NULL,
    file_hash CHAR(64) NOT NULL,
    file_size BIGINT NOT NULL,
    backup_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);