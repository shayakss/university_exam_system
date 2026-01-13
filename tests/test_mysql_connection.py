"""
Test MySQL Connection
Verifies that MySQL connection is working correctly
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from database.db_manager import db

def test_connection():
    """Test database connection"""
    print("=" * 70)
    print("  MySQL Connection Test")
    print("=" * 70)
    
    print(f"\nDatabase Type: {'MySQL' if config.USE_MYSQL else 'SQLite'}")
    
    if config.USE_MYSQL:
        print(f"Host: {config.MYSQL_HOST}")
        print(f"User: {config.MYSQL_USER}")
        print(f"Database: {config.MYSQL_DATABASE}")
        print(f"Port: {config.MYSQL_PORT}")
    
    try:
        # Get connection
        conn = db.get_connection()
        print("\n✓ Database connection successful!")
        
        # Test query
        print("\n📊 Testing query execution...")
        result = db.execute_query("SELECT 1 as test")
        if result and result[0]['test'] == 1:
            print("✓ Query execution successful!")
        
        # Check tables
        print("\n📋 Checking tables...")
        tables = [
            'departments', 'students', 'courses', 
            'marks', 'results', 'users'
        ]
        
        for table in tables:
            if db.table_exists(table):
                count = db.get_table_count(table)
                print(f"  ✓ {table}: {count} records")
            else:
                print(f"  ✗ {table}: not found")
        
        print("\n" + "=" * 70)
        print("  CONNECTION TEST PASSED")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n✗ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
