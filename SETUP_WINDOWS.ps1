# Windows PowerShell Commands for MySQL Setup
# University Exam Management System - MySQL Migration

## Step 1: Install MySQL Driver
pip install mysql-connector-python

## Step 2: Create MySQL Database
# Open MySQL command line or MySQL Workbench and run:
# CREATE DATABASE exam_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# CREATE USER 'ems_user'@'localhost' IDENTIFIED BY 'StrongPass123!';
# GRANT ALL PRIVILEGES ON exam_management.* TO 'ems_user'@'localhost';
# FLUSH PRIVILEGES;

## Step 3: Load Schema (PowerShell)
# Option 1: Using Get-Content (PowerShell way)
Get-Content database\schema.sql | mysql -u ems_user -p exam_management

# Option 2: Using mysql source command
mysql -u ems_user -p
# Then inside MySQL prompt:
# USE exam_management;
# source d:/New folder/New folder (2)/university_exam_system/database/schema.sql;
# exit;

## Step 4: Test Connection
python test_mysql_connection.py

## Step 5: Migrate Data (if you have SQLite data)
python migrate_sqlite_to_mysql.py

## Step 6: Run Application
python main.py

## Alternative: Use Python to Load Schema
python -c "from database.db_manager import db; db.initialize_schema()"
