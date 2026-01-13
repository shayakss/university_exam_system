"""
Script to clear all data and import fresh data from Excel file
"""
import sqlite3
import pandas as pd
import config
from controllers.department_controller import department_controller
from controllers.course_controller import course_controller
from controllers.student_controller import student_controller
from controllers.marks_controller import marks_controller
from controllers.user_controller import user_controller
from utils.security import hash_password

def clear_all_data():
    """Clear all data from the database except admin user"""
    print("Clearing all data from database...")
    
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Delete in order to respect foreign key constraints
        cursor.execute("DELETE FROM results")
        cursor.execute("DELETE FROM marks")
        cursor.execute("DELETE FROM courses")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM users WHERE role != 'Admin'")
        cursor.execute("DELETE FROM departments")
        
        conn.commit()
        print("✓ All data cleared successfully")
        return True
    except Exception as e:
        print(f"✗ Error clearing data: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def import_excel_data(file_path):
    """Import data from Excel file"""
    print(f"\nImporting data from: {file_path}")
    
    try:
        # Read all sheets
        excel_data = pd.read_excel(file_path, sheet_name=None)
        print(f"Found {len(excel_data)} sheets")
        
        # Process each sheet
        for sheet_name, df in excel_data.items():
            print(f"\nProcessing sheet: {sheet_name}")
            print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"Columns: {list(df.columns)}")
            
        return True
    except Exception as e:
        print(f"✗ Error importing data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RESET AND IMPORT TOOL")
    print("=" * 60)
    
    # Step 1: Clear all data
    if clear_all_data():
        # Step 2: Import new data
        file_path = r"sample_data\Computer science  2021-to-2025  8 Semesters Results.xls"
        import_excel_data(file_path)
    
    print("\n" + "=" * 60)
    print("Process completed")
    print("=" * 60)
