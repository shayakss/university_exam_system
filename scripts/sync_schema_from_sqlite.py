"""
Sync All Missing Columns from SQLite to MySQL
Analyzes SQLite schema and adds any missing columns to MySQL
"""
import sqlite3
import mysql.connector
from mysql.connector import Error as MySQLError
import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, 'r') as f:
        return json.load(f)

def get_sqlite_schema():
    """Get all tables and columns from SQLite database"""
    db_path = os.path.join(os.path.dirname(__file__), "exam_system.db")
    if not os.path.exists(db_path):
        print("ℹ SQLite database not found, skipping schema sync")
        return {}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = {}
        for row in cursor.fetchall():
            col_name = row[1]
            col_type = row[2]
            # Convert SQLite types to MySQL types
            mysql_type = col_type.upper()
            if 'INT' in mysql_type and 'AUTOINCREMENT' not in mysql_type:
                mysql_type = 'INT'
            elif 'TEXT' in mysql_type:
                mysql_type = 'TEXT'
            elif 'REAL' in mysql_type:
                mysql_type = 'DECIMAL(10,2)'
            elif 'BLOB' in mysql_type:
                mysql_type = 'BLOB'
            columns[col_name] = mysql_type
        schema[table] = columns
    
    conn.close()
    return schema

def get_mysql_schema(conn):
    """Get all tables and columns from MySQL database"""
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = {}
        for row in cursor.fetchall():
            col_name = row[0]
            col_type = row[1]
            columns[col_name] = col_type
        schema[table] = columns
    
    return schema

def sync_schemas():
    print("=" * 70)
    print("  Syncing SQLite Schema to MySQL")
    print("=" * 70)
    
    # Get SQLite schema
    print("\nAnalyzing SQLite database...")
    sqlite_schema = get_sqlite_schema()
    if not sqlite_schema:
        return
    
    print(f"✓ Found {len(sqlite_schema)} tables in SQLite")
    
    # Connect to MySQL
    config = load_config()
    try:
        conn = mysql.connector.connect(
            host=config.get('mysql_host', 'localhost'),
            user=config.get('mysql_user', 'root'),
            password=config.get('mysql_password', ''),
            database=config.get('mysql_database', 'exam_management')
        )
        print("✓ Connected to MySQL")
    except MySQLError as e:
        print(f"✗ MySQL connection failed: {e}")
        return
    
    # Get MySQL schema
    print("\nAnalyzing MySQL database...")
    mysql_schema = get_mysql_schema(conn)
    print(f"✓ Found {len(mysql_schema)} tables in MySQL")
    
    # Find and add missing columns
    cursor = conn.cursor()
    added_count = 0
    
    print("\nChecking for missing columns...")
    for table, sqlite_columns in sqlite_schema.items():
        if table not in mysql_schema:
            print(f"\n  ⚠ Table '{table}' exists in SQLite but not in MySQL (skipping)")
            continue
        
        mysql_columns = mysql_schema[table]
        
        for col_name, col_type in sqlite_columns.items():
            if col_name not in mysql_columns:
                try:
                    # Add missing column
                    sql = f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}"
                    cursor.execute(sql)
                    print(f"  ✓ Added {table}.{col_name} ({col_type})")
                    added_count += 1
                except MySQLError as e:
                    print(f"  ✗ Failed to add {table}.{col_name}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    if added_count > 0:
        print(f"  ✅ Added {added_count} missing column(s)")
    else:
        print("  ✅ All columns are in sync")
    print("=" * 70)

if __name__ == "__main__":
    try:
        sync_schemas()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
