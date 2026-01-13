"""
Reset admin password to 'admin123'
"""
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.security import hash_password

db_path = os.path.join(os.path.dirname(__file__), '..', 'exam_system.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Hash the password
    new_password = hash_password('admin123')
    
    # Update admin user
    cursor.execute("""
        UPDATE users 
        SET password_hash = ?
        WHERE username = 'admin'
    """, (new_password,))
    
    conn.commit()
    print("✓ Admin password reset to 'admin123'")
    print("✓ You can now login with:")
    print("  Username: admin")
    print("  Password: admin123")
    
except Exception as e:
    conn.rollback()
    print(f"✗ Error: {e}")
finally:
    conn.close()
