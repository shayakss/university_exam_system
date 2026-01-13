import sqlite3

conn = sqlite3.connect('exam_system.db')
cursor = conn.cursor()

# Get table info
cursor.execute('PRAGMA table_info(students)')
columns = cursor.fetchall()

print("=== STUDENTS TABLE COLUMNS ===")
for col in columns:
    print(f"Column {col[0]}: {col[1]} ({col[2]})")

print(f"\nTotal columns: {len(columns)}")

# Check if new columns exist
new_columns = ['registration_no', 'cnic', 'father_name', 'father_cnic', 'guardian_phone']
existing_cols = [col[1] for col in columns]

print("\n=== NEW COLUMNS CHECK ===")
for new_col in new_columns:
    status = "✓ EXISTS" if new_col in existing_cols else "✗ MISSING"
    print(f"{new_col:20} {status}")

conn.close()
