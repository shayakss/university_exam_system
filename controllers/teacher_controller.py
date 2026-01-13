"""
Teacher Controller - Manages teacher-specific operations
"""
from typing import List, Tuple
from database.db_manager import db


class TeacherController:
    """Handles teacher course assignments and permissions"""
    
    def assign_teacher_to_course(self, user_id: int, course_id: int) -> Tuple[bool, str]:
        """
        Assign a teacher to a course
        
        Args:
            user_id: Teacher's user ID
            course_id: Course ID
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if assignment already exists
        existing = db.execute_query(
            "SELECT * FROM teacher_assignments WHERE user_id = ? AND course_id = ?",
            (user_id, course_id)
        )
        
        if existing and len(existing) > 0:
            return False, "Teacher is already assigned to this course"
        
        # Get course department
        course = db.execute_query(
            "SELECT department_id FROM courses WHERE course_id = ?",
            (course_id,)
        )
        
        if not course:
            return False, "Course not found"
        
        department_id = course[0]['department_id']
        
        # Create assignment
        query = """
            INSERT INTO teacher_assignments (user_id, department_id, course_id)
            VALUES (?, ?, ?)
        """
        
        success, _ = db.execute_update(query, (user_id, department_id, course_id))
        
        if success:
            return True, "Teacher assigned to course successfully"
        else:
            return False, "Failed to assign teacher to course"
    
    def remove_teacher_from_course(self, user_id: int, course_id: int) -> Tuple[bool, str]:
        """Remove teacher from a course"""
        query = "DELETE FROM teacher_assignments WHERE user_id = ? AND course_id = ?"
        success, _ = db.execute_update(query, (user_id, course_id))
        
        if success:
            return True, "Teacher removed from course"
        else:
            return False, "Failed to remove teacher from course"
    
    def get_teacher_courses(self, user_id: int) -> List[dict]:
        """Get all courses assigned to a teacher"""
        query = """
            SELECT c.*, d.department_name, d.department_code
            FROM teacher_assignments ta
            JOIN courses c ON ta.course_id = c.course_id
            JOIN departments d ON c.department_id = d.department_id
            WHERE ta.user_id = ? AND c.is_active = 1
            ORDER BY c.course_name
        """
        
        result = db.execute_query(query, (user_id,))
        return [dict(row) for row in result] if result else []
    
    def get_teacher_students(self, user_id: int) -> List[dict]:
        """Get all students in teacher's courses"""
        query = """
            SELECT DISTINCT s.*, d.department_name
            FROM teacher_assignments ta
            JOIN courses c ON ta.course_id = c.course_id
            JOIN students s ON s.department_id = c.department_id AND s.semester = c.semester
            JOIN departments d ON s.department_id = d.department_id
            WHERE ta.user_id = ? AND s.is_active = 1
            ORDER BY s.roll_number
        """
        
        result = db.execute_query(query, (user_id,))
        return [dict(row) for row in result] if result else []
    
    def can_teacher_enter_marks(self, user_id: int, course_id: int) -> bool:
        """Check if teacher can enter marks for a specific course"""
        query = """
            SELECT COUNT(*) as count
            FROM teacher_assignments
            WHERE user_id = ? AND course_id = ?
        """
        
        result = db.execute_query(query, (user_id, course_id))
        return result[0]['count'] > 0 if result else False
    
    def get_teachers_by_department(self, department_id: int) -> List[dict]:
        """Get all teachers in a department"""
        query = """
            SELECT DISTINCT u.user_id, u.username, u.full_name, u.email
            FROM users u
            JOIN teacher_assignments ta ON u.user_id = ta.user_id
            WHERE ta.department_id = ? AND u.role = 'Teacher' AND u.is_active = 1
            ORDER BY u.full_name
        """
        
        result = db.execute_query(query, (department_id,))
        return [dict(row) for row in result] if result else []


# Global teacher controller instance
teacher_controller = TeacherController()
