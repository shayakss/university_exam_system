"""
Student Controller - Handles student CRUD operations
"""
from typing import List, Optional, Tuple
from database.db_manager import db
from utils.security import validate_email, validate_phone
from utils.validators import validate_roll_number, validate_name, validate_semester, validate_gender, validate_date
import pandas as pd


class StudentController:
    """Manages student operations"""
    
    def get_all_students(self, include_inactive: bool = False) -> List[dict]:
        """Get all students with department information"""
        query = """
            SELECT s.*, d.department_name, d.department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
        """
        if not include_inactive:
            query += " WHERE s.is_active = 1"
        query += " ORDER BY s.roll_number"
        
        result = db.execute_query(query)
        return [dict(row) for row in result] if result else []
    
    def get_students_by_department(self, department_id: int, semester: Optional[int] = None) -> List[dict]:
        """Get students by department and optionally by semester"""
        query = """
            SELECT s.*, d.department_name, d.department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
            WHERE s.department_id = ? AND s.is_active = 1
        """
        params = [department_id]
        
        if semester is not None:
            query += " AND s.semester = ?"
            params.append(semester)
        
        query += " ORDER BY s.roll_number"
        
        result = db.execute_query(query, tuple(params))
        return [dict(row) for row in result] if result else []
    
    def get_student_by_id(self, student_id: int) -> Optional[dict]:
        """Get student by ID"""
        query = """
            SELECT s.*, d.department_name, d.department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
            WHERE s.student_id = ?
        """
        result = db.execute_query(query, (student_id,))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def get_student_by_roll_number(self, roll_number: str) -> Optional[dict]:
        """Get student by roll number"""
        query = """
            SELECT s.*, d.department_name, d.department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
            WHERE s.roll_number = ?
        """
        result = db.execute_query(query, (roll_number.upper(),))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def search_students(self, search_term: str) -> List[dict]:
        """Search students by name, roll number, cnic, email or department"""
        query = """
            SELECT s.*, d.department_name, d.department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
            WHERE s.is_active = 1 AND (
                s.name LIKE ? OR 
                s.roll_number LIKE ? OR
                s.email LIKE ? OR
                s.cnic LIKE ? OR
                d.department_name LIKE ?
            )
            ORDER BY s.roll_number
        """
        search_pattern = f"%{search_term}%"
        result = db.execute_query(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        return [dict(row) for row in result] if result else []
    
    def create_student(self, roll_number: str, name: str, department_id: int, semester: int,
                      gender: str, date_of_birth: str, email: str = None, 
                      phone: str = None, address: str = None, registration_no: str = None,
                      cnic: str = None, father_name: str = None, father_cnic: str = None,
                      guardian_phone: str = None) -> Tuple[bool, str, Optional[int]]:
        """Create a new student with all fields"""
        # Validate inputs
        is_valid, msg = validate_roll_number(roll_number)
        if not is_valid:
            return False, msg, None
        
        is_valid, msg = validate_name(name)
        if not is_valid:
            return False, msg, None
        
        if email and not validate_email(email):
            return False, "Invalid email format", None
        
        if phone and not validate_phone(phone):
            return False, "Invalid phone number format (must be 11 digits)", None
            
        if guardian_phone and not validate_phone(guardian_phone):
            return False, "Invalid guardian phone number format (must be 11 digits)", None
        
        # Check if department exists
        dept_check = db.execute_query("SELECT department_id FROM departments WHERE department_id = ?", (department_id,))
        if not dept_check or len(dept_check) == 0:
            return False, "Department not found", None
        
        # Check for duplicate roll number
        existing = db.execute_query(
            "SELECT student_id FROM students WHERE roll_number = ?",
            (roll_number.upper(),)
        )
        if existing and len(existing) > 0:
            return False, "Roll number already exists", None
            
        # Insert student
        query = """
            INSERT INTO students (
                roll_number, name, department_id, semester, gender, date_of_birth,
                email, phone, address, registration_no, cnic, father_name, father_cnic, guardian_phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            roll_number.upper(), name, department_id, semester, gender, date_of_birth,
            email, phone, address, registration_no, cnic, father_name, father_cnic, guardian_phone
        )
        
        success, row_id = db.execute_update(query, params)
        if success:
            return True, "Student created successfully", row_id
        return False, "Failed to create student", None
    
    def update_student(self, student_id: int, roll_number: str, name: str, department_id: int,
                      semester: int, gender: str, date_of_birth: str, email: str = None,
                      phone: str = None, address: str = None, registration_no: str = None,
                      cnic: str = None, father_name: str = None, father_cnic: str = None,
                      guardian_phone: str = None) -> Tuple[bool, str]:
        """Update student details with all fields"""
        # Validate inputs
        is_valid, msg = validate_roll_number(roll_number)
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_name(name)
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_semester(semester)
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_gender(gender)
        if not is_valid:
            return False, msg
        
        is_valid, parsed_date, msg = validate_date(date_of_birth)
        if not is_valid:
            return False, msg
        
        if email and not validate_email(email):
            return False, "Invalid email format"
        
        if phone and not validate_phone(phone):
            return False, "Invalid phone number format"
        
        # Check if student exists
        existing = self.get_student_by_id(student_id)
        if not existing:
            return False, "Student not found"
        
        # Check for duplicate roll number (excluding current student)
        duplicate = db.execute_query(
            "SELECT student_id FROM students WHERE roll_number = ? AND student_id != ?",
            (roll_number.upper(), student_id)
        )
        if duplicate and len(duplicate) > 0:
            return False, "Roll number already exists"
        
        # Update student
        query = """
            UPDATE students 
            SET roll_number = ?, name = ?, department_id = ?, semester = ?, gender = ?,
                date_of_birth = ?, email = ?, phone = ?, address = ?, registration_no = ?,
                cnic = ?, father_name = ?, father_cnic = ?, guardian_phone = ?
            WHERE student_id = ?
        """
        success, _ = db.execute_update(
            query,
            (roll_number.upper(), name.strip(), department_id, semester, gender,
             date_of_birth, email, phone, address, registration_no, cnic,
             father_name, father_cnic, guardian_phone, student_id)
        )
        
        if success:
            return True, "Student updated successfully"
        else:
            return False, "Failed to update student"
    
    def delete_student(self, student_id: int) -> Tuple[bool, str]:
        """
        Delete a student and all related records
        
        Args:
            student_id: ID of student to delete
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Delete related records first (to handle foreign key constraints)
            # Delete marks
            db.execute_update("DELETE FROM marks WHERE student_id = %s", (student_id,))
            
            # Delete results
            db.execute_update("DELETE FROM results WHERE student_id = %s", (student_id,))
            
            # Delete attendance records if they exist
            db.execute_update("DELETE FROM student_attendance WHERE student_id = %s", (student_id,))
            
            # Delete user account if linked
            db.execute_update("DELETE FROM users WHERE student_id = %s", (student_id,))
            
            # Delete the student
            success, _ = db.execute_update("DELETE FROM students WHERE student_id = %s", (student_id,))
            
            if success:
                return True, "Student and all related records deleted successfully"
            else:
                return False, "Failed to delete student"
        except Exception as e:
            return False, f"Failed to delete student: {str(e)}"
    
    def deactivate_student(self, student_id: int) -> Tuple[bool, str]:
        """Deactivate a student"""
        query = "UPDATE students SET is_active = 0 WHERE student_id = ?"
        success, _ = db.execute_update(query, (student_id,))
        
        if success:
            return True, "Student deactivated successfully"
        else:
            return False, "Failed to deactivate student"
    
    def activate_student(self, student_id: int) -> Tuple[bool, str]:
        """Activate a student"""
        query = "UPDATE students SET is_active = 1 WHERE student_id = ?"
        success, _ = db.execute_update(query, (student_id,))
        
        if success:
            return True, "Student activated successfully"
        else:
            return False, "Failed to activate student"
    
    def bulk_import_students(self, file_path: str) -> Tuple[bool, str, int]:
        """
        Import students from CSV/Excel file
        
        Expected columns: roll_number, name, department_code, semester, gender, 
                         date_of_birth, email, phone, address
        
        Returns:
            Tuple of (success: bool, message: str, imported_count: int)
        """
        try:
            # Read file
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return False, "Unsupported file format. Use CSV or Excel.", 0
            
            # Validate required columns
            required_cols = ['roll_number', 'name', 'department_code', 'semester', 'gender', 'date_of_birth']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return False, f"Missing required columns: {', '.join(missing_cols)}", 0
            
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Get department ID from code
                    dept_result = db.execute_query(
                        "SELECT department_id FROM departments WHERE department_code = ?",
                        (str(row['department_code']).upper(),)
                    )
                    if not dept_result:
                        errors.append(f"Row {index + 2}: Department code '{row['department_code']}' not found")
                        continue
                    
                    department_id = dept_result[0]['department_id']
                    
                    # Create student
                    success, msg, _ = self.create_student(
                        roll_number=str(row['roll_number']),
                        name=str(row['name']),
                        department_id=department_id,
                        semester=int(row['semester']),
                        gender=str(row['gender']),
                        date_of_birth=str(row['date_of_birth']),
                        email=str(row.get('email', '')) if pd.notna(row.get('email')) else None,
                        phone=str(row.get('phone', '')) if pd.notna(row.get('phone')) else None,
                        address=str(row.get('address', '')) if pd.notna(row.get('address')) else None
                    )
                    
                    if success:
                        imported_count += 1
                    else:
                        errors.append(f"Row {index + 2}: {msg}")
                
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
            
            if imported_count > 0:
                error_msg = f"\n{len(errors)} errors occurred:\n" + "\n".join(errors[:5]) if errors else ""
                return True, f"Imported {imported_count} students successfully.{error_msg}", imported_count
            else:
                return False, f"No students imported. Errors:\n" + "\n".join(errors[:10]), 0
        
        except Exception as e:
            return False, f"Import failed: {str(e)}", 0


# Global student controller instance
student_controller = StudentController()
