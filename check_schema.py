"""
Check Users Table Schema
"""
import sqlite3

db_path = r"d:\New folder\New folder (2)\university_exam_system\Release\exam_system.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Users Table Columns ===")
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
for col in columns:
    print(col)

conn.close()
