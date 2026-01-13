"""
Check and add missing columns
"""
import sqlite3

conn = sqlite3.connect('exam_system.db')
cursor = conn.cursor()

print("=== Checking Students Table ===\n")

# Get current columns
cursor.execute('PRAGMA table_info(students)')
columns = cursor.fetchall()
existing_cols = [col[1] for col in columns]

print(f"Existing columns ({len(existing_cols)}):")
for col in existing_cols:
    print(f"  - {col}")

# Columns we need
required_cols = {
    'registration_no': 'VARCHAR(50)',
    'cnic': 'VARCHAR(15)',
    'father_name': 'VARCHAR(100)',
    'father_cnic': 'VARCHAR(15)',
    'guardian_phone': 'VARCHAR(20)'
}

print(f"\n=== Adding Missing Columns ===\n")

for col_name, col_type in required_cols.items():
    if col_name not in existing_cols:
        try:
            query = f"ALTER TABLE students ADD COLUMN {col_name} {col_type}"
            print(f"Adding {col_name}...")
            cursor.execute(query)
            conn.commit()
            print(f"  ✓ Added {col_name}")
        except sqlite3.Error as e:
            print(f"  ✗ Error adding {col_name}: {e}")
    else:
        print(f"  ✓ {col_name} already exists")

print("\n=== Checking Departments Table ===\n")

# Check departments table
cursor.execute('PRAGMA table_info(departments)')
dept_cols = cursor.fetchall()
dept_col_names = [col[1] for col in dept_cols]

print(f"Department columns ({len(dept_col_names)}):")
for col in dept_col_names:
    print(f"  - {col}")

# Add gender count columns
gender_cols = {
    'male_count': 'INTEGER DEFAULT 0',
    'female_count': 'INTEGER DEFAULT 0'
}

print(f"\n=== Adding Gender Count Columns ===\n")

for col_name, col_type in gender_cols.items():
    if col_name not in dept_col_names:
        try:
            query = f"ALTER TABLE departments ADD COLUMN {col_name} {col_type}"
            print(f"Adding {col_name}...")
            cursor.execute(query)
            conn.commit()
            print(f"  ✓ Added {col_name}")
        except sqlite3.Error as e:
            print(f"  ✗ Error adding {col_name}: {e}")
    else:
        print(f"  ✓ {col_name} already exists")

conn.close()
print("\n✓ Migration complete!")
