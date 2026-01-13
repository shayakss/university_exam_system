"""
Check and Reset Admin Password in Release Database (Correct Hashing - Bcrypt)
"""
import sqlite3
import bcrypt

# Path to the Release database
db_path = r"d:\New folder\New folder (2)\university_exam_system\Release\exam_system.db"

print(f"Checking database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT user_id, username, role FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    # Generate bcrypt hash for 'admin123'
    password = "admin123"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    if admin:
        print(f"✓ Admin user found: ID={admin[0]}, Role={admin[2]}")
        
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed_password,))
        conn.commit()
        print("✓ Password reset to 'admin123' using Bcrypt")
    else:
        print("✗ Admin user NOT found! Creating it...")
        
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, full_name, email, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('admin', hashed_password, 'Admin', 'System Administrator', 'admin@system.com', 1))
        conn.commit()
        print("✓ Admin user created with password 'admin123' using Bcrypt")
        
    # Verify
    cursor.execute("SELECT username, password_hash FROM users WHERE username = 'admin'")
    user = cursor.fetchone()
    print(f"Current Hash: {user[1]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
