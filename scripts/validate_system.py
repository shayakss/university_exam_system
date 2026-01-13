"""
Core Features Validation Script
Validates that all core data and features are working
"""
from database.db_manager import db

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def validate_database():
    """Validate database structure and data"""
    print_header("DATABASE VALIDATION")
    
    tables = {
        'departments': 'Department data',
        'students': 'Student records',
        'courses': 'Course catalog',
        'marks': 'Student marks',
        'results': 'Generated results',
        'users': 'System users'
    }
    
    all_valid = True
    for table, description in tables.items():
        if db.table_exists(table):
            count = db.get_table_count(table)
            print(f"✓ {description:20} - {count:3} records in '{table}'")
        else:
            print(f"✗ {description:20} - Table '{table}' missing!")
            all_valid = False
    
    return all_valid

def validate_departments():
    """Validate department data"""
    print_header("DEPARTMENTS")
    
    query = "SELECT * FROM departments WHERE is_active = 1"
    depts = db.execute_query(query)
    
    if not depts:
        print("✗ No departments found!")
        return False
    
    print(f"✓ Found {len(depts)} active departments:\n")
    for dept in depts:
        print(f"  [{dept['department_code']:6}] {dept['department_name']}")
    
    return True

def validate_students():
    """Validate student data"""
    print_header("STUDENTS")
    
    query = """
        SELECT s.*, d.department_name, d.department_code
        FROM students s
        JOIN departments d ON s.department_id = d.department_id
        WHERE s.is_active = 1
        ORDER BY s.roll_number
    """
    students = db.execute_query(query)
    
    if not students:
        print("✗ No students found!")
        return False
    
    print(f"✓ Found {len(students)} active students:\n")
    
    # Group by semester
    by_semester = {}
    for s in students:
        sem = s['semester']
        if sem not in by_semester:
            by_semester[sem] = []
        by_semester[sem].append(s)
    
    for sem in sorted(by_semester.keys()):
        print(f"\n  Semester {sem}:")
        for s in by_semester[sem][:5]:  # Show first 5 per semester
            print(f"    {s['roll_number']:12} {s['name']:25} ({s['department_code']})")
        if len(by_semester[sem]) > 5:
            print(f"    ... and {len(by_semester[sem]) - 5} more")
    
    return True

def validate_courses():
    """Validate course data"""
    print_header("COURSES")
    
    query = """
        SELECT c.*, d.department_name, d.department_code
        FROM courses c
        JOIN departments d ON c.department_id = d.department_id
        WHERE c.is_active = 1
        ORDER BY c.semester, c.course_code
    """
    courses = db.execute_query(query)
    
    if not courses:
        print("✗ No courses found!")
        return False
    
    print(f"✓ Found {len(courses)} active courses:\n")
    
    # Group by semester
    by_semester = {}
    for c in courses:
        sem = c['semester']
        if sem not in by_semester:
            by_semester[sem] = []
        by_semester[sem].append(c)
    
    for sem in sorted(by_semester.keys()):
        print(f"\n  Semester {sem}:")
        for c in by_semester[sem]:
            print(f"    {c['course_code']:8} {c['course_name']:30} ({c['credits']} credits, {c['department_code']})")
    
    return True

def validate_marks():
    """Validate marks data"""
    print_header("MARKS & GRADES")
    
    query = """
        SELECT 
            s.roll_number,
            s.name as student_name,
            c.course_code,
            c.course_name,
            m.marks_obtained,
            c.max_marks,
            m.grade,
            m.status
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
        JOIN courses c ON m.course_id = c.course_id
        ORDER BY s.roll_number, c.course_code
    """
    marks = db.execute_query(query)
    
    if not marks:
        print("⚠ No marks entered yet")
        return True  # Not an error, just empty
    
    print(f"✓ Found {len(marks)} marks entries:\n")
    
    # Group by student
    by_student = {}
    for m in marks:
        roll = m['roll_number']
        if roll not in by_student:
            by_student[roll] = []
        by_student[roll].append(m)
    
    for roll in sorted(by_student.keys())[:3]:  # Show first 3 students
        student_marks = by_student[roll]
        print(f"\n  {roll} - {student_marks[0]['student_name']}:")
        for m in student_marks:
            percentage = (m['marks_obtained'] / m['max_marks']) * 100
            print(f"    {m['course_code']:8} {m['marks_obtained']:3}/{m['max_marks']:3} = {percentage:5.1f}% ({m['grade']}) - {m['status']}")
    
    if len(by_student) > 3:
        print(f"\n  ... and {len(by_student) - 3} more students with marks")
    
    return True

def validate_results():
    """Validate generated results"""
    print_header("GENERATED RESULTS")
    
    query = """
        SELECT 
            s.roll_number,
            s.name,
            r.semester,
            r.cgpa,
            r.sgpa,
            r.percentage,
            r.overall_grade,
            r.status
        FROM results r
        JOIN students s ON r.student_id = s.student_id
        ORDER BY r.cgpa DESC
    """
    results = db.execute_query(query)
    
    if not results:
        print("⚠ No results generated yet")
        return True  # Not an error
    
    print(f"✓ Found {len(results)} generated results:\n")
    
    for r in results[:5]:  # Show top 5
        print(f"  {r['roll_number']:12} {r['name']:25} Sem {r['semester']}: CGPA {r['cgpa']:.2f}, {r['percentage']:.1f}% ({r['overall_grade']}) - {r['status']}")
    
    if len(results) > 5:
        print(f"\n  ... and {len(results) - 5} more results")
    
    return True

def validate_users():
    """Validate user accounts"""
    print_header("USER ACCOUNTS")
    
    query = "SELECT username, full_name, role FROM users WHERE is_active = 1"
    users = db.execute_query(query)
    
    if not users:
        print("✗ No users found!")
        return False
    
    print(f"✓ Found {len(users)} active users:\n")
    
    # Group by role
    by_role = {}
    for u in users:
        role = u['role']
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(u)
    
    for role in sorted(by_role.keys()):
        print(f"\n  {role}:")
        for u in by_role[role]:
            print(f"    {u['username']:15} - {u['full_name']}")
    
    return True

def run_validation():
    """Run all validations"""
    print("\n" + "="*70)
    print("  UNIVERSITY EXAM SYSTEM - CORE FEATURES VALIDATION")
    print("="*70)
    
    results = {
        "Database Structure": validate_database(),
        "Departments": validate_departments(),
        "Students": validate_students(),
        "Courses": validate_courses(),
        "Marks & Grades": validate_marks(),
        "Results": validate_results(),
        "User Accounts": validate_users()
    }
    
    # Summary
    print_header("VALIDATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  TOTAL: {passed}/{total} validations passed ({passed/total*100:.1f}%)")
    print(f"{'='*70}")
    
    if passed == total:
        print("\n🎉 All core features validated successfully!")
        print("\nNext steps:")
        print("  1. Run the application: python main.py")
        print("  2. Login with: admin / admin123")
        print("  3. Test features in the UI")
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_validation()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
