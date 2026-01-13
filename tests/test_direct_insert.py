from database.db_manager import db

# Direct database insert test
print("=== Direct Database Insert Test ===\n")

try:
    # Get a department
    depts = db.execute_query("SELECT * FROM departments LIMIT 1")
    if not depts:
        print("No departments found")
    else:
        dept_id = depts[0]['department_id']
        print(f"Department ID: {dept_id}")
        
        # Try direct insert
        query = """
            INSERT INTO students (roll_number, name, department_id, semester, gender, 
                                date_of_birth, email, phone, address, registration_no,
                                cnic, father_name, father_cnic, guardian_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        success, student_id = db.execute_update(
            query,
            ('TEST002', 'Test Student 2', dept_id, 1, 'Male',
             '2000-01-01', 'test@test.com', '1234567890', 'Test Address', 'REG002',
             '12345-1234567-1', 'Test Father', '12345-1234567-2', '0987654321')
        )
        
        print(f"\nDirect insert result:")
        print(f"  Success: {success}")
        print(f"  Student ID: {student_id}")
        
        if success:
            # Verify it was inserted
            result = db.execute_query("SELECT * FROM students WHERE roll_number = 'TEST002'")
            if result:
                print(f"\n✓ Student found in database!")
                print(f"  Name: {result[0]['name']}")
                print(f"  Registration: {result[0].get('registration_no', 'N/A')}")
                
                # Clean up
                db.execute_update("DELETE FROM students WHERE roll_number = 'TEST002'")
                print("\n✓ Test student deleted")
            else:
                print("\n✗ Student not found after insert")
        else:
            print("\n✗ Insert failed")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
