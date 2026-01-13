"""
Check Users Table Schema Clean
"""
import sqlite3

db_path = r"d:\New folder\New folder (2)\university_exam_system\Release\exam_system.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
print("Columns found:")
for col in columns:
    print(f"- {col[1]}")

conn.close()
