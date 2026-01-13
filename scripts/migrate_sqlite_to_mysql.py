"""
SQLite to MySQL Data Migration Script
University Exam Management System

This script migrates all data from SQLite (exam_system.db) to MySQL database.
"""
import sqlite3
import mysql.connector
from mysql.connector import Error as MySQLError
import os
import sys
import json
from datetime import datetime

# Load MySQL configuration
def load_config():
    """Load MySQL configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        print("✗ config.json not found!")
        print("  Please create config.json with MySQL connection details")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    if config.get('use') != 'mysql':
        print("✗ config.json is not set to use MySQL")
        sys.exit(1)
    
    return config

# Get SQLite database path
def get_sqlite_path():
    """Get path to SQLite database"""
    db_path = os.path.join(os.path.dirname(__file__), "exam_system.db")
    if not os.path.exists(db_path):
        print(f"✗ SQLite database not found at: {db_path}")
        sys.exit(1)
    return db_path

def connect_sqlite(db_path):
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"✓ Connected to SQLite: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ SQLite connection error: {e}")
        sys.exit(1)

def connect_mysql(config):
    """Connect to MySQL database"""
    try:
        conn = mysql.connector.connect(
            host=config.get('mysql_host', 'localhost'),
            user=config.get('mysql_user', 'root'),
            password=config.get('mysql_password', ''),
            database=config.get('mysql_database', 'exam_management'),
            port=config.get('mysql_port', 3306),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        print(f"✓ Connected to MySQL: {config['mysql_user']}@{config['mysql_host']}/{config['mysql_database']}")
        return conn
    except MySQLError as e:
        print(f"✗ MySQL connection error: {e}")
        sys.exit(1)

def get_table_list(sqlite_conn):
    """Get list of all tables from SQLite"""
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    return tables

def get_table_columns(sqlite_conn, table_name):
    """Get column names for a table"""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns

def migrate_table(sqlite_conn, mysql_conn, table_name):
    """Migrate a single table from SQLite to MySQL"""
    print(f"\n📋 Migrating table: {table_name}")
    
    # Get columns
    columns = get_table_columns(sqlite_conn, table_name)
    if not columns:
        print(f"  ⚠ No columns found, skipping")
        return 0
    
    # Get data from SQLite
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    if not rows:
        print(f"  ℹ No data to migrate")
        return 0
    
    # Prepare MySQL insert
    placeholders = ', '.join(['%s'] * len(columns))
    column_names = ', '.join(columns)
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    
    # Insert data into MySQL
    mysql_cursor = mysql_conn.cursor()
    migrated_count = 0
    failed_count = 0
    
    for row in rows:
        try:
            # Convert Row object to tuple
            values = tuple(row)
            mysql_cursor.execute(insert_query, values)
            migrated_count += 1
        except MySQLError as e:
            failed_count += 1
            if failed_count <= 3:  # Show first 3 errors
                print(f"  ⚠ Error inserting row: {e}")
    
    mysql_conn.commit()
    
    print(f"  ✓ Migrated {migrated_count} rows")
    if failed_count > 0:
        print(f"  ⚠ Failed to migrate {failed_count} rows")
    
    return migrated_count

def clear_mysql_tables(mysql_conn, tables):
    """Clear all tables in MySQL (in correct order to handle foreign keys)"""
    print("\n🗑️  Clearing existing MySQL data...")
    
    mysql_cursor = mysql_conn.cursor()
    
    # Disable foreign key checks temporarily
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    for table in tables:
        try:
            mysql_cursor.execute(f"TRUNCATE TABLE {table}")
            print(f"  ✓ Cleared {table}")
        except MySQLError as e:
            # Table might not exist yet
            print(f"  ℹ Could not clear {table}: {e}")
    
    # Re-enable foreign key checks
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    mysql_conn.commit()

def main():
    """Main migration function"""
    print("=" * 70)
    print("  SQLite to MySQL Data Migration")
    print("  University Exam Management System")
    print("=" * 70)
    
    # Load configuration
    config = load_config()
    
    # Connect to databases
    sqlite_path = get_sqlite_path()
    sqlite_conn = connect_sqlite(sqlite_path)
    mysql_conn = connect_mysql(config)
    
    # Get list of tables
    tables = get_table_list(sqlite_conn)
    print(f"\n📊 Found {len(tables)} tables to migrate:")
    for table in tables:
        print(f"  - {table}")
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will clear all existing data in MySQL database!")
    response = input("Continue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Migration cancelled.")
        return
    
    # Clear existing MySQL data
    clear_mysql_tables(mysql_conn, tables)
    
    # Define migration order (to handle foreign keys)
    # Tables with no dependencies first, then dependent tables
    priority_order = [
        'departments',
        'users',
        'students',
        'courses',
        'teachers',
        'marks',
        'results',
        'attendance',
        'student_attendance',
        'teacher_attendance',
        'class_schedule',
        'exam_schedule',
        'assignments',
        'assignment_submissions',
        'timetable',
        'promotion_rules',
        'promotion_history',
        'id_cards',
        'alumni',
        'alumni_employment',
        'roles',
        'permissions',
        'role_permissions',
        'user_roles',
        'audit_logs',
        'archived_students',
        'archived_marks',
        'archived_results',
        'archive_metadata',
        'backup_config',
        'user_preferences',
        'teacher_assignments',
        'login_attempts'
    ]
    
    # Migrate tables in order
    total_migrated = 0
    migrated_tables = []
    
    # First migrate priority tables
    for table in priority_order:
        if table in tables:
            count = migrate_table(sqlite_conn, mysql_conn, table)
            total_migrated += count
            migrated_tables.append(table)
    
    # Then migrate any remaining tables
    for table in tables:
        if table not in migrated_tables:
            count = migrate_table(sqlite_conn, mysql_conn, table)
            total_migrated += count
    
    # Close connections
    sqlite_conn.close()
    mysql_conn.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("  MIGRATION COMPLETE")
    print("=" * 70)
    print(f"  Total tables migrated: {len(tables)}")
    print(f"  Total rows migrated: {total_migrated}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print("\n✅ Data migration successful!")
    print("   You can now use the application with MySQL database.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
