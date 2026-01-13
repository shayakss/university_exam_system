import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "exam_system.db")

def add_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add guardian_phone column
        try:
            cursor.execute("ALTER TABLE students ADD COLUMN guardian_phone TEXT")
            print("Added guardian_phone column")
        except sqlite3.OperationalError:
            print("guardian_phone column already exists")
            
        # Add address column
        try:
            cursor.execute("ALTER TABLE students ADD COLUMN address TEXT")
            print("Added address column")
        except sqlite3.OperationalError:
            print("address column already exists")
            
        conn.commit()
        print("Schema update completed successfully")
        
    except Exception as e:
        print(f"Error updating schema: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_columns()
