"""
Test student creation with detailed error output
"""
import sys
import traceback
from database.db_manager import db
from controllers.student_controller import student_controller

print("=== Testing Student Creation ===\n")

try:
    # Get a department to use
    depts = db.execute_query("SELECT * FROM departments LIMIT 1")
    if not depts:
        print("ERROR: No departments found. Please add a department first.")
        sys.exit(1)
    
    dept_id = depts[0]['department_id']
    print(f"Using department ID: {dept_id}\n")
    
    # Try to create a test student
    print("Creating test student...")
    success, msg, student_id = student_controller.create_student(
        roll_number="TEST001",
        name="Test Student",
        department_id=dept_id,
        semester=1,
        gender="Male",
        date_of_birth="2000-01-01",
        email="test@test.com",
        phone="1234567890",
        address="Test Address",
        registration_no="REG001",
        cnic="12345-1234567-1",
        father_name="Test Father",
        father_cnic="12345-1234567-2",
        guardian_phone="0987654321"
    )

    print(f"\nResult:")
    print(f"  Success: {success}")
    print(f"  Message: {msg}")
    print(f"  Student ID: {student_id}")

    # Clean up
    if success:
        db.execute_update("DELETE FROM students WHERE roll_number = 'TEST001'")
        print("\n✓ Test student created and deleted successfully!")
    else:
        print(f"\n✗ Failed to create student: {msg}")

except Exception as e:
    print(f"\n✗ EXCEPTION: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
