"""
Marks Controller - Handles marks entry and management
"""
from typing import List, Optional, Tuple
from database.db_manager import db
from utils.security import validate_marks
import config


class MarksController:
    """Manages marks operations"""
    
    def get_student_marks(self, student_id: int, semester: Optional[int] = None) -> List[dict]:
        """Get all marks for a student"""
        query = """
            SELECT m.*, c.course_name, c.course_code, c.max_marks, c.pass_marks, 
                   c.credits, c.semester, u.full_name as entered_by_name
            FROM marks m
            LEFT JOIN courses c ON m.course_id = c.course_id
            LEFT JOIN users u ON m.entered_by = u.user_id
            WHERE m.student_id = ?
        """
        params = [student_id]
        
        if semester is not None:
            query += " AND c.semester = ?"
            params.append(semester)
        
        query += " ORDER BY c.semester, c.course_name"
        
        result = db.execute_query(query, tuple(params))
        return [dict(row) for row in result] if result else []
    
    def get_course_marks(self, course_id: int) -> List[dict]:
        """Get all marks for a course"""
        query = """
            SELECT m.*, s.roll_number, s.name as student_name, 
                   d.department_name, u.full_name as entered_by_name
            FROM marks m
            LEFT JOIN students s ON m.student_id = s.student_id
            LEFT JOIN departments d ON s.department_id = d.department_id
            LEFT JOIN users u ON m.entered_by = u.user_id
            WHERE m.course_id = ?
            ORDER BY s.roll_number
        """
        result = db.execute_query(query, (course_id,))
        return [dict(row) for row in result] if result else []
    
    def get_mark_by_id(self, mark_id: int) -> Optional[dict]:
        """Get mark by ID"""
        query = """
            SELECT m.*, c.course_name, c.course_code, c.max_marks, c.pass_marks,
                   s.roll_number, s.name as student_name
            FROM marks m
            LEFT JOIN courses c ON m.course_id = c.course_id
            LEFT JOIN students s ON m.student_id = s.student_id
            WHERE m.mark_id = ?
        """
        result = db.execute_query(query, (mark_id,))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def get_mark(self, student_id: int, course_id: int) -> Optional[dict]:
        """Get mark for a specific student and course"""
        query = """
            SELECT m.*, c.course_name, c.course_code, c.max_marks, c.pass_marks
            FROM marks m
            LEFT JOIN courses c ON m.course_id = c.course_id
            WHERE m.student_id = ? AND m.course_id = ?
        """
        result = db.execute_query(query, (student_id, course_id))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def calculate_grade(self, marks_obtained: float, max_marks: float) -> str:
        """
        Calculate grade based on percentage
        
        Args:
            marks_obtained: Marks obtained
            max_marks: Maximum marks
        
        Returns:
            Grade (A+, A, B+, B, C+, C, F)
        """
        percentage = (marks_obtained / max_marks) * 100
        
        for grade, scale in config.GRADING_SCALE.items():
            if scale['min'] <= percentage <= scale['max']:
                return grade
        
        return 'F'
    
    def calculate_status(self, marks_obtained: float, pass_marks: float) -> str:
        """Determine pass/fail status"""
        return 'Pass' if marks_obtained >= pass_marks else 'Fail'
    
    def enter_marks(self, student_id: int, course_id: int, marks_obtained: float, 
                   entered_by: int) -> Tuple[bool, str, Optional[int]]:
        """
        Enter marks for a student in a course
        
        Args:
            student_id: Student ID
            course_id: Course ID
            marks_obtained: Marks obtained
            entered_by: User ID who entered the marks
        
        Returns:
            Tuple of (success: bool, message: str, mark_id: int)
        """
        # Get course details
        course_query = "SELECT max_marks, pass_marks FROM courses WHERE course_id = ?"
        course_result = db.execute_query(course_query, (course_id,))
        
        if not course_result or len(course_result) == 0:
            return False, "Course not found", None
        
        course = course_result[0]
        max_marks = course['max_marks']
        pass_marks = course['pass_marks']
        
        # Validate marks
        is_valid, msg = validate_marks(marks_obtained, max_marks)
        if not is_valid:
            return False, msg, None
        
        # Check if student exists
        student_check = db.execute_query("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
        if not student_check or len(student_check) == 0:
            return False, "Student not found", None
        
        # Calculate grade and status
        grade = self.calculate_grade(marks_obtained, max_marks)
        status = self.calculate_status(marks_obtained, pass_marks)
        
        # Check if marks already exist
        existing = self.get_mark(student_id, course_id)
        
        if existing:
            # Update existing marks
            query = """
                UPDATE marks 
                SET marks_obtained = ?, grade = ?, status = ?, 
                    entered_by = ?, updated_at = CURRENT_TIMESTAMP
                WHERE student_id = ? AND course_id = ?
            """
            success, _ = db.execute_update(
                query,
                (marks_obtained, grade, status, entered_by, student_id, course_id)
            )
            
            if success:
                return True, "Marks updated successfully", existing['mark_id']
            else:
                return False, "Failed to update marks", None
        else:
            # Insert new marks
            query = """
                INSERT INTO marks (student_id, course_id, marks_obtained, grade, status, entered_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            success, mark_id = db.execute_update(
                query,
                (student_id, course_id, marks_obtained, grade, status, entered_by)
            )
            
            if success:
                return True, "Marks entered successfully", mark_id
            else:
                return False, "Failed to enter marks", None
    
    def bulk_enter_marks(self, marks_data: List[dict], entered_by: int) -> Tuple[bool, str, int]:
        """
        Bulk enter marks for multiple students
        
        Args:
            marks_data: List of dicts with keys: student_id, course_id, marks_obtained
            entered_by: User ID who entered the marks
        
        Returns:
            Tuple of (success: bool, message: str, count: int)
        """
        success_count = 0
        errors = []
        
        for data in marks_data:
            success, msg, _ = self.enter_marks(
                student_id=data['student_id'],
                course_id=data['course_id'],
                marks_obtained=data['marks_obtained'],
                entered_by=entered_by
            )
            
            if success:
                success_count += 1
            else:
                errors.append(f"Student {data.get('student_id')}: {msg}")
        
        if success_count > 0:
            error_msg = f"\n{len(errors)} errors occurred" if errors else ""
            return True, f"Entered marks for {success_count} students.{error_msg}", success_count
        else:
            return False, f"Failed to enter marks. Errors:\n" + "\n".join(errors[:5]), 0
    
    def delete_marks(self, mark_id: int) -> Tuple[bool, str]:
        """Delete marks entry"""
        query = "DELETE FROM marks WHERE mark_id = ?"
        success, _ = db.execute_update(query, (mark_id,))
        
        if success:
            return True, "Marks deleted successfully"
        else:
            return False, "Failed to delete marks"
    
    def get_marks_by_department_semester(self, department_id: int, semester: int) -> List[dict]:
        """Get all marks for a department and semester"""
        query = """
            SELECT m.*, s.roll_number, s.name as student_name, 
                   c.course_name, c.course_code, c.max_marks, c.pass_marks
            FROM marks m
            LEFT JOIN students s ON m.student_id = s.student_id
            LEFT JOIN courses c ON m.course_id = c.course_id
            WHERE s.department_id = ? AND c.semester = ?
            ORDER BY s.roll_number, c.course_name
        """
        result = db.execute_query(query, (department_id, semester))
        return [dict(row) for row in result] if result else []
    
    def get_recent_marks_entries(self, limit: int = 10) -> List[dict]:
        """Get recent marks entries"""
        query = """
            SELECT m.*, s.roll_number, s.name as student_name,
                   c.course_name, c.course_code, u.full_name as entered_by_name
            FROM marks m
            LEFT JOIN students s ON m.student_id = s.student_id
            LEFT JOIN courses c ON m.course_id = c.course_id
            LEFT JOIN users u ON m.entered_by = u.user_id
            ORDER BY m.entered_at DESC
            LIMIT ?
        """
        result = db.execute_query(query, (limit,))
        return [dict(row) for row in result] if result else []


# Global marks controller instance
marks_controller = MarksController()
