import sqlite3
import config

DB_PATH = config.DATABASE_PATH

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(departments)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'head_of_department' not in columns:
            print("Adding head_of_department column...")
            cursor.execute("ALTER TABLE departments ADD COLUMN head_of_department TEXT")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column head_of_department already exists.")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
