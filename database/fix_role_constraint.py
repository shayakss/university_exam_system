"""
Fix role constraint in users table to allow Teacher and Student roles
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'exam_system.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # SQLite doesn't support ALTER TABLE to modify constraints
    # We need to recreate the table without the CHECK constraint
    
    print("Creating backup of users table...")
    cursor.execute("""
        CREATE TABLE users_backup AS SELECT * FROM users
    """)
    
    print("Dropping old users table...")
    cursor.execute("DROP TABLE users")
    
    print("Creating new users table without role constraint...")
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            department_id INTEGER,
            student_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            is_locked INTEGER DEFAULT 0,
            failed_login_attempts INTEGER DEFAULT 0,
            account_expiry DATE,
            FOREIGN KEY (department_id) REFERENCES departments(department_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)
    
    print("Restoring user data...")
    cursor.execute("""
        INSERT INTO users SELECT * FROM users_backup
    """)
    
    print("Dropping backup table...")
    cursor.execute("DROP TABLE users_backup")
    
    conn.commit()
    print("✓ Successfully updated users table!")
    print("✓ Teacher and Student roles are now allowed")
    
except Exception as e:
    conn.rollback()
    print(f"✗ Error: {e}")
finally:
    conn.close()
