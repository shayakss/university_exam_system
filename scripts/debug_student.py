"""
Debug student creation
"""
from database.db_manager import db
from controllers.student_controller import student_controller
import traceback

print("=== Testing Student Creation ===\n")

try:
    # Get a department
    depts = db.execute_query("SELECT * FROM departments LIMIT 1")
    if not depts:
        print("ERROR: No departments found")
    else:
        dept_id = depts[0]['department_id']
        print(f"Department ID: {dept_id}")
        print(f"Department: {depts[0]['department_name']}\n")
        
        # Try to create with minimal data
        print("Attempting to create student...")
        success, msg, student_id = student_controller.create_student(
            roll_number="TEST123",
            name="Test Student",
            department_id=dept_id,
            semester=1,
            gender="Male",
            date_of_birth="2000-01-01"
        )
        
        print(f"\nResult:")
        print(f"  Success: {success}")
        print(f"  Message: {msg}")
        print(f"  Student ID: {student_id}")
        
        if success:
            print("\n✓ SUCCESS! Cleaning up...")
            db.execute_update("DELETE FROM students WHERE roll_number = 'TEST123'")
        else:
            print(f"\n✗ FAILED: {msg}")
            
except Exception as e:
    print(f"\n✗ EXCEPTION: {e}")
    traceback.print_exc()
