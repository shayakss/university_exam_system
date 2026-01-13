-- MySQL Database Setup Script
-- Run this in MySQL Workbench or MySQL Command Line Client
-- (Connect as root user first)

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS exam_management 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Step 2: Create the user (for localhost)
CREATE USER IF NOT EXISTS 'ems_user'@'localhost' IDENTIFIED BY 'StrongPass123!';

-- Step 3: Grant all privileges
GRANT ALL PRIVILEGES ON exam_management.* TO 'ems_user'@'localhost';

-- Step 4: Apply changes
FLUSH PRIVILEGES;

-- Step 5: Verify user was created
SELECT User, Host FROM mysql.user WHERE User = 'ems_user';

-- Step 6: Show granted privileges
SHOW GRANTS FOR 'ems_user'@'localhost';
