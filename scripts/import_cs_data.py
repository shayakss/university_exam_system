"""
Complete script to import Computer Science data from Excel
"""
import sqlite3
import pandas as pd
import config
from datetime import datetime

def clear_all_data():
    """Clear all data except admin user"""
    print("=" * 60)
    print("STEP 1: Clearing existing data...")
    print("=" * 60)
    
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM results")
        cursor.execute("DELETE FROM marks")
        cursor.execute("DELETE FROM courses")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM users WHERE role != 'Admin'")
        cursor.execute("DELETE FROM departments")
        
        conn.commit()
        print("✓ All data cleared successfully\n")
        return True
    except Exception as e:
        print(f"✗ Error: {e}\n")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_department():
    """Create Computer Science department"""
    print("=" * 60)
    print("STEP 2: Creating Computer Science Department...")
    print("=" * 60)
    
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO departments (department_name, department_code, head_of_department)
            VALUES (?, ?, ?)
        """, ("Computer Science", "CS", "Dr. Computer Science Head"))
        
        dept_id = cursor.lastrowid
        conn.commit()
        print(f"✓ Department created with ID: {dept_id}\n")
        return dept_id
    except Exception as e:
        print(f"✗ Error: {e}\n")
        conn.rollback()
        return None
    finally:
        conn.close()

def import_excel_data(file_path, dept_id):
    """Import students, courses, and marks from Excel"""
    print("=" * 60)
    print("STEP 3: Importing data from Excel...")
    print("=" * 60)
    
    try:
        # Read all sheets
        excel_data = pd.read_excel(file_path, sheet_name=None)
        
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        students_created = set()
        courses_created = {}
        marks_entered = 0
        
        # Process each semester sheet
        for sheet_name, df in excel_data.items():
            print(f"\nProcessing: {sheet_name}")
            
            # Determine semester number
            semester = int(''.join(filter(str.isdigit, sheet_name))) if any(c.isdigit() for c in sheet_name) else 1
            print(f"  Semester: {semester}")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Process each row
            for idx, row in df.iterrows():
                try:
                    # Skip header rows or empty rows
                    if pd.isna(row.get('Roll No', row.iloc[0])) or str(row.get('Roll No', row.iloc[0])).strip() == '':
                        continue
                    
                    # Extract student info
                    roll_no = str(row.get('Roll No', row.iloc[0])).strip()
                    student_name = str(row.get('Student Name', row.iloc[1])).strip() if len(row) > 1 else f"Student {roll_no}"
                    father_name = str(row.get('Father Name', row.iloc[2])).strip() if len(row) > 2 else ""
                    
                    # Skip if invalid
                    if roll_no == 'nan' or roll_no == '' or 'Roll' in roll_no:
                        continue
                    
                    # Create student if not exists
                    if roll_no not in students_created:
                        cursor.execute("""
                            INSERT INTO students (roll_number, name, father_name, department_id, semester, gender, date_of_birth)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (roll_no, student_name, father_name, dept_id, semester, 'Male', '2000-01-01'))
                        
                        students_created.add(roll_no)
                        print(f"    ✓ Student: {roll_no} - {student_name}")
                    
                    # Get student_id
                    cursor.execute("SELECT student_id FROM students WHERE roll_number = ?", (roll_no,))
                    student_result = cursor.fetchone()
                    if not student_result:
                        continue
                    student_id = student_result[0]
                    
                    # Process course marks (columns after student info)
                    for col_idx, col_name in enumerate(df.columns):
                        if col_idx < 3:  # Skip Roll No, Name, Father Name
                            continue
                        
                        if 'TOTAL' in str(col_name).upper() or 'REMARK' in str(col_name).upper() or 'RESULT' in str(col_name).upper():
                            continue
                        
                        # Get marks value
                        marks_value = row.iloc[col_idx]
                        if pd.isna(marks_value) or str(marks_value).strip() == '':
                            continue
                        
                        try:
                            marks = float(marks_value)
                        except:
                            continue
                        
                        # Create course if not exists
                        course_code = str(col_name).strip()
                        course_key = f"{course_code}_S{semester}"
                        
                        if course_key not in courses_created:
                            cursor.execute("""
                                INSERT INTO courses (course_code, course_name, department_id, semester, credits, max_marks, pass_marks)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (course_code, course_code, dept_id, semester, 3, 100, 40))
                            
                            course_id = cursor.lastrowid
                            courses_created[course_key] = course_id
                            print(f"    ✓ Course: {course_code}")
                        else:
                            course_id = courses_created[course_key]
                        
                        # Enter marks
                        cursor.execute("""
                            INSERT OR REPLACE INTO marks (student_id, course_id, marks_obtained, max_marks, grade, status, entered_by)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (student_id, course_id, marks, 100, 
                              'A' if marks >= 80 else 'B' if marks >= 60 else 'C' if marks >= 40 else 'F',
                              'Pass' if marks >= 40 else 'Fail', 1))
                        
                        marks_entered += 1
                
                except Exception as e:
                    print(f"    ✗ Error processing row {idx}: {e}")
                    continue
        
        conn.commit()
        conn.close()
        
        print(f"\n{'=' * 60}")
        print("IMPORT SUMMARY")
        print("=" * 60)
        print(f"✓ Students created: {len(students_created)}")
        print(f"✓ Courses created: {len(courses_created)}")
        print(f"✓ Marks entered: {marks_entered}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COMPUTER SCIENCE DATA IMPORT TOOL")
    print("=" * 60 + "\n")
    
    # Step 1: Clear data
    if not clear_all_data():
        print("Failed to clear data. Exiting.")
        exit(1)
    
    # Step 2: Create department
    dept_id = create_department()
    if not dept_id:
        print("Failed to create department. Exiting.")
        exit(1)
    
    # Step 3: Import Excel data
    file_path = r"sample_data\Computer science  2021-to-2025  8 Semesters Results.xls"
    if import_excel_data(file_path, dept_id):
        print("\n" + "=" * 60)
        print("✓ IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ IMPORT FAILED")
        print("=" * 60)
