-- MySQL Migration: Add new student fields and department gender counts
-- Converted from SQLite to MySQL syntax
-- Date: 2025-11-26

-- Add new columns to students table (use IF NOT EXISTS equivalent for MySQL)
ALTER TABLE students ADD COLUMN IF NOT EXISTS registration_no VARCHAR(50);
ALTER TABLE students ADD COLUMN IF NOT EXISTS cnic VARCHAR(15);
ALTER TABLE students ADD COLUMN IF NOT EXISTS father_name VARCHAR(100);
ALTER TABLE students ADD COLUMN IF NOT EXISTS father_cnic VARCHAR(15);
ALTER TABLE students ADD COLUMN IF NOT EXISTS address TEXT;
ALTER TABLE students ADD COLUMN IF NOT EXISTS guardian_phone VARCHAR(20);

-- Note: phone column already exists in students table

-- Add gender count columns to departments table
ALTER TABLE departments ADD COLUMN IF NOT EXISTS male_count INT DEFAULT 0;
ALTER TABLE departments ADD COLUMN IF NOT EXISTS female_count INT DEFAULT 0;

-- Update existing department counts based on current students
UPDATE departments SET 
    male_count = (
        SELECT COUNT(*) FROM students 
        WHERE students.department_id = departments.department_id 
        AND students.gender = 'Male'
    ),
    female_count = (
        SELECT COUNT(*) FROM students 
        WHERE students.department_id = departments.department_id 
        AND students.gender = 'Female'
    );
