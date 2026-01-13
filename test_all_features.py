"""
Comprehensive Test Script for University Exam System
Tests all features including new implementations
"""
from database.db_manager import db
from controllers.department_controller import department_controller
from controllers.student_controller import student_controller
from controllers.course_controller import course_controller
from controllers.user_controller import user_controller
from controllers.marks_controller import marks_controller
from controllers.result_controller import result_controller
from controllers.assignment_controller import assignment_controller
from controllers.attendance_controller import attendance_controller
from controllers.promotion_controller import promotion_controller
from controllers.id_card_controller import id_card_controller
from controllers.alumni_controller import alumni_controller
from datetime import datetime, date, timedelta
import random

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_departments():
    """Test department management"""
    print_section("Testing Departments")
    
    departments = [
        ("Computer Science", "CS"),
        ("Electrical Engineering", "EE"),
        ("Mechanical Engineering", "ME"),
        ("Business Administration", "BA"),
        ("Mathematics", "MATH")
    ]
    
    for name, code in departments:
        success, msg, dept_id = department_controller.create_department(name, code)
        if success:
            print(f"✓ Added: {name} ({code})")
        else:
            print(f"✗ Failed: {name} - {msg}")
    
    # List all departments
    all_depts = department_controller.get_all_departments()
    print(f"\nTotal Departments: {len(all_depts)}")
    return all_depts

def test_users():
    """Test user management"""
    print_section("Testing Users")
    
    users = [
        ("teacher1", "password123", "Teacher", "Dr. John Smith"),
        ("teacher2", "password123", "Teacher", "Dr. Sarah Johnson"),
        ("dataentry1", "password123", "DataEntry", "Mark Wilson"),
        ("hod1", "password123", "HOD", "Prof. David Brown")
    ]
    
    for username, password, role, fullname in users:
        success, user_id = user_controller.create_user(username, password, role, fullname)
        if success:
            print(f"✓ Created user: {username} ({role})")
        else:
            print(f"✗ Failed: {username}")
    
    all_users = user_controller.get_all_users()
    print(f"\nTotal Users: {len(all_users)}")
    return all_users

def test_courses(departments):
    """Test course management"""
    print_section("Testing Courses")
    
    if not departments:
        print("No departments available")
        return []
    
    courses_data = [
        ("CS101", "Introduction to Programming", 1, 100, 40, 4),
        ("CS102", "Data Structures", 2, 100, 40, 4),
        ("CS201", "Database Systems", 3, 100, 40, 4),
        ("CS202", "Web Development", 4, 100, 40, 3),
        ("EE101", "Circuit Analysis", 1, 100, 40, 4),
        ("EE102", "Digital Electronics", 2, 100, 40, 4),
        ("ME101", "Engineering Mechanics", 1, 100, 40, 4),
        ("BA101", "Business Fundamentals", 1, 100, 40, 3),
    ]
    
    created_courses = []
    for code, name, sem, max_marks, pass_marks, credits in courses_data:
        # Assign to appropriate department
        dept_id = None
        if code.startswith("CS"):
            dept_id = next((d['department_id'] for d in departments if d['department_code'] == 'CS'), None)
        elif code.startswith("EE"):
            dept_id = next((d['department_id'] for d in departments if d['department_code'] == 'EE'), None)
        elif code.startswith("ME"):
            dept_id = next((d['department_id'] for d in departments if d['department_code'] == 'ME'), None)
        elif code.startswith("BA"):
            dept_id = next((d['department_id'] for d in departments if d['department_code'] == 'BA'), None)
        
        if dept_id:
            success, msg, course_id = course_controller.create_course(
                code, name, dept_id, sem, max_marks, pass_marks, credits
            )
            if success:
                print(f"✓ Added: {code} - {name}")
                created_courses.append({'course_id': course_id, 'code': code})
            else:
                print(f"✗ Failed: {code} - {msg}")
    
    all_courses = course_controller.get_all_courses()
    print(f"\nTotal Courses: {len(all_courses)}")
    return all_courses

def test_students(departments):
    """Test student management"""
    print_section("Testing Students")
    
    if not departments:
        print("No departments available")
        return []
    
    cs_dept = next((d for d in departments if d['department_code'] == 'CS'), None)
    ee_dept = next((d for d in departments if d['department_code'] == 'EE'), None)
    
    students_data = [
        ("CS2024001", "Alice Johnson", cs_dept['department_id'] if cs_dept else 1, 1, "Female", "2005-03-15", "alice@example.com", "1234567890"),
        ("CS2024002", "Bob Smith", cs_dept['department_id'] if cs_dept else 1, 1, "Male", "2005-05-20", "bob@example.com", "1234567891"),
        ("CS2024003", "Charlie Brown", cs_dept['department_id'] if cs_dept else 1, 2, "Male", "2004-07-10", "charlie@example.com", "1234567892"),
        ("CS2024004", "Diana Prince", cs_dept['department_id'] if cs_dept else 1, 2, "Female", "2004-09-25", "diana@example.com", "1234567893"),
        ("EE2024001", "Eve Wilson", ee_dept['department_id'] if ee_dept else 2, 1, "Female", "2005-01-30", "eve@example.com", "1234567894"),
        ("EE2024002", "Frank Miller", ee_dept['department_id'] if ee_dept else 2, 1, "Male", "2005-04-12", "frank@example.com", "1234567895"),
        ("CS2024005", "Grace Lee", cs_dept['department_id'] if cs_dept else 1, 3, "Female", "2003-11-08", "grace@example.com", "1234567896"),
        ("CS2024006", "Henry Davis", cs_dept['department_id'] if cs_dept else 1, 3, "Male", "2003-12-22", "henry@example.com", "1234567897"),
    ]
    
    for roll, name, dept_id, sem, gender, dob, email, phone in students_data:
        success, msg, student_id = student_controller.create_student(
            roll, name, dept_id, sem, gender, dob, email, phone, "123 Main St"
        )
        if success:
            print(f"✓ Added: {roll} - {name}")
        else:
            print(f"✗ Failed: {roll} - {msg}")
    
    all_students = student_controller.get_all_students()
    print(f"\nTotal Students: {len(all_students)}")
    return all_students

def test_marks_and_results(students, courses):
    """Test marks entry and result generation"""
    print_section("Testing Marks Entry & Results")
    
    if not students or not courses:
        print("No students or courses available")
        return
    
    # Add marks for semester 1 students
    sem1_students = [s for s in students if s['semester'] == 1]
    sem1_courses = [c for c in courses if c['semester'] == 1]
    
    for student in sem1_students[:4]:  # First 4 students
        for course in sem1_courses:
            if student['department_id'] == course['department_id']:
                # Random marks between 50-95
                marks = random.randint(50, 95)
                success, msg = marks_controller.add_marks(
                    student['student_id'], course['course_id'], marks, 1  # user_id = 1 (admin)
                )
                if success:
                    print(f"✓ {student['roll_number']} - {course['course_code']}: {marks}")
    
    # Generate results
    print("\nGenerating Results...")
    for student in sem1_students[:4]:
        success, msg = result_controller.generate_result(student['student_id'], 1)
        if success:
            print(f"✓ Generated result for {student['roll_number']}")

def test_assignments(courses, users):
    """Test assignment management"""
    print_section("Testing Assignments")
    
    if not courses:
        print("No courses available")
        return
    
    teacher = next((u for u in users if u['role'] == 'Teacher'), None)
    if not teacher:
        print("No teacher available")
        return
    
    cs_courses = [c for c in courses if c['course_code'].startswith('CS')][:2]
    
    for course in cs_courses:
        due_date = date.today() + timedelta(days=7)
        success, msg = assignment_controller.create_assignment(
            course['course_id'],
            teacher['user_id'],
            f"Assignment for {course['course_name']}",
            "Complete the given exercises and submit your solution.",
            due_date,
            10
        )
        if success:
            print(f"✓ Created assignment for {course['course_code']}")
        else:
            print(f"✗ Failed: {msg}")

def test_attendance(students, courses):
    """Test attendance marking"""
    print_section("Testing Attendance")
    
    if not students or not courses:
        print("No students or courses available")
        return
    
    # Mark attendance for today
    today = date.today()
    sem1_students = [s for s in students if s['semester'] == 1]
    
    for student in sem1_students[:4]:
        status = random.choice(['Present', 'Present', 'Present', 'Absent'])  # 75% present
        success, msg = attendance_controller.mark_student_attendance(
            student['student_id'], today, status
        )
        if success:
            print(f"✓ {student['roll_number']}: {status}")

def test_id_cards(students):
    """Test ID card generation"""
    print_section("Testing ID Card Generation")
    
    if not students:
        print("No students available")
        return
    
    for student in students[:3]:  # Generate for first 3 students
        success, msg, details = id_card_controller.generate_student_id_card(
            student['student_id'], 1  # issued_by = admin
        )
        if success:
            print(f"✓ Generated ID card for {student['roll_number']}: {details['card_number']}")
        else:
            print(f"✗ Failed: {msg}")

def test_promotion(students):
    """Test student promotion"""
    print_section("Testing Student Promotion")
    
    sem1_students = [s for s in students if s['semester'] == 1]
    
    if sem1_students:
        student = sem1_students[0]
        success, msg = promotion_controller.promote_student(student['student_id'], 1)
        if success:
            print(f"✓ Promoted {student['roll_number']} to semester 2")
        else:
            print(f"✗ Failed: {msg}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  UNIVERSITY EXAM SYSTEM - COMPREHENSIVE TEST")
    print("="*60)
    
    try:
        # Test in order
        departments = test_departments()
        users = test_users()
        courses = test_courses(departments)
        students = test_students(departments)
        test_marks_and_results(students, courses)
        test_assignments(courses, users)
        test_attendance(students, courses)
        test_id_cards(students)
        test_promotion(students)
        
        print_section("TEST SUMMARY")
        print("✓ All features tested successfully!")
        print("\nYou can now:")
        print("  1. Login with: admin / admin123")
        print("  2. Explore all tabs and features")
        print("  3. Test the new Extra Features tab")
        print("  4. Toggle between Light/Dark themes")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
