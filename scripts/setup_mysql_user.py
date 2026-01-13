"""
MySQL Database Setup Helper
Creates the database and user if they don't exist
Run this as MySQL root user
"""
import mysql.connector
from mysql.connector import Error as MySQLError
import getpass

def setup_database():
    """Setup MySQL database and user"""
    print("=" * 70)
    print("  MySQL Database Setup")
    print("  University Exam Management System")
    print("=" * 70)
    
    print("\nThis script will create:")
    print("  - Database: exam_management")
    print("  - User: ems_user")
    print("  - Password: StrongPass123!")
    print("\nYou need MySQL root credentials to proceed.")
    print("-" * 70)
    
    # Get root credentials
    root_user = input("\nMySQL root username [root]: ").strip() or "root"
    root_password = getpass.getpass("MySQL root password: ")
    host = input("MySQL host [localhost]: ").strip() or "localhost"
    
    # Connect as root
    try:
        print("\nConnecting to MySQL as root...")
        conn = mysql.connector.connect(
            host=host,
            user=root_user,
            password=root_password
        )
        print("✓ Connected successfully")
    except MySQLError as e:
        print(f"✗ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure MySQL server is running")
        print("  2. Verify root username and password")
        print("  3. Check if MySQL is accessible on localhost")
        return False
    
    cursor = conn.cursor()
    
    try:
        # Create database
        print("\n1. Creating database 'exam_management'...")
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS exam_management 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        print("   ✓ Database created")
        
        # Create user
        print("\n2. Creating user 'ems_user'@'localhost'...")
        try:
            cursor.execute("DROP USER IF EXISTS 'ems_user'@'localhost'")
        except:
            pass
        
        cursor.execute("""
            CREATE USER 'ems_user'@'localhost' 
            IDENTIFIED BY 'StrongPass123!'
        """)
        print("   ✓ User created")
        
        # Grant privileges
        print("\n3. Granting privileges...")
        cursor.execute("""
            GRANT ALL PRIVILEGES ON exam_management.* 
            TO 'ems_user'@'localhost'
        """)
        print("   ✓ Privileges granted")
        
        # Flush privileges
        print("\n4. Applying changes...")
        cursor.execute("FLUSH PRIVILEGES")
        print("   ✓ Changes applied")
        
        # Verify
        print("\n5. Verifying setup...")
        cursor.execute("SELECT User, Host FROM mysql.user WHERE User = 'ems_user'")
        users = cursor.fetchall()
        if users:
            print(f"   ✓ User found: {users[0]}")
        
        cursor.execute("SHOW GRANTS FOR 'ems_user'@'localhost'")
        grants = cursor.fetchall()
        print(f"   ✓ Privileges: {len(grants)} grant(s)")
        
        print("\n" + "=" * 70)
        print("  SETUP COMPLETE!")
        print("=" * 70)
        print("\nDatabase credentials:")
        print("  Host: localhost")
        print("  Database: exam_management")
        print("  Username: ems_user")
        print("  Password: StrongPass123!")
        print("\nYou can now run: python init_mysql_schema.py")
        print("=" * 70)
        
        return True
        
    except MySQLError as e:
        print(f"\n✗ Setup failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def test_connection():
    """Test if ems_user can connect"""
    print("\n" + "=" * 70)
    print("  Testing Connection")
    print("=" * 70)
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='ems_user',
            password='StrongPass123!',
            database='exam_management'
        )
        print("✓ Connection test successful!")
        print("  ems_user can access exam_management database")
        conn.close()
        return True
    except MySQLError as e:
        print(f"✗ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        if setup_database():
            print("\n")
            test_connection()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
