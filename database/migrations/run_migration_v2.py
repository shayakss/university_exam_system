"""
Database Migration Script V2
Applies new schema for feature enhancements
"""
import sqlite3
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from database.db_manager import db
import config
from datetime import datetime

def run_migration():
    """Run the database migration"""
    print("=" * 60)
    print("Database Migration V2 - Feature Enhancements")
    print("=" * 60)
    
    # Backup database first
    backup_path = os.path.join(
        config.BACKUP_DIR,
        f"pre_migration_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    )
    
    print(f"\n📦 Creating backup at: {backup_path}")
    try:
        import shutil
        os.makedirs(config.BACKUP_DIR, exist_ok=True)
        shutil.copy2(config.DATABASE_PATH, backup_path)
        print("✓ Backup created successfully")
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        response = input("Continue without backup? (yes/no): ")
        if response.lower() != 'yes':
            print("Migration cancelled")
            return False
    
    # Read migration SQL
    migration_file = os.path.join(
        os.path.dirname(__file__),
        'database_migration_v2.sql'
    )
    
    print(f"\n📄 Reading migration file: {migration_file}")
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        print("✓ Migration file loaded")
    except Exception as e:
        print(f"✗ Failed to read migration file: {e}")
        return False
    
    # Execute migration
    print("\n🔧 Executing migration...")
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Split by semicolon and execute each statement
        statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
        
        total = len(statements)
        for i, statement in enumerate(statements, 1):
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    # Show progress every 10 statements
                    if i % 10 == 0 or i == total:
                        print(f"  Progress: {i}/{total} statements executed")
                except Exception as e:
                    # Ignore "already exists" errors
                    if "already exists" not in str(e).lower():
                        print(f"  Warning on statement {i}: {e}")
        
        conn.commit()
        conn.close()
        print("✓ Migration executed successfully")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        print(f"\n⚠ You can restore from backup: {backup_path}")
        return False
    
    # Verify migration
    print("\n🔍 Verifying migration...")
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check for new tables
        new_tables = [
            'student_attendance', 'teacher_attendance',
            'class_schedule', 'exam_schedule',
            'assignments', 'assignment_submissions',
            'promotion_rules', 'promotion_history',
            'id_cards', 'alumni', 'alumni_employment',
            'roles', 'permissions', 'role_permissions', 'user_roles',
            'audit_logs',
            'archived_students', 'archived_marks', 'archived_results', 'archive_metadata',
            'backup_config', 'user_preferences'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        for table in new_tables:
            if table in existing_tables:
                print(f"  ✓ Table '{table}' created")
            else:
                print(f"  ✗ Table '{table}' missing")
                missing_tables.append(table)
        
        conn.close()
        
        if missing_tables:
            print(f"\n⚠ Warning: {len(missing_tables)} tables were not created")
            return False
        else:
            print(f"\n✓ All {len(new_tables)} tables verified successfully")
            
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ Migration completed successfully!")
    print("=" * 60)
    print(f"\nBackup location: {backup_path}")
    print("\nNew features are now available:")
    print("  • Attendance Tracking")
    print("  • Timetable & Scheduling")
    print("  • Assignment Management")
    print("  • Student Promotion System")
    print("  • ID Card Generation")
    print("  • Alumni Database")
    print("  • Role-Based Access Control")
    print("  • Audit Logging")
    print("  • Database Archiving")
    print("  • Cloud Backup Configuration")
    print("  • User Preferences (Theme Support)")
    
    return True

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
