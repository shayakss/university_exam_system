"""
Quick Database Setup for New Features
Runs the SQL migration directly
"""
import sqlite3
import os
import sys

# Get database path
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'exam_system.db')

print("=" * 60)
print("Setting up new feature tables...")
print("=" * 60)

# Read SQL file
sql_file = os.path.join(current_dir, 'database', 'migrations', 'database_migration_v2.sql')

try:
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute SQL
    cursor.executescript(sql_content)
    conn.commit()
    conn.close()
    
    print("\n✓ All tables created successfully!")
    print("\nNew features are now available:")
    print("  • Attendance Tracking")
    print("  • Timetable & Scheduling")
    print("  • Assignment Management")
    print("  • Student Promotion")
    print("  • ID Card Generation")
    print("  • Alumni Database")
    print("  • RBAC System")
    print("  • Audit Logging")
    print("  • Database Archiving")
    print("  • Cloud Backup")
    print("  • Theme Preferences")
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nNote: Some tables may already exist, which is normal.")
    print("=" * 60)
