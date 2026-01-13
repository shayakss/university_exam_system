"""
Course Controller - Handles course/subject CRUD operations
"""
from typing import List, Optional, Tuple
from database.db_manager import db
from utils.validators import validate_course_code, validate_semester, validate_credits


class CourseController:
    """Manages course operations"""
    
    def get_all_courses(self, include_inactive: bool = False) -> List[dict]:
        """Get all courses with department information"""
        query = """
            SELECT c.*, d.department_name, d.department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.department_id
        """
        if not include_inactive:
            query += " WHERE c.is_active = 1"
        query += " ORDER BY d.department_name, c.semester, c.course_name"
        
        result = db.execute_query(query)
        return [dict(row) for row in result] if result else []
    
    def get_courses_by_department(self, department_id: int, semester: Optional[int] = None) -> List[dict]:
        """Get courses by department and optionally by semester"""
        query = """
            SELECT c.*, d.department_name, d.department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.department_id
            WHERE c.department_id = ? AND c.is_active = 1
        """
        params = [department_id]
        
        if semester is not None:
            query += " AND c.semester = ?"
            params.append(semester)
        
        query += " ORDER BY c.semester, c.course_name"
        
        result = db.execute_query(query, tuple(params))
        return [dict(row) for row in result] if result else []
    
    def get_course_by_id(self, course_id: int) -> Optional[dict]:
        """Get course by ID"""
        query = """
            SELECT c.*, d.department_name, d.department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.department_id
            WHERE c.course_id = ?
        """
        result = db.execute_query(query, (course_id,))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def get_course_by_code(self, course_code: str) -> Optional[dict]:
        """Get course by code"""
        query = """
            SELECT c.*, d.department_name, d.department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.department_id
            WHERE c.course_code = ?
        """
        result = db.execute_query(query, (course_code.upper(),))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def create_course(self, course_code: str, course_name: str, department_id: int,
                     semester: int, max_marks: int, pass_marks: int, credits: int) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new course
        
        Args:
            course_code: Unique course code
            course_name: Course name
            department_id: Department ID
            semester: Semester number (1-8)
            max_marks: Maximum marks
            pass_marks: Passing marks
            credits: Course credits
        
        Returns:
            Tuple of (success: bool, message: str, course_id: int)
        """
        # Validate inputs
        is_valid, msg = validate_course_code(course_code)
        if not is_valid:
            return False, msg, None
        
        if not course_name or len(course_name.strip()) < 2:
            return False, "Course name must be at least 2 characters", None
        
        is_valid, msg = validate_semester(semester)
        if not is_valid:
            return False, msg, None
        
        is_valid, msg = validate_credits(credits)
        if not is_valid:
            return False, msg, None
        
        if max_marks <= 0:
            return False, "Maximum marks must be greater than 0", None
        
        if pass_marks <= 0 or pass_marks > max_marks:
            return False, "Pass marks must be between 1 and maximum marks", None
        
        # Check if department exists
        dept_check = db.execute_query("SELECT department_id FROM departments WHERE department_id = ?", (department_id,))
        if not dept_check or len(dept_check) == 0:
            return False, "Department not found", None
        
        # Check for duplicate course code
        existing = db.execute_query(
            "SELECT course_id FROM courses WHERE course_code = ?",
            (course_code.upper(),)
        )
        if existing and len(existing) > 0:
            return False, "Course code already exists", None
        
        # Insert course
        query = """
            INSERT INTO courses (course_code, course_name, department_id, semester, 
                               max_marks, pass_marks, credits)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        success, course_id = db.execute_update(
            query,
            (course_code.upper(), course_name.strip(), department_id, semester, max_marks, pass_marks, credits)
        )
        
        if success:
            return True, "Course created successfully", course_id
        else:
            return False, "Failed to create course", None
    
    def update_course(self, course_id: int, course_code: str, course_name: str,
                     department_id: int, semester: int, max_marks: int, 
                     pass_marks: int, credits: int) -> Tuple[bool, str]:
        """Update course details"""
        # Validate inputs
        is_valid, msg = validate_course_code(course_code)
        if not is_valid:
            return False, msg
        
        if not course_name or len(course_name.strip()) < 2:
            return False, "Course name must be at least 2 characters"
        
        is_valid, msg = validate_semester(semester)
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_credits(credits)
        if not is_valid:
            return False, msg
        
        if max_marks <= 0:
            return False, "Maximum marks must be greater than 0"
        
        if pass_marks <= 0 or pass_marks > max_marks:
            return False, "Pass marks must be between 1 and maximum marks"
        
        # Check if course exists
        existing = self.get_course_by_id(course_id)
        if not existing:
            return False, "Course not found"
        
        # Check for duplicate code (excluding current course)
        duplicate = db.execute_query(
            "SELECT course_id FROM courses WHERE course_code = ? AND course_id != ?",
            (course_code.upper(), course_id)
        )
        if duplicate and len(duplicate) > 0:
            return False, "Course code already exists"
        
        # Update course
        query = """
            UPDATE courses 
            SET course_code = ?, course_name = ?, department_id = ?, semester = ?,
                max_marks = ?, pass_marks = ?, credits = ?
            WHERE course_id = ?
        """
        success, _ = db.execute_update(
            query,
            (course_code.upper(), course_name.strip(), department_id, semester, 
             max_marks, pass_marks, credits, course_id)
        )
        
        if success:
            return True, "Course updated successfully"
        else:
            return False, "Failed to update course"
    
    def delete_course(self, course_id: int) -> Tuple[bool, str]:
        """Delete a course (only if no marks exist)"""
        # Check if course has marks
        marks = db.execute_query(
            "SELECT COUNT(*) as count FROM marks WHERE course_id = ?",
            (course_id,)
        )
        if marks and marks[0]['count'] > 0:
            return False, "Cannot delete course with existing marks. Deactivate instead."
        
        # Delete course
        query = "DELETE FROM courses WHERE course_id = ?"
        success, _ = db.execute_update(query, (course_id,))
        
        if success:
            return True, "Course deleted successfully"
        else:
            return False, "Failed to delete course"
    
    def deactivate_course(self, course_id: int) -> Tuple[bool, str]:
        """Deactivate a course"""
        query = "UPDATE courses SET is_active = 0 WHERE course_id = ?"
        success, _ = db.execute_update(query, (course_id,))
        
        if success:
            return True, "Course deactivated successfully"
        else:
            return False, "Failed to deactivate course"
    
    def activate_course(self, course_id: int) -> Tuple[bool, str]:
        """Activate a course"""
        query = "UPDATE courses SET is_active = 1 WHERE course_id = ?"
        success, _ = db.execute_update(query, (course_id,))
        
        if success:
            return True, "Course activated successfully"
        else:
            return False, "Failed to activate course"
    
    def get_course_statistics(self, course_id: int) -> dict:
        """Get statistics for a course"""
        stats = {
            'total_students_enrolled': 0,
            'average_marks': 0.0,
            'pass_rate': 0.0,
            'highest_marks': 0.0,
            'lowest_marks': 0.0
        }
        
        # Get marks statistics
        query = """
            SELECT 
                COUNT(*) as total,
                AVG(marks_obtained) as avg_marks,
                MAX(marks_obtained) as max_marks,
                MIN(marks_obtained) as min_marks,
                SUM(CASE WHEN status = 'Pass' THEN 1 ELSE 0 END) as passed
            FROM marks
            WHERE course_id = ?
        """
        result = db.execute_query(query, (course_id,))
        
        if result and result[0]['total'] > 0:
            row = result[0]
            stats['total_students_enrolled'] = row['total']
            stats['average_marks'] = round(row['avg_marks'], 2) if row['avg_marks'] else 0.0
            stats['highest_marks'] = row['max_marks'] if row['max_marks'] else 0.0
            stats['lowest_marks'] = row['min_marks'] if row['min_marks'] else 0.0
            stats['pass_rate'] = round((row['passed'] / row['total']) * 100, 2) if row['total'] > 0 else 0.0
        
        return stats


# Global course controller instance
course_controller = CourseController()
