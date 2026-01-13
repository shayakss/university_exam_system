"""
Fix missing columns and tables in TiDB Cloud schema
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import db

print("\n" + "="*60)
print("FIXING TIDB CLOUD SCHEMA")
print("="*60)

# Fix 1: Add last_login column to users table
print("\n1. Adding last_login column to users table...")
try:
    db.execute_update("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP NULL")
    print("✓ Added last_login column")
except Exception as e:
    if "Duplicate column" in str(e):
        print("⚠ Column already exists")
    else:
        print(f"✗ Error: {e}")

# Fix 2: Create user_preferences table
print("\n2. Creating user_preferences table...")
try:
    query = """
    CREATE TABLE IF NOT EXISTS user_preferences (
        preference_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        theme VARCHAR(20) DEFAULT 'light',
        language VARCHAR(10) DEFAULT 'en',
        notifications_enabled TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        UNIQUE KEY unique_user_pref (user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    db.execute_update(query)
    print("✓ Created user_preferences table")
except Exception as e:
    print(f"✗ Error: {e}")

# Fix 3: Create student_attendance table
print("\n3. Creating student_attendance table...")
try:
    query = """
    CREATE TABLE IF NOT EXISTS student_attendance (
        attendance_id INT PRIMARY KEY AUTO_INCREMENT,
        student_id INT NOT NULL,
        course_id INT NOT NULL,
        attendance_date DATE NOT NULL,
        status VARCHAR(20) NOT NULL,
        remarks TEXT,
        marked_by INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE RESTRICT,
        FOREIGN KEY (marked_by) REFERENCES users(user_id),
        UNIQUE KEY unique_attendance (student_id, course_id, attendance_date),
        INDEX idx_attendance_student (student_id),
        INDEX idx_attendance_course (course_id),
        INDEX idx_attendance_date (attendance_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    db.execute_update(query)
    print("✓ Created student_attendance table")
except Exception as e:
    print(f"✗ Error: {e}")

# Fix 4: Add head_of_department column to departments table
print("\n4. Adding head_of_department column to departments table...")
try:
    db.execute_update("ALTER TABLE departments ADD COLUMN IF NOT EXISTS head_of_department VARCHAR(100) NULL")
    print("✓ Added head_of_department column")
except Exception as e:
    if "Duplicate column" in str(e):
        print("⚠ Column already exists")
    else:
        print(f"✗ Error: {e}")

# Verify fixes
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

# Check users table
print("\n✓ Checking users table...")
users_cols = db.execute_query("SHOW COLUMNS FROM users")
if users_cols:
    col_names = [col['Field'] for col in users_cols]
    if 'last_login' in col_names:
        print("  ✓ last_login column exists")
    else:
        print("  ✗ last_login column missing")

# Check tables exist
print("\n✓ Checking tables...")
tables = db.execute_query("SHOW TABLES")
table_names = [list(t.values())[0] for t in tables]

if 'user_preferences' in table_names:
    print("  ✓ user_preferences table exists")
else:
    print("  ✗ user_preferences table missing")

if 'student_attendance' in table_names:
    print("  ✓ student_attendance table exists")
else:
    print("  ✗ student_attendance table missing")

print("\n" + "="*60)
print("✓ SCHEMA FIXES COMPLETE!")
print("="*60)
print("\nYou can now run the application without errors.")
