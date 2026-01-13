"""
Check and Reset Admin Password in Release Database
"""
import sqlite3
import hashlib

# Path to the Release database
db_path = r"d:\New folder\New folder (2)\university_exam_system\Release\exam_system.db"

print(f"Checking database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT user_id, username, role FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if admin:
        print(f"✓ Admin user found: ID={admin[0]}, Role={admin[2]}")
        
        # Reset password to 'admin123'
        # The system uses SHA256 hashing
        password = "admin123"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (hashed_password,))
        conn.commit()
        print("✓ Password reset to 'admin123'")
    else:
        print("✗ Admin user NOT found! Creating it...")
        
        # Create admin user
        password = "admin123"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO users (username, password, role, full_name, email, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('admin', hashed_password, 'Admin', 'System Administrator', 'admin@system.com', 1))
        conn.commit()
        print("✓ Admin user created with password 'admin123'")
        
    # Verify
    cursor.execute("SELECT username, password FROM users WHERE username = 'admin'")
    user = cursor.fetchone()
    print(f"Current Hash: {user[1]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
