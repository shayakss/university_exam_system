"""
Debug login issue - check users table
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'exam_system.db')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    print("Checking users table...")
    cursor.execute("SELECT user_id, username, role, is_active, is_locked FROM users")
    users = cursor.fetchall()
    
    print(f"\nFound {len(users)} users:")
    for user in users:
        print(f"  - ID: {user['user_id']}, Username: {user['username']}, Role: {user['role']}, Active: {user['is_active']}, Locked: {user['is_locked']}")
    
    # Check if admin exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if admin:
        print("\n✓ Admin user found")
        print(f"  Username: {admin['username']}")
        print(f"  Role: {admin['role']}")
        print(f"  Is Active: {admin['is_active']}")
        print(f"  Is Locked: {admin['is_locked']}")
        print(f"  Password Hash Length: {len(admin['password_hash']) if admin['password_hash'] else 0}")
    else:
        print("\n✗ Admin user NOT found!")
        print("Creating admin user...")
        
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from utils.security import hash_password
        
        password_hash = hash_password('admin123')
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, full_name, is_active)
            VALUES ('admin', ?, 'Admin', 'Administrator', 1)
        """, (password_hash,))
        conn.commit()
        print("✓ Admin user created with password 'admin123'")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
