"""
Complete MySQL Schema Setup
Adds all missing columns and tables required by the application
"""
import mysql.connector
from mysql.connector import Error as MySQLError
import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, 'r') as f:
        return json.load(f)

def execute_sql(cursor, sql, description):
    """Execute SQL and handle errors"""
    try:
        cursor.execute(sql)
        print(f"  ✓ {description}")
        return True
    except MySQLError as e:
        if "Duplicate column" in str(e) or "already exists" in str(e):
            print(f"  ℹ {description} (already exists)")
            return True
        else:
            print(f"  ✗ {description}: {e}")
            return False

def complete_schema():
    print("=" * 70)
    print("  Completing MySQL Schema")
    print("=" * 70)
    
    config = load_config()
    
    try:
        conn = mysql.connector.connect(
            host=config.get('mysql_host', 'localhost'),
            user=config.get('mysql_user', 'root'),
            password=config.get('mysql_password', ''),
            database=config.get('mysql_database', 'exam_management')
        )
        print("✓ Connected to MySQL\n")
        
        cursor = conn.cursor()
        
        # Add missing columns to users table
        print("Adding missing columns to users table...")
        execute_sql(cursor, "ALTER TABLE users ADD COLUMN last_login TIMESTAMP NULL", "last_login column")
        
        # Create student_attendance table
        print("\nCreating student_attendance table...")
        execute_sql(cursor, """
            CREATE TABLE IF NOT EXISTS student_attendance (
                attendance_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT NOT NULL,
                course_id INT,
                attendance_date DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'Present',
                marked_by INT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL,
                FOREIGN KEY (marked_by) REFERENCES users(user_id),
                UNIQUE KEY unique_student_course_date (student_id, course_id, attendance_date),
                INDEX idx_attendance_date (attendance_date),
                INDEX idx_attendance_student (student_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """, "student_attendance table")
        
        # Create teacher_attendance table
        print("\nCreating teacher_attendance table...")
        execute_sql(cursor, """
            CREATE TABLE IF NOT EXISTS teacher_attendance (
                attendance_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                attendance_date DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'Present',
                marked_by INT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (marked_by) REFERENCES users(user_id),
                UNIQUE KEY unique_user_date (user_id, attendance_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """, "teacher_attendance table")
        
        # Create user_preferences table
        print("\nCreating user_preferences table...")
        execute_sql(cursor, """
            CREATE TABLE IF NOT EXISTS user_preferences (
                preference_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                theme VARCHAR(20) DEFAULT 'light',
                language VARCHAR(10) DEFAULT 'en',
                notifications_enabled TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE KEY unique_user (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """, "user_preferences table")
        
        # Create class_schedule table
        print("\nCreating class_schedule table...")
        execute_sql(cursor, """
            CREATE TABLE IF NOT EXISTS class_schedule (
                schedule_id INT PRIMARY KEY AUTO_INCREMENT,
                course_id INT NOT NULL,
                teacher_id INT NOT NULL,
                department_id INT NOT NULL,
                semester INT NOT NULL,
                day_of_week VARCHAR(20) NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                room_number VARCHAR(50),
                is_active TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """, "class_schedule table")
        
        # Create exam_schedule table
        print("\nCreating exam_schedule table...")
        execute_sql(cursor, """
            CREATE TABLE IF NOT EXISTS exam_schedule (
                exam_id INT PRIMARY KEY AUTO_INCREMENT,
                course_id INT NOT NULL,
                department_id INT NOT NULL,
                semester INT NOT NULL,
                exam_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                room_number VARCHAR(50),
                exam_type VARCHAR(20) DEFAULT 'Final',
                total_marks INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """, "exam_schedule table")
        
        # Create assignment_submissions table
        print("\nCreating assignment_submissions table...")
        execute_sql(cursor, """
            CREATE TABLE IF NOT EXISTS assignment_submissions (
                submission_id INT PRIMARY KEY AUTO_INCREMENT,
                assignment_id INT NOT NULL,
                student_id INT NOT NULL,
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'Pending',
                marks_obtained DECIMAL(10,2),
                remarks TEXT,
                file_path VARCHAR(500),
                FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                UNIQUE KEY unique_assignment_student (assignment_id, student_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """, "assignment_submissions table")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("  ✅ SCHEMA COMPLETION SUCCESSFUL")
        print("=" * 70)
        print("\n  All missing tables and columns have been added!")
        print("  Your application should now work properly.")
        print("=" * 70)
        
    except MySQLError as e:
        print(f"\n✗ Error: {e}")
        return False

if __name__ == "__main__":
    complete_schema()
