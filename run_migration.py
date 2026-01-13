"""
Run database migration to add new student fields
"""
from database.db_manager import db

# Read migration SQL
with open('database/migrations/add_student_fields.sql', 'r') as f:
    sql_script = f.read()

# Split into individual statements
statements = [s.strip() for s in sql_script.split(';') if s.strip() and not s.strip().startswith('--')]

# Execute each statement
for statement in statements:
    if statement:
        try:
            db.execute_update(statement)
            print(f"✓ Executed: {statement[:50]}...")
        except Exception as e:
            print(f"✗ Error: {e}")
            print(f"  Statement: {statement[:100]}")

print("\n✓ Migration completed!")
