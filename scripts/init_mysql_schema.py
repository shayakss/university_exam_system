"""
Initialize MySQL Schema
Loads the schema.sql file into MySQL database
"""
import os
import sys
import mysql.connector
from mysql.connector import Error as MySQLError
import json

def load_config():
    """Load MySQL configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        print("✗ config.json not found!")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config

def load_schema():
    """Load and execute schema.sql"""
    print("=" * 70)
    print("  MySQL Schema Initialization")
    print("=" * 70)
    
    # Load config
    config = load_config()
    
    print(f"\nConnecting to MySQL...")
    print(f"Host: {config.get('mysql_host', 'localhost')}")
    print(f"Database: {config.get('mysql_database', 'exam_management')}")
    
    # Connect to MySQL
    try:
        conn = mysql.connector.connect(
            host=config.get('mysql_host', 'localhost'),
            user=config.get('mysql_user', 'root'),
            password=config.get('mysql_password', ''),
            database=config.get('mysql_database', 'exam_management'),
            port=config.get('mysql_port', 3306)
        )
        print("✓ Connected to MySQL")
    except MySQLError as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)
    
    # Read schema file
    schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
    if not os.path.exists(schema_path):
        print(f"✗ Schema file not found: {schema_path}")
        sys.exit(1)
    
    print(f"\nReading schema from: {schema_path}")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Split into individual statements
    statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
    
    print(f"Found {len(statements)} SQL statements")
    print("\nExecuting schema...")
    
    cursor = conn.cursor()
    executed = 0
    failed = 0
    
    for i, statement in enumerate(statements, 1):
        try:
            cursor.execute(statement)
            executed += 1
            # Show progress for every 5 statements
            if i % 5 == 0:
                print(f"  Executed {i}/{len(statements)} statements...")
        except MySQLError as e:
            failed += 1
            if failed <= 3:  # Show first 3 errors
                print(f"  ⚠ Error in statement {i}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("  SCHEMA INITIALIZATION COMPLETE")
    print("=" * 70)
    print(f"  Executed: {executed} statements")
    if failed > 0:
        print(f"  Failed: {failed} statements")
    print("=" * 70)
    
    if failed == 0:
        print("\n✅ Schema loaded successfully!")
    else:
        print(f"\n⚠️  Schema loaded with {failed} errors")
        print("   (Some errors may be normal, e.g., 'table already exists')")

if __name__ == "__main__":
    try:
        load_schema()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
