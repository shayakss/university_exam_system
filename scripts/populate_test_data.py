"""
Simple Test Data Populator for University Exam System
Adds sample data directly to database
"""
from database.db_manager import db
from utils.security import hash_password
from datetime import date, timedelta
import random

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def add_sample_data():
    """Add sample data to database"""
    
    try:
        # 1. Add Departments
        print_section("Adding Departments")
        departments = [
            ("Computer Science", "CS"),
            ("Electrical Engineering", "EE"),
            ("Mechanical Engineering", "ME"),
            ("Business Administration", "BA")
        ]
        
        for name, code in departments:
            query = "INSERT OR IGNORE INTO departments (department_name, department_code) VALUES (?, ?)"
            success, dept_id = db.execute_update(query, (name, code))
            if success:
                print(f"✓ {name} ({code})")
        
        # Get department IDs
        depts = db.execute_query("SELECT * FROM departments")
        dept_dict = {d['department_code']: d['department_id'] for d in depts}
        
        # 2. Add Courses
        print_section("Adding Courses")
        courses = [
            ("CS101", "Intro to Programming", dept_dict.get('CS', 1), 1, 100, 40, 4),
            ("CS102", "Data Structures", dept_dict.get('CS', 1), 2, 100, 40, 4),
            ("CS201", "Database Systems", dept_dict.get('CS', 1), 3, 100, 40, 4),
            ("EE101", "Circuit Analysis", dept_dict.get('EE', 2), 1, 100, 40, 4),
            ("EE102", "Digital Electronics", dept_dict.get('EE', 2), 2, 100, 40, 4),
            ("ME101", "Engineering Mechanics", dept_dict.get('ME', 3), 1, 100, 40, 4),
        ]
        
        for code, name, dept_id, sem, max_m, pass_m, credits in courses:
            query = """INSERT OR IGNORE INTO courses 
                       (course_code, course_name, department_id, semester, max_marks, pass_marks, credits)
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            success, _ = db.execute_update(query, (code, name, dept_id, sem, max_m, pass_m, credits))
            if success:
                print(f"✓ {code} - {name}")
        
        # 3. Add Students
        print_section("Adding Students")
        students = [
            ("CS2024001", "Alice Johnson", dept_dict.get('CS', 1), 1, "Female", "2005-03-15", "alice@test.com", "1111111111"),
            ("CS2024002", "Bob Smith", dept_dict.get('CS', 1), 1, "Male", "2005-05-20", "bob@test.com", "1111111112"),
            ("CS2024003", "Charlie Brown", dept_dict.get('CS', 1), 2, "Male", "2004-07-10", "charlie@test.com", "1111111113"),
            ("CS2024004", "Diana Prince", dept_dict.get('CS', 1), 2, "Female", "2004-09-25", "diana@test.com", "1111111114"),
            ("EE2024001", "Eve Wilson", dept_dict.get('EE', 2), 1, "Female", "2005-01-30", "eve@test.com", "1111111115"),
            ("EE2024002", "Frank Miller", dept_dict.get('EE', 2), 1, "Male", "2005-04-12", "frank@test.com", "1111111116"),
        ]
        
        for roll, name, dept_id, sem, gender, dob, email, phone in students:
            query = """INSERT OR IGNORE INTO students 
                       (roll_number, name, department_id, semester, gender, date_of_birth, email, phone, address)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            success, _ = db.execute_update(query, (roll, name, dept_id, sem, gender, dob, email, phone, "123 Main St"))
            if success:
                print(f"✓ {roll} - {name}")
        
        # 4. Add Marks for Semester 1 Students
        print_section("Adding Sample Marks")
        students_data = db.execute_query("SELECT * FROM students WHERE semester = 1")
        courses_data = db.execute_query("SELECT * FROM courses WHERE semester = 1")
        
        for student in students_data:
            for course in courses_data:
                if student['department_id'] == course['department_id']:
                    marks = random.randint(50, 95)
                    query = """INSERT OR IGNORE INTO marks 
                               (student_id, course_id, marks_obtained, entered_by)
                               VALUES (?, ?, ?, 1)"""
                    success, _ = db.execute_update(query, (student['student_id'], course['course_id'], marks))
                    if success:
                        # Calculate grade
                        percentage = (marks / course['max_marks']) * 100
                        if percentage >= 90: grade = 'A+'
                        elif percentage >= 80: grade = 'A'
                        elif percentage >= 70: grade = 'B'
                        elif percentage >= 60: grade = 'C'
                        elif percentage >= 50: grade = 'D'
                        else: grade = 'F'
                        
                        status = 'Pass' if marks >= course['pass_marks'] else 'Fail'
                        
                        update_query = "UPDATE marks SET grade = ?, status = ? WHERE student_id = ? AND course_id = ?"
                        db.execute_update(update_query, (grade, status, student['student_id'], course['course_id']))
                        
                        print(f"✓ {student['roll_number']} - {course['course_code']}: {marks} ({grade})")
        
        # 5. Add Additional Users
        print_section("Adding Additional Users")
        users = [
            ("teacher1", "password123", "Teacher", "Dr. John Smith"),
            ("teacher2", "password123", "Teacher", "Dr. Sarah Johnson"),
        ]
        
        for username, password, role, fullname in users:
            pwd_hash = hash_password(password)
            query = """INSERT OR IGNORE INTO users (username, password_hash, role, full_name)
                       VALUES (?, ?, ?, ?)"""
            success, _ = db.execute_update(query, (username, pwd_hash, role, fullname))
            if success:
                print(f"✓ {username} ({role})")
        
        print_section("SUCCESS!")
        print("✓ Sample data added successfully!")
        print("\nYou can now:")
        print("  1. Run the application: python main.py")
        print("  2. Login with: admin / admin123")
        print("  3. Explore all features:")
        print("     - View students, courses, departments")
        print("     - Check marks and results")
        print("     - Test Extra Features tab")
        print("     - Toggle Light/Dark theme (button in header)")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  UNIVERSITY EXAM SYSTEM - DATA POPULATOR")
    print("="*60)
    add_sample_data()
