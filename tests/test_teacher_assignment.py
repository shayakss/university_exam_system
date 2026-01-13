import sqlite3
import os
from controllers.user_controller import user_controller
from controllers.course_controller import course_controller
from controllers.department_controller import department_controller

# Mock authentication for testing
class MockAuth:
    def __init__(self, user):
        self.user = user
    def get_current_user(self):
        return self.user

def test_teacher_assignment():
    print("=== Testing Teacher Assignment ===")
    
    # 1. Setup Data
    print("Setting up test data...")
    # Get a department
    depts = department_controller.get_all_departments()
    if not depts:
        print("No departments found. Skipping.")
        return
    dept_id = depts[0]['department_id']
    
    # Get a course in that department
    courses = course_controller.get_courses_by_department(dept_id)
    if not courses:
        print("No courses found in department. Skipping.")
        return
    course_id = courses[0]['course_id']
    
    # 2. Create Teacher with Assigned Subject
    print(f"Creating teacher with assigned subject (Course ID: {course_id})...")
    username = "test_teacher_subject"
    
    # Clean up if exists
    existing = user_controller.get_user_by_username(username)
    if existing:
        user_controller.delete_user(existing['user_id'])
        
    success, msg, user_id = user_controller.create_user(
        username=username,
        password="Password123",
        full_name="Test Teacher Subject",
        role="Teacher",
        email="teacher@test.com",
        department_id=dept_id,
        assigned_subject_id=course_id
    )
    
    if success:
        print("Teacher created successfully.")
    else:
        print(f"Failed to create teacher: {msg}")
        return

    # 3. Verify Database
    print("Verifying database record...")
    user = user_controller.get_user_by_id(user_id)
    if user['assigned_subject_id'] == course_id:
        print("PASS: assigned_subject_id matches.")
    else:
        print(f"FAIL: assigned_subject_id mismatch. Expected {course_id}, got {user['assigned_subject_id']}")

    # 4. Simulate Marks Entry Logic
    print("Simulating Marks Entry Logic...")
    # Mock the auth
    from controllers import auth_controller
    auth_controller.auth = MockAuth(user)
    
    # Check logic from MarksEntryPage
    assigned_subject_id = None
    current_user = auth_controller.auth.get_current_user()
    if current_user and current_user.get('role') == 'Teacher':
        assigned_subject_id = current_user.get('assigned_subject_id')
    
    if assigned_subject_id == course_id:
        print("PASS: UI logic correctly identifies assigned subject.")
    else:
        print(f"FAIL: UI logic failed. Got {assigned_subject_id}")

    # Cleanup
    # user_controller.delete_user(user_id)
    print("Test Complete.")

if __name__ == "__main__":
    test_teacher_assignment()
