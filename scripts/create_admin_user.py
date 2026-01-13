"""
Create Default Admin User
Creates the default admin user in MySQL database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import db
from utils.security import hash_password

def create_admin_user():
    """Create default admin user"""
    print("=" * 70)
    print("  Creating Default Admin User")
    print("=" * 70)
    
    try:
        # Check if admin already exists
        existing = db.execute_query(
            "SELECT user_id FROM users WHERE username = %s",
            ('admin',)
        )
        
        if existing:
            print("\n⚠️  Admin user already exists!")
            print("   Username: admin")
            print("   If you forgot the password, delete the user and run this script again.")
            return False
        
        # Create admin user
        print("\nCreating admin user...")
        password_hash = hash_password('admin123')
        
        query = """
            INSERT INTO users (
                username, password_hash, full_name, role, 
                is_active, failed_login_attempts, is_locked
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        success, user_id = db.execute_update(
            query,
            ('admin', password_hash, 'System Administrator', 'Admin', 1, 0, 0)
        )
        
        if success:
            print("\n✅ Admin user created successfully!")
            print("\n" + "=" * 70)
            print("  Login Credentials")
            print("=" * 70)
            print("  Username: admin")
            print("  Password: admin123")
            print("=" * 70)
            print("\n⚠️  IMPORTANT: Change the password after first login!")
            return True
        else:
            print("\n✗ Failed to create admin user")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
