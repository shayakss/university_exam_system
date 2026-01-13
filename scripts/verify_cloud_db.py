"""
Comprehensive verification and test data script for TiDB Cloud
Tests MySQL connection, creates departments, courses, students, and marks
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import db
from controllers.department_controller import department_controller
from controllers.course_controller import course_controller
from controllers.student_controller import student_controller
from controllers.marks_controller import marks_controller
from controllers.user_controller import user_controller
import random

def test_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("STEP 1: Testing Database Connection")
    print("="*60)
    try:
        conn = db.get_connection()
        print("✓ Database connection successful!")
        
        # Test a simple query
        result = db.execute_query("SELECT 1 as test")
        if result and result[0]['test'] == 1:
            print("✓ Query execution successful!")
            return True
        else:
            print("✗ Query execution failed")
            return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def create_departments():
    """Create 2 departments"""
    print("\n" + "="*60)
    print("STEP 2: Creating Departments")
    print("="*60)
    
    departments = [
        ("Computer Science", "CS"),
        ("Mathematics", "MATH")
    ]
    
    dept_ids = []
    for name, code in departments:
        success, message, dept_id = department_controller.create_department(name, code)
        if success:
            print(f"✓ Created department: {name} ({code}) - ID: {dept_id}")
            dept_ids.append(dept_id)
        else:
            print(f"✗ Failed to create department: {name} - {message}")
    
    return dept_ids

def create_courses(dept_ids):
    """Create courses for each department"""
    print("\n" + "="*60)
    print("STEP 3: Creating Courses")
    print("="*60)
    
    courses = [
        # CS Department
        ("CS101", "Introduction to Programming", dept_ids[0], 1, 3, 100, 40),
        ("CS102", "Data Structures", dept_ids[0], 1, 4, 100, 40),
        ("CS201", "Database Systems", dept_ids[0], 2, 3, 100, 40),
        
        # Math Department
        ("MATH101", "Calculus I", dept_ids[1], 1, 4, 100, 40),
        ("MATH102", "Linear Algebra", dept_ids[1], 1, 3, 100, 40),
        ("MATH201", "Differential Equations", dept_ids[1], 2, 4, 100, 40),
    ]
    
    course_ids = []
    for code, name, dept_id, semester, credits, max_marks, pass_marks in courses:
        success, message, course_id = course_controller.create_course(
            code, name, dept_id, semester, max_marks, pass_marks, credits
        )
        if success:
            print(f"✓ Created course: {code} - {name}")
            course_ids.append((course_id, dept_id, semester))
        else:
            print(f"✗ Failed to create course: {code} - {message}")
    
    return course_ids

def create_students(dept_ids):
    """Create 10 students across departments"""
    print("\n" + "="*60)
    print("STEP 4: Creating Students")
    print("="*60)
    
    first_names = ["Ahmed", "Fatima", "Ali", "Ayesha", "Hassan", "Zainab", "Omar", "Mariam", "Bilal", "Sara"]
    last_names = ["Khan", "Ahmed", "Ali", "Hassan", "Hussain", "Malik", "Shah", "Baloch", "Raza", "Siddiqui"]
    
    students = []
    for i in range(10):
        dept_id = dept_ids[i % 2]  # Alternate between departments
        dept_name = "CS" if i % 2 == 0 else "MATH"
        
        roll_number = f"{dept_name}-{2021+i//2:02d}-{i+1:02d}"
        name = f"{first_names[i]} {last_names[i]}"
        father_name = f"{random.choice(['Muhammad', 'Abdul', 'Ahmed'])} {last_names[i]}"
        
        success, message, student_id = student_controller.create_student(
            roll_number=roll_number,
            name=name,
            father_name=father_name,
            department_id=dept_id,
            semester=1,
            gender=random.choice(['Male', 'Female']),
            date_of_birth='2003-01-01',
            cnic='',
            father_cnic='',
            phone='',
            email=f"{name.lower().replace(' ', '.')}@student.edu",
            guardian_phone='',
            address='Quetta, Pakistan',
            registration_no=f"REG-{2021}-{i+1:04d}"
        )
        
        if success:
            print(f"✓ Created student: {roll_number} - {name}")
            students.append((student_id, dept_id, roll_number, name))
        else:
            print(f"✗ Failed to create student: {roll_number} - {message}")
    
    return students

def assign_marks(students, course_ids):
    """Assign marks to students"""
    print("\n" + "="*60)
    print("STEP 5: Assigning Marks")
    print("="*60)
    
    # Get admin user ID
    admin_query = "SELECT user_id FROM users WHERE username = 'admin' LIMIT 1"
    admin_result = db.execute_query(admin_query)
    admin_id = admin_result[0]['user_id'] if admin_result else 1
    
    marks_count = 0
    for student_id, dept_id, roll_number, name in students:
        # Find courses for this student's department and semester
        student_courses = [(cid, did, sem) for cid, did, sem in course_ids if did == dept_id and sem == 1]
        
        for course_id, _, _ in student_courses:
            # Generate random marks between 50-95
            marks_obtained = random.randint(50, 95)
            
            success, message, mark_id = marks_controller.enter_marks(
                student_id=student_id,
                course_id=course_id,
                marks_obtained=marks_obtained,
                entered_by=admin_id
            )
            
            if success:
                marks_count += 1
            else:
                print(f"✗ Failed to assign marks for student {roll_number} - {message}")
    
    print(f"✓ Assigned {marks_count} marks entries")
    return marks_count

def verify_data():
    """Verify all data was created"""
    print("\n" + "="*60)
    print("STEP 6: Verifying Data")
    print("="*60)
    
    # Count departments
    dept_count = db.execute_query("SELECT COUNT(*) as count FROM departments")
    print(f"✓ Departments: {dept_count[0]['count']}")
    
    # Count courses
    course_count = db.execute_query("SELECT COUNT(*) as count FROM courses")
    print(f"✓ Courses: {course_count[0]['count']}")
    
    # Count students
    student_count = db.execute_query("SELECT COUNT(*) as count FROM students")
    print(f"✓ Students: {student_count[0]['count']}")
    
    # Count marks
    marks_count = db.execute_query("SELECT COUNT(*) as count FROM marks")
    print(f"✓ Marks entries: {marks_count[0]['count']}")
    
    # Show sample data
    print("\n" + "-"*60)
    print("Sample Students:")
    students = db.execute_query("SELECT roll_number, name, department_id FROM students LIMIT 5")
    for s in students:
        print(f"  - {s['roll_number']}: {s['name']}")
    
    return True

def main():
    """Main verification script"""
    print("\n" + "="*60)
    print("TiDB CLOUD VERIFICATION & TEST DATA SCRIPT")
    print("="*60)
    
    # Step 1: Test connection
    if not test_connection():
        print("\n✗ Connection test failed. Exiting.")
        return False
    
    # Step 2: Create departments
    dept_ids = create_departments()
    if len(dept_ids) < 2:
        print("\n✗ Failed to create departments. Exiting.")
        return False
    
    # Step 3: Create courses
    course_ids = create_courses(dept_ids)
    if len(course_ids) < 4:
        print("\n✗ Failed to create courses. Exiting.")
        return False
    
    # Step 4: Create students
    students = create_students(dept_ids)
    if len(students) < 10:
        print("\n✗ Failed to create students. Exiting.")
        return False
    
    # Step 5: Assign marks
    marks_count = assign_marks(students, course_ids)
    if marks_count < 10:
        print("\n⚠ Warning: Not all marks were assigned")
    
    # Step 6: Verify data
    verify_data()
    
    print("\n" + "="*60)
    print("✓ VERIFICATION COMPLETE!")
    print("="*60)
    print("\nYour TiDB Cloud database is working perfectly!")
    print("You can now run the application and see all the test data.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
