"""
Department Controller - Handles department CRUD operations
"""
from typing import List, Optional, Tuple
from database.db_manager import db
from utils.validators import validate_department_code


class DepartmentController:
    """Manages department operations"""
    
    def get_all_departments(self, include_inactive: bool = False) -> List[dict]:
        """
        Get all departments
        
        Args:
            include_inactive: Include inactive departments
        
        Returns:
            List of department dictionaries
        """
        query = "SELECT * FROM departments"
        if not include_inactive:
            query += " WHERE is_active = 1"
        query += " ORDER BY department_name"
        
        result = db.execute_query(query)
        return [dict(row) for row in result] if result else []
    
    def get_department_by_id(self, department_id: int) -> Optional[dict]:
        """Get department by ID"""
        query = "SELECT * FROM departments WHERE department_id = ?"
        result = db.execute_query(query, (department_id,))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def get_department_by_code(self, department_code: str) -> Optional[dict]:
        """Get department by code"""
        query = "SELECT * FROM departments WHERE department_code = ?"
        result = db.execute_query(query, (department_code.upper(),))
        return dict(result[0]) if result and len(result) > 0 else None
    
    def create_department(self, department_name: str, department_code: str, head_of_department: str = None) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new department
        
        Args:
            department_name: Department name
            department_code: Department code (e.g., CS, EE, MATH)
            head_of_department: Name of the head of department (optional)
        
        Returns:
            Tuple of (success: bool, message: str, department_id: int)
        """
        # Validate inputs
        if not department_name or len(department_name.strip()) < 2:
            return False, "Department name must be at least 2 characters", None
        
        is_valid, msg = validate_department_code(department_code)
        if not is_valid:
            return False, msg, None
        
        # Check for duplicates
        existing_name = db.execute_query(
            "SELECT department_id FROM departments WHERE LOWER(department_name) = LOWER(?)",
            (department_name.strip(),)
        )
        if existing_name and len(existing_name) > 0:
            return False, "Department name already exists", None
        
        existing_code = db.execute_query(
            "SELECT department_id FROM departments WHERE department_code = ?",
            (department_code.upper(),)
        )
        if existing_code and len(existing_code) > 0:
            return False, "Department code already exists", None
        
        # Insert department
        query = """
            INSERT INTO departments (department_name, department_code, head_of_department)
            VALUES (?, ?, ?)
        """
        success, dept_id = db.execute_update(query, (department_name.strip(), department_code.upper(), head_of_department))
        
        if success:
            return True, "Department created successfully", dept_id
        else:
            return False, "Failed to create department", None
    
    def update_department(self, department_id: int, department_name: str, department_code: str, head_of_department: str = None) -> Tuple[bool, str]:
        """
        Update department details
        
        Args:
            department_id: Department ID
            department_name: New department name
            department_code: New department code
            head_of_department: Name of the head of department (optional)
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate inputs
        if not department_name or len(department_name.strip()) < 2:
            return False, "Department name must be at least 2 characters"
        
        is_valid, msg = validate_department_code(department_code)
        if not is_valid:
            return False, msg
        
        # Check if department exists
        existing = self.get_department_by_id(department_id)
        if not existing:
            return False, "Department not found"
        
        # Check for duplicate name (excluding current department)
        duplicate_name = db.execute_query(
            "SELECT department_id FROM departments WHERE LOWER(department_name) = LOWER(?) AND department_id != ?",
            (department_name.strip(), department_id)
        )
        if duplicate_name and len(duplicate_name) > 0:
            return False, "Department name already exists"
        
        # Check for duplicate code (excluding current department)
        duplicate_code = db.execute_query(
            "SELECT department_id FROM departments WHERE department_code = ? AND department_id != ?",
            (department_code.upper(), department_id)
        )
        if duplicate_code and len(duplicate_code) > 0:
            return False, "Department code already exists"
        
        # Update department
        query = """
            UPDATE departments 
            SET department_name = ?, department_code = ?, head_of_department = ?
            WHERE department_id = ?
        """
        success, _ = db.execute_update(query, (department_name.strip(), department_code.upper(), head_of_department, department_id))
        
        if success:
            return True, "Department updated successfully"
        else:
            return False, "Failed to update department"
    
    def delete_department(self, department_id: int) -> Tuple[bool, str]:
        """
        Delete a department
        
        Args:
            department_id: Department ID
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if department has students
        students_check = db.execute_query(
            "SELECT COUNT(*) as count FROM students WHERE department_id = ?",
            (department_id,)
        )
        if students_check and students_check[0]['count'] > 0:
            return False, "Cannot delete department with existing students"
        
        # Check if department has courses
        courses_check = db.execute_query(
            "SELECT COUNT(*) as count FROM courses WHERE department_id = ?",
            (department_id,)
        )
        if courses_check and courses_check[0]['count'] > 0:
            return False, "Cannot delete department with existing courses"
        
        # Delete department
        query = "DELETE FROM departments WHERE department_id = ?"
        success, _ = db.execute_update(query, (department_id,))
        
        if success:
            return True, "Department deleted successfully"
        else:
            return False, "Failed to delete department"
    
    def deactivate_department(self, department_id: int) -> Tuple[bool, str]:
        """Deactivate a department"""
        query = "UPDATE departments SET is_active = 0 WHERE department_id = ?"
        success, _ = db.execute_update(query, (department_id,))
        
        if success:
            return True, "Department deactivated successfully"
        else:
            return False, "Failed to deactivate department"
    
    def activate_department(self, department_id: int) -> Tuple[bool, str]:
        """Activate a department"""
        query = "UPDATE departments SET is_active = 1 WHERE department_id = ?"
        success, _ = db.execute_update(query, (department_id,))
        
        if success:
            return True, "Department activated successfully"
        else:
            return False, "Failed to activate department"
    
    def get_department_statistics(self, department_id: int) -> dict:
        """Get statistics for a department"""
        stats = {
            'total_students': 0,
            'total_courses': 0,
            'students_by_semester': {}
        }
        
        # Get total students
        result = db.execute_query(
            "SELECT COUNT(*) as count FROM students WHERE department_id = ? AND is_active = 1",
            (department_id,)
        )
        if result:
            stats['total_students'] = result[0]['count']
        
        # Get total courses
        result = db.execute_query(
            "SELECT COUNT(*) as count FROM courses WHERE department_id = ? AND is_active = 1",
            (department_id,)
        )
        if result:
            stats['total_courses'] = result[0]['count']
        
        # Get students by semester
        result = db.execute_query(
            "SELECT semester, COUNT(*) as count FROM students WHERE department_id = ? AND is_active = 1 GROUP BY semester",
            (department_id,)
        )
        if result:
            for row in result:
                stats['students_by_semester'][row['semester']] = row['count']
        
        return stats


# Global department controller instance
department_controller = DepartmentController()
