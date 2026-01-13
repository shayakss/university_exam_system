"""
Migration script to add missing student fields
"""
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def migrate():
    """Add missing columns to students table"""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check existing columns
        cursor.execute("PRAGMA table_info(students)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")
        
        # Add missing columns
        columns_to_add = {
            'father_name': 'TEXT',
            'cnic': 'TEXT',
            'father_cnic': 'TEXT',
            'guardian_phone': 'TEXT',
            'registration_no': 'TEXT'
        }
        
        for column_name, column_type in columns_to_add.items():
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE students ADD COLUMN {column_name} {column_type}")
                    print(f"✓ Added column: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"✗ Failed to add {column_name}: {e}")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        
        # Verify columns
        cursor.execute("PRAGMA table_info(students)")
        all_columns = [row[1] for row in cursor.fetchall()]
        print(f"\nFinal columns: {all_columns}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Migration error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting database migration...")
    print(f"Database path: {config.DATABASE_PATH}")
    migrate()
