"""
Update Users Table
Adds missing columns to users table
"""
import mysql.connector
from mysql.connector import Error as MySQLError
import json
import os

def update_users_table():
    print("=" * 70)
    print("  Updating Users Table")
    print("=" * 70)
    
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    try:
        conn = mysql.connector.connect(
            host=config.get('mysql_host', 'localhost'),
            user=config.get('mysql_user', 'root'),
            password=config.get('mysql_password', ''),
            database=config.get('mysql_database', 'exam_management')
        )
        print("✓ Connected to MySQL")
        
        cursor = conn.cursor()
        
        # Add failed_login_attempts
        try:
            print("Adding failed_login_attempts column...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN failed_login_attempts INT DEFAULT 0
            """)
            print("✓ Added failed_login_attempts")
        except MySQLError as e:
            if "Duplicate column name" in str(e):
                print("ℹ Column failed_login_attempts already exists")
            else:
                print(f"✗ Error: {e}")

        # Add is_locked
        try:
            print("Adding is_locked column...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN is_locked TINYINT DEFAULT 0
            """)
            print("✓ Added is_locked")
        except MySQLError as e:
            if "Duplicate column name" in str(e):
                print("ℹ Column is_locked already exists")
            else:
                print(f"✗ Error: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("\n✅ Users table updated successfully!")
        
    except MySQLError as e:
        print(f"✗ Connection failed: {e}")

if __name__ == "__main__":
    update_users_table()
