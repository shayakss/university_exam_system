"""
Generate Sample Student Data with Complete 8-Semester Records
This script creates 10 students with full academic data for transcript testing
"""
from database.db_manager import db
from controllers.student_controller import student_controller
from controllers.course_controller import course_controller
from controllers.marks_controller import marks_controller
import random
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate 10 students with complete 8-semester data"""
    
    print("=" * 60)
    print("GENERATING SAMPLE STUDENT DATA")
    print("=" * 60)
    
    # Sample student names
    students_info = [
        {"name": "Ahmed Khan", "father": "Muhammad Khan", "cnic": "42101-1234567-1"},
        {"name": "Fatima Ali", "father": "Ali Ahmed", "cnic": "42101-2345678-2"},
        {"name": "Hassan Baloch", "father": "Abdul Baloch", "cnic": "42101-3456789-3"},
        {"name": "Ayesha Raza", "father": "Raza Hussain", "cnic": "42101-4567890-4"},
        {"name": "Bilal Shah", "father": "Shah Nawaz", "cnic": "42101-5678901-5"},
        {"name": "Zainab Malik", "father": "Malik Asad", "cnic": "42101-6789012-6"},
        {"name": "Usman Kakar", "father": "Kakar Khan", "cnic": "42101-7890123-7"},
        {"name": "Maryam Achakzai", "father": "Achakzai Sardar", "cnic": "42101-8901234-8"},
        {"name": "Hamza Mengal", "father": "Mengal Nawab", "cnic": "42101-9012345-9"},
        {"name": "Sana Bugti", "father": "Bugti Sardar", "cnic": "42101-0123456-0"}
    ]
    
    # Get first department (CS)
    departments = db.execute_query("SELECT * FROM departments LIMIT 1")
    if not departments:
        print("❌ No departments found! Please create departments first.")
        return
    
    dept = dict(departments[0])
    dept_id = dept['department_id']
    dept_code = dept['department_code']
    
    print(f"\n📚 Using Department: {dept['department_name']} ({dept_code})")
    
    # Get or create courses for all 8 semesters
    print("\n📖 Setting up courses for 8 semesters...")
    courses_by_semester = {}
    
    # Course templates for each semester
    course_templates = {
        1: [
            ("Programming Fundamentals", "PF", 4),
            ("Discrete Mathematics", "DM", 3),
            ("English Composition", "ENG", 3),
            ("Islamic Studies", "ISL", 2),
            ("Pakistan Studies", "PAK", 2)
        ],
        2: [
            ("Object Oriented Programming", "OOP", 4),
            ("Data Structures", "DS", 4),
            ("Digital Logic Design", "DLD", 3),
            ("Linear Algebra", "LA", 3),
            ("Communication Skills", "CS", 2)
        ],
        3: [
            ("Database Systems", "DBS", 4),
            ("Computer Organization", "COA", 3),
            ("Probability & Statistics", "PS", 3),
            ("Software Engineering", "SE", 3),
            ("Technical Writing", "TW", 2)
        ],
        4: [
            ("Operating Systems", "OS", 4),
            ("Web Technologies", "WT", 3),
            ("Algorithm Analysis", "AA", 3),
            ("Computer Networks", "CN", 3),
            ("Professional Ethics", "PE", 2)
        ],
        5: [
            ("Artificial Intelligence", "AI", 4),
            ("Mobile App Development", "MAD", 3),
            ("Information Security", "IS", 3),
            ("Software Design", "SD", 3),
            ("Entrepreneurship", "ENT", 2)
        ],
        6: [
            ("Machine Learning", "ML", 4),
            ("Cloud Computing", "CC", 3),
            ("Compiler Construction", "COMP", 3),
            ("Human Computer Interaction", "HCI", 3),
            ("Research Methodology", "RM", 2)
        ],
        7: [
            ("Deep Learning", "DL", 4),
            ("Big Data Analytics", "BDA", 3),
            ("Cyber Security", "CYS", 3),
            ("Project Management", "PM", 3),
            ("Elective I", "EL1", 3)
        ],
        8: [
            ("Final Year Project", "FYP", 6),
            ("Blockchain Technology", "BCT", 3),
            ("IoT Systems", "IOT", 3),
            ("Elective II", "EL2", 3)
        ]
    }
    
    # Create courses for each semester
    for semester in range(1, 9):
        courses_by_semester[semester] = []
        for course_name, course_code, credits in course_templates[semester]:
            # Check if course exists
            existing = db.execute_query(
                "SELECT course_id FROM courses WHERE course_code = ? AND semester = ?",
                (course_code, semester)
            )
            
            if existing:
                course_id = existing[0]['course_id']
            else:
                # Create course
                success, msg, course_id = course_controller.create_course(
                    course_code=course_code,
                    course_name=course_name,
                    department_id=dept_id,
                    credits=credits,
                    semester=semester,
                    max_marks=100,
                    pass_marks=50
                )
                if not success:
                    print(f"  ⚠️  Warning: Could not create {course_name}: {msg}")
                    continue
            
            courses_by_semester[semester].append({
                'course_id': course_id,
                'course_name': course_name,
                'course_code': course_code,
                'credits': credits
            })
        
        print(f"  ✓ Semester {semester}: {len(courses_by_semester[semester])} courses")
    
    # Create students with full data
    print(f"\n👥 Creating 10 students with 8-semester records...")
    created_count = 0
    
    for idx, student_info in enumerate(students_info, 1):
        # Generate roll number
        year = datetime.now().year - 4  # Started 4 years ago
        roll_number = f"{dept_code}-{idx:02d}-{year % 100}"
        
        # Generate email
        email = f"{student_info['name'].lower().replace(' ', '.')}@student.uob.edu.pk"
        
        # Generate phone
        phone = f"03{random.randint(10, 99)}{random.randint(1000000, 9999999)}"
        guardian_phone = f"03{random.randint(10, 99)}{random.randint(1000000, 9999999)}"
        
        # Generate DOB (20-25 years old)
        age_years = random.randint(20, 25)
        dob = (datetime.now() - timedelta(days=age_years*365)).strftime("%Y-%m-%d")
        
        # Address
        address = f"House #{random.randint(1, 999)}, Street {random.randint(1, 50)}, Quetta, Balochistan"
        
        # Create student
        success, msg, student_id = student_controller.create_student(
            roll_number=roll_number,
            name=student_info['name'],
            department_id=dept_id,
            semester=8,  # Final semester
            gender=random.choice(["Male", "Female"]),
            date_of_birth=dob,
            email=email,
            phone=phone,
            address=address,
            registration_no=f"REG-{year}-{idx:04d}",
            cnic=student_info['cnic'],
            father_name=student_info['father'],
            father_cnic=student_info['cnic'].replace('1', '2'),  # Slightly different
            guardian_phone=guardian_phone
        )
        
        if not success:
            print(f"  ❌ Failed to create {student_info['name']}: {msg}")
            continue
        
        print(f"\n  ✓ Created: {student_info['name']} ({roll_number})")
        
        # Add marks for all 8 semesters
        total_marks_added = 0
        for semester in range(1, 9):
            if semester not in courses_by_semester:
                continue
            
            for course in courses_by_semester[semester]:
                # Generate realistic marks (50-95)
                # Better students get higher marks
                base_performance = random.randint(60, 95)
                obtained = random.randint(max(50, base_performance - 10), min(100, base_performance + 5))
                
                # Add marks using enter_marks (student_id, course_id, marks_obtained, entered_by)
                # Using student_id 1 as the admin who entered marks
                success, msg, _ = marks_controller.enter_marks(
                    student_id=student_id,
                    course_id=course['course_id'],
                    marks_obtained=obtained,
                    entered_by=1  # Admin user
                )
                
                if success:
                    total_marks_added += 1
        
        print(f"    📝 Added {total_marks_added} marks entries across 8 semesters")
        created_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ SAMPLE DATA GENERATION COMPLETE!")
    print(f"   Created: {created_count} students")
    print(f"   Each with: 8 semesters of courses and marks")
    print(f"   Total courses per student: ~40 courses")
    print("=" * 60)
    print("\n💡 You can now export transcripts for these students!")
    print("   Go to Student Management → Select a student → Click 'Transcript'")
    print("=" * 60)


if __name__ == "__main__":
    try:
        generate_sample_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
