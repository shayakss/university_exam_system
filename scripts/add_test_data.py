"""
Add 10 test students with marks to existing TiDB Cloud database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import db
from controllers.department_controller import department_controller
from controllers.course_controller import course_controller
from controllers.student_controller import student_controller
from controllers.marks_controller import marks_controller
import random

print("\n" + "="*60)
print("ADDING TEST DATA TO TIDB CLOUD")
print("="*60)

# Get existing departments
print("\n1. Getting existing departments...")
depts = department_controller.get_all_departments()
if len(depts) < 2:
    print("⚠ Need at least 2 departments. Creating them...")
    success, msg, cs_id = department_controller.create_department("Computer Science", "CS")
    if success:
        print(f"✓ Created CS department (ID: {cs_id})")
    success, msg, math_id = department_controller.create_department("Mathematics", "MATH")
    if success:
        print(f"✓ Created MATH department (ID: {math_id})")
    depts = department_controller.get_all_departments()

print(f"✓ Found {len(depts)} departments")
for dept in depts[:2]:
    print(f"  - {dept['department_name']} ({dept['department_code']})")

# Get existing courses
print("\n2. Getting existing courses...")
courses = course_controller.get_all_courses()
print(f"✓ Found {len(courses)} courses")

# If no courses, create some
if len(courses) == 0:
    print("⚠ No courses found. Creating sample courses...")
    for dept in depts[:2]:
        dept_id = dept['department_id']
        dept_code = dept['department_code']
        
        # Create 3 courses per department
        for i in range(1, 4):
            code = f"{dept_code}{100+i}"
            name = f"{dept['department_name']} Course {i}"
            success, msg, course_id = course_controller.create_course(
                code, name, dept_id, 1, 100, 40, 3
            )
            if success:
                print(f"✓ Created course: {code}")
    
    courses = course_controller.get_all_courses()
    print(f"✓ Now have {len(courses)} courses")

# Create 10 students
print("\n3. Creating 10 students...")
first_names = ["Ahmed", "Fatima", "Ali", "Ayesha", "Hassan", "Zainab", "Omar", "Mariam", "Bilal", "Sara"]
last_names = ["Khan", "Ahmed", "Ali", "Hassan", "Hussain", "Malik", "Shah", "Baloch", "Raza", "Siddiqui"]

students_created = 0
for i in range(10):
    dept = depts[i % len(depts)]  # Alternate between departments
    dept_code = dept['department_code']
    
    roll_number = f"{dept_code}-{2021}-{i+1:03d}"
    name = f"{first_names[i]} {last_names[i]}"
    father_name = f"{random.choice(['Muhammad', 'Abdul', 'Ahmed'])} {last_names[i]}"
    
    success, message, student_id = student_controller.create_student(
        roll_number=roll_number,
        name=name,
        father_name=father_name,
        department_id=dept['department_id'],
        semester=1,
        gender=random.choice(['Male', 'Female']),
        date_of_birth='2003-01-01',
        email=f"{name.lower().replace(' ', '.')}@student.edu",
        phone='',
        address='Quetta, Pakistan',
        registration_no=f"REG-2021-{i+1:04d}"
    )
    
    if success:
        print(f"✓ Created: {roll_number} - {name}")
        students_created += 1
    else:
        if "already exists" in message.lower():
            print(f"⚠ Student already exists: {roll_number}")
        else:
            print(f"✗ Failed: {roll_number} - {message}")

print(f"\n✓ Created {students_created} new students")

# Assign marks
print("\n4. Assigning marks to students...")
students = student_controller.get_all_students()
admin_query = "SELECT user_id FROM users WHERE username = 'admin' LIMIT 1"
admin_result = db.execute_query(admin_query)
admin_id = admin_result[0]['user_id'] if admin_result else 1

marks_assigned = 0
for student in students[:10]:  # Only first 10 students
    # Get courses for this student's department
    student_courses = course_controller.get_courses_by_department(
        student['department_id'], semester=1
    )
    
    for course in student_courses[:3]:  # Max 3 courses per student
        # Check if marks already exist
        existing = marks_controller.get_mark(student['student_id'], course['course_id'])
        if existing:
            continue
        
        # Assign random marks
        marks = random.randint(50, 95)
        success, msg, mark_id = marks_controller.enter_marks(
            student_id=student['student_id'],
            course_id=course['course_id'],
            marks_obtained=marks,
            entered_by=admin_id
        )
        
        if success:
            marks_assigned += 1

print(f"✓ Assigned {marks_assigned} new marks entries")

# Final summary
print("\n" + "="*60)
print("FINAL DATABASE STATUS")
print("="*60)

dept_count = db.execute_query("SELECT COUNT(*) as count FROM departments")[0]['count']
course_count = db.execute_query("SELECT COUNT(*) as count FROM courses")[0]['count']
student_count = db.execute_query("SELECT COUNT(*) as count FROM students")[0]['count']
marks_count = db.execute_query("SELECT COUNT(*) as count FROM marks")[0]['count']

print(f"✓ Departments: {dept_count}")
print(f"✓ Courses: {course_count}")
print(f"✓ Students: {student_count}")
print(f"✓ Marks entries: {marks_count}")

print("\n" + "="*60)
print("✓ TEST DATA ADDED SUCCESSFULLY!")
print("="*60)
print("\nYour TiDB Cloud database is ready to use!")
print("Run the application to see all the data.")
