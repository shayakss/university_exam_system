"""
Reset Admin User
Deletes and recreates the admin user with correct password hash
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import db
from utils.security import hash_password

def reset_admin():
    """Delete and recreate admin user"""
    print("=" * 70)
    print("  Resetting Admin User")
    print("=" * 70)
    
    try:
        # Delete existing admin user
        print("\nDeleting existing admin user...")
        db.execute_update("DELETE FROM users WHERE username = %s", ('admin',))
        print("✓ Deleted existing admin user")
        
        # Create new admin user with correct bcrypt hash
        print("\nCreating new admin user with bcrypt hash...")
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
            print("✓ Created new admin user")
            print("\n" + "=" * 70)
            print("  ✅ ADMIN USER RESET SUCCESSFUL")
            print("=" * 70)
            print("\n  Login Credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\n  ⚠️  Change the password after first login!")
            print("=" * 70)
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
        reset_admin()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
