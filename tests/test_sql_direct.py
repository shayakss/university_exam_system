"""
Direct SQL test
"""
import sqlite3

conn = sqlite3.connect('exam_system.db')
cursor = conn.cursor()

print("=== Testing Direct SQL Insert ===\n")

try:
    # Get a department
    cursor.execute("SELECT * FROM departments LIMIT 1")
    dept = cursor.fetchone()
    
    if not dept:
        print("No departments found")
    else:
        print(f"Department ID: {dept[0]}")
        
        # Try direct insert
        query = """
            INSERT INTO students (roll_number, name, department_id, semester, gender, 
                                date_of_birth, email, phone, address, registration_no,
                                cnic, father_name, father_cnic, guardian_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        print("Executing INSERT...")
        cursor.execute(query, (
            'TEST999', 'Test Student', dept[0], 1, 'Male',
            '2000-01-01', None, None, None, None,
            None, None, None, None
        ))
        conn.commit()
        
        print(f"✓ Insert successful! Row ID: {cursor.lastrowid}")
        
        # Clean up
        cursor.execute("DELETE FROM students WHERE roll_number = 'TEST999'")
        conn.commit()
        print("✓ Cleanup done")
        
except sqlite3.Error as e:
    print(f"✗ SQL Error: {e}")
    conn.rollback()
finally:
    conn.close()
