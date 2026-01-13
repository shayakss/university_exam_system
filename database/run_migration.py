"""
Run database migration for Teacher/Student roles
"""
import sqlite3
import os

# Get database path
db_path = os.path.join(os.path.dirname(__file__), '..', 'exam_system.db')

# Read migration SQL
migration_path = os.path.join(os.path.dirname(__file__), 'migration_teacher_student.sql')
with open(migration_path, 'r') as f:
    migration_sql = f.read()

# Connect and execute
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Execute migration
    cursor.executescript(migration_sql)
    conn.commit()
    print("✓ Migration completed successfully!")
    print("✓ Added new columns to users table")
    print("✓ Created teacher_assignments table")
    print("✓ Created login_attempts table")
    print("✓ Created indexes")
except Exception as e:
    conn.rollback()
    print(f"✗ Migration failed: {e}")
finally:
    conn.close()
