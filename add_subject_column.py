import sqlite3
import os
import config

DB_PATH = config.DATABASE_PATH

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'assigned_subject_id' not in columns:
            print("Adding assigned_subject_id column...")
            cursor.execute("ALTER TABLE users ADD COLUMN assigned_subject_id INTEGER REFERENCES courses(course_id)")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column assigned_subject_id already exists.")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
