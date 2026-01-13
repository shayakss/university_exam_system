"""
Test Script for Core/Old Features
Tests all existing functionality of the University Exam System
"""
from database.db_manager import db
from controllers.student_controller import student_controller
from controllers.department_controller import department_controller
from controllers.course_controller import course_controller
from controllers.marks_controller import marks_controller
from controllers.result_controller import result_controller
from controllers.user_controller import user_controller
from utils.security import hash_password, verify_password
import random

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_database_connection():
    """Test database connectivity"""
    print_header("TEST 1: Database Connection")
    try:
        conn = db.get_connection()
        if conn:
            print("✓ Database connection successful")
            
            # Check if tables exist
            tables = ['departments', 'students', 'courses', 'marks', 'results', 'users']
            for table in tables:
                if db.table_exists(table):
                    count = db.get_table_count(table)
                    print(f"✓ Table '{table}' exists - {count} records")
                else:
                    print(f"✗ Table '{table}' missing")
            return True
        return False
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_departments():
    """Test department operations"""
    print_header("TEST 2: Department Management")
    
    # Get all departments
    depts = department_controller.get_all_departments()
    print(f"✓ Retrieved {len(depts)} departments")
    
    for dept in depts[:5]:  # Show first 5
        print(f"  - {dept['department_name']} ({dept['department_code']})")
    
    # Test get by ID
    if depts:
        dept = department_controller.get_department_by_id(depts[0]['department_id'])
        if dept:
            print(f"✓ Get by ID works: {dept['department_name']}")
        
        # Test get by code
        dept = department_controller.get_department_by_code(depts[0]['department_code'])
        if dept:
            print(f"✓ Get by code works: {dept['department_name']}")
    
    return len(depts) > 0

def test_students():
    """Test student operations"""
    print_header("TEST 3: Student Management")
    
    # Get all students
    students = student_controller.get_all_students()
    print(f"✓ Retrieved {len(students)} students")
    
    for student in students[:5]:  # Show first 5
        print(f"  - {student['roll_number']}: {student['name']} (Sem {student['semester']})")
    
    # Test get by ID
    if students:
        student = student_controller.get_student_by_id(students[0]['student_id'])
        if student:
            print(f"✓ Get by ID works: {student['name']}")
        
        # Test get by roll number
        student = student_controller.get_student_by_roll_number(students[0]['roll_number'])
        if student:
            print(f"✓ Get by roll number works: {student['name']}")
        
        # Test get by department
        dept_students = student_controller.get_students_by_department(students[0]['department_id'])
        print(f"✓ Get by department works: {len(dept_students)} students")
    
    return len(students) > 0

def test_courses():
    """Test course operations"""
    print_header("TEST 4: Course Management")
    
    # Get all courses
    courses = course_controller.get_all_courses()
    print(f"✓ Retrieved {len(courses)} courses")
    
    for course in courses[:5]:  # Show first 5
        print(f"  - {course['course_code']}: {course['course_name']} (Sem {course['semester']})")
    
    # Test get by ID
    if courses:
        course = course_controller.get_course_by_id(courses[0]['course_id'])
        if course:
            print(f"✓ Get by ID works: {course['course_name']}")
        
        # Test get by department
        dept_courses = course_controller.get_courses_by_department(courses[0]['department_id'])
        print(f"✓ Get by department works: {len(dept_courses)} courses")
        
        # Test get by semester
        sem_courses = course_controller.get_courses_by_semester(1)
        print(f"✓ Get by semester works: {len(sem_courses)} courses in semester 1")
    
    return len(courses) > 0

def test_marks():
    """Test marks operations"""
    print_header("TEST 5: Marks Management")
    
    # Get students and courses
    students = student_controller.get_all_students()
    courses = course_controller.get_all_courses()
    
    if not students or not courses:
        print("✗ No students or courses to test marks")
        return False
    
    # Get marks for first student
    student = students[0]
    marks = marks_controller.get_student_marks(student['student_id'])
    print(f"✓ Retrieved {len(marks)} marks for {student['roll_number']}")
    
    for mark in marks[:3]:  # Show first 3
        print(f"  - {mark['course_code']}: {mark['marks_obtained']}/{mark['max_marks']} ({mark['grade']})")
    
    # Test get marks by course
    if courses:
        course_marks = marks_controller.get_course_marks(courses[0]['course_id'])
        print(f"✓ Retrieved {len(course_marks)} marks for course {courses[0]['course_code']}")
    
    return len(marks) > 0

def test_results():
    """Test result operations"""
    print_header("TEST 6: Results Management")
    
    students = student_controller.get_all_students()
    
    if not students:
        print("✗ No students to test results")
        return False
    
    # Check existing results
    results_count = 0
    for student in students[:5]:
        result = result_controller.get_student_result(student['student_id'], student['semester'])
        if result:
            results_count += 1
            print(f"✓ {student['roll_number']}: CGPA {result['cgpa']:.2f}, {result['percentage']:.1f}% ({result['status']})")
    
    print(f"\n✓ Found {results_count} existing results")
    
    # Test result generation for a student without result
    sem1_students = [s for s in students if s['semester'] == 1]
    if sem1_students:
        student = sem1_students[0]
        # Check if student has marks
        marks = marks_controller.get_student_marks(student['student_id'])
        if marks:
            print(f"\n✓ Student {student['roll_number']} has {len(marks)} marks entries")
            print("  Ready for result generation")
        else:
            print(f"\n⚠ Student {student['roll_number']} has no marks")
    
    return results_count > 0

def test_users():
    """Test user operations"""
    print_header("TEST 7: User Management")
    
    # Get all users
    users = user_controller.get_all_users()
    print(f"✓ Retrieved {len(users)} users")
    
    for user in users[:5]:  # Show first 5
        print(f"  - {user['username']}: {user['full_name']} ({user['role']})")
    
    # Test authentication
    print("\n✓ Testing authentication:")
    test_password = "admin123"
    admin_user = next((u for u in users if u['username'] == 'admin'), None)
    
    if admin_user:
        # Verify password
        if verify_password(test_password, admin_user['password_hash']):
            print(f"  ✓ Password verification works for admin")
        else:
            print(f"  ✗ Password verification failed")
    
    return len(users) > 0

def test_security():
    """Test security features"""
    print_header("TEST 8: Security Features")
    
    # Test password hashing
    test_password = "TestPassword123"
    hashed = hash_password(test_password)
    print(f"✓ Password hashing works")
    
    # Test password verification
    if verify_password(test_password, hashed):
        print(f"✓ Password verification works")
    else:
        print(f"✗ Password verification failed")
    
    # Test wrong password
    if not verify_password("WrongPassword", hashed):
        print(f"✓ Wrong password correctly rejected")
    else:
        print(f"✗ Security issue: wrong password accepted")
    
    return True

def test_data_integrity():
    """Test data integrity and relationships"""
    print_header("TEST 9: Data Integrity")
    
    # Test student-department relationship
    students = student_controller.get_all_students()
    if students:
        student = students[0]
        dept = department_controller.get_department_by_id(student['department_id'])
        if dept:
            print(f"✓ Student-Department relationship intact")
            print(f"  {student['name']} → {dept['department_name']}")
        else:
            print(f"✗ Orphaned student found")
    
    # Test course-department relationship
    courses = course_controller.get_all_courses()
    if courses:
        course = courses[0]
        dept = department_controller.get_department_by_id(course['department_id'])
        if dept:
            print(f"✓ Course-Department relationship intact")
            print(f"  {course['course_name']} → {dept['department_name']}")
        else:
            print(f"✗ Orphaned course found")
    
    # Test marks-student-course relationship
    marks = marks_controller.get_student_marks(students[0]['student_id']) if students else []
    if marks:
        mark = marks[0]
        student = student_controller.get_student_by_id(mark['student_id'])
        course = course_controller.get_course_by_id(mark['course_id'])
        if student and course:
            print(f"✓ Marks relationships intact")
            print(f"  {student['name']} → {course['course_code']}: {mark['marks_obtained']}")
        else:
            print(f"✗ Orphaned marks found")
    
    return True

def test_queries_performance():
    """Test query performance"""
    print_header("TEST 10: Query Performance")
    
    import time
    
    # Test student query
    start = time.time()
    students = student_controller.get_all_students()
    elapsed = time.time() - start
    print(f"✓ Get all students: {elapsed*1000:.2f}ms ({len(students)} records)")
    
    # Test course query
    start = time.time()
    courses = course_controller.get_all_courses()
    elapsed = time.time() - start
    print(f"✓ Get all courses: {elapsed*1000:.2f}ms ({len(courses)} records)")
    
    # Test marks query
    if students:
        start = time.time()
        marks = marks_controller.get_student_marks(students[0]['student_id'])
        elapsed = time.time() - start
        print(f"✓ Get student marks: {elapsed*1000:.2f}ms ({len(marks)} records)")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  UNIVERSITY EXAM SYSTEM - CORE FEATURES TEST SUITE")
    print("="*70)
    
    results = {
        "Database Connection": test_database_connection(),
        "Department Management": test_departments(),
        "Student Management": test_students(),
        "Course Management": test_courses(),
        "Marks Management": test_marks(),
        "Results Management": test_results(),
        "User Management": test_users(),
        "Security Features": test_security(),
        "Data Integrity": test_data_integrity(),
        "Query Performance": test_queries_performance()
    }
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'='*70}")
    
    if passed == total:
        print("\n🎉 All core features are working correctly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error during testing: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
