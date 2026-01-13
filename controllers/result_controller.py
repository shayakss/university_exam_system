"""
Result Controller - Handles result generation and calculation
"""
from typing import List, Optional, Tuple, Dict
from database.db_manager import db
from controllers.marks_controller import marks_controller
import config


class ResultController:
    """Manages result generation and calculations"""
    
    def get_student_results(self, student_id):
        """Get all results for a specific student"""
        query = """
            SELECT 
                m.*,
                c.course_code,
                c.course_name,
                c.max_marks
            FROM marks m
            JOIN courses c ON m.course_id = c.course_id
            WHERE m.student_id = ?
            ORDER BY c.course_code
        """
        
        try:
            results = db.execute_query(query, (student_id,))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"Error fetching student results: {e}")
            return []
    
    def calculate_sgpa(self, student_id: int, semester: int) -> Tuple[bool, float, str]:
        """
        Calculate SGPA (Semester Grade Point Average) for a student
        
        Args:
            student_id: Student ID
            semester: Semester number
        
        Returns:
            Tuple of (success: bool, sgpa: float, message: str)
        """
        # Get all marks for the semester
        marks = marks_controller.get_student_marks(student_id, semester)
        
        if not marks or len(marks) == 0:
            return False, 0.0, "No marks found for this semester"
        
        total_grade_points = 0.0
        total_credits = 0
        
        for mark in marks:
            grade = mark['grade']
            credits = mark['credits']
            
            # Get grade points from grading scale
            grade_points = config.GRADING_SCALE.get(grade, {}).get('points', 0)
            
            total_grade_points += grade_points * credits
            total_credits += credits
        
        if total_credits == 0:
            return False, 0.0, "No credits found"
        
        sgpa = round(total_grade_points / total_credits, 2)
        return True, sgpa, "SGPA calculated successfully"
    
    def calculate_cgpa(self, student_id: int, up_to_semester: int) -> Tuple[bool, float, str]:
        """
        Calculate CGPA (Cumulative Grade Point Average) for a student
        
        Args:
            student_id: Student ID
            up_to_semester: Calculate CGPA up to this semester
        
        Returns:
            Tuple of (success: bool, cgpa: float, message: str)
        """
        total_grade_points = 0.0
        total_credits = 0
        
        # Get marks for all semesters up to the specified semester
        for sem in range(1, up_to_semester + 1):
            marks = marks_controller.get_student_marks(student_id, sem)
            
            for mark in marks:
                grade = mark['grade']
                credits = mark['credits']
                
                grade_points = config.GRADING_SCALE.get(grade, {}).get('points', 0)
                
                total_grade_points += grade_points * credits
                total_credits += credits
        
        if total_credits == 0:
            return False, 0.0, "No marks found"
        
        cgpa = round(total_grade_points / total_credits, 2)
        return True, cgpa, "CGPA calculated successfully"
    
    def calculate_percentage(self, student_id: int, semester: int) -> Tuple[bool, float, float, float, str]:
        """
        Calculate percentage for a semester
        
        Returns:
            Tuple of (success: bool, percentage: float, total_marks: float, 
                     marks_obtained: float, message: str)
        """
        marks = marks_controller.get_student_marks(student_id, semester)
        
        if not marks or len(marks) == 0:
            return False, 0.0, 0.0, 0.0, "No marks found for this semester"
        
        total_max_marks = 0.0
        total_obtained_marks = 0.0
        
        for mark in marks:
            total_max_marks += mark['max_marks']
            total_obtained_marks += mark['marks_obtained']
        
        if total_max_marks == 0:
            return False, 0.0, 0.0, 0.0, "Invalid marks data"
        
        percentage = round((total_obtained_marks / total_max_marks) * 100, 2)
        return True, percentage, total_max_marks, total_obtained_marks, "Percentage calculated successfully"
    
    def calculate_overall_grade(self, cgpa: float) -> str:
        """Calculate overall grade based on CGPA"""
        # Convert CGPA (0-10) to percentage equivalent
        percentage = cgpa * 10
        
        for grade, scale in config.GRADING_SCALE.items():
            if scale['min'] <= percentage <= scale['max']:
                return grade
        
        return 'F'
    
    def determine_overall_status(self, student_id: int, semester: int) -> str:
        """Determine if student passed or failed the semester"""
        marks = marks_controller.get_student_marks(student_id, semester)
        
        for mark in marks:
            if mark['status'] == 'Fail':
                return 'Fail'
        
        return 'Pass' if marks else 'No Data'
    
    def generate_result(self, student_id: int, semester: int) -> Tuple[bool, Optional[Dict], str]:
        """
        Generate complete result for a student for a semester
        
        Returns:
            Tuple of (success: bool, result_data: dict, message: str)
        """
        # Get student details
        student_query = """
            SELECT s.*, d.department_name, d.department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
            WHERE s.student_id = ?
        """
        student_result = db.execute_query(student_query, (student_id,))
        
        if not student_result or len(student_result) == 0:
            return False, None, "Student not found"
        
        student = dict(student_result[0])
        
        # Get marks
        marks = marks_controller.get_student_marks(student_id, semester)
        
        if not marks or len(marks) == 0:
            return False, None, "No marks found for this semester"
        
        # Calculate SGPA
        success, sgpa, msg = self.calculate_sgpa(student_id, semester)
        if not success:
            return False, None, msg
        
        # Calculate CGPA
        success, cgpa, msg = self.calculate_cgpa(student_id, semester)
        if not success:
            cgpa = sgpa  # Use SGPA if CGPA calculation fails
        
        # Calculate percentage
        success, percentage, total_marks, marks_obtained, msg = self.calculate_percentage(student_id, semester)
        if not success:
            return False, None, msg
        
        # Determine overall status
        overall_status = self.determine_overall_status(student_id, semester)
        
        # Calculate overall grade
        overall_grade = self.calculate_overall_grade(cgpa)
        
        # Prepare result data
        result_data = {
            'student': student,
            'semester': semester,
            'marks': marks,
            'sgpa': sgpa,
            'cgpa': cgpa,
            'percentage': percentage,
            'total_marks': total_marks,
            'marks_obtained': marks_obtained,
            'overall_grade': overall_grade,
            'status': overall_status
        }
        
        # Save/update result in database
        self._save_result(student_id, semester, total_marks, marks_obtained, 
                         percentage, sgpa, cgpa, overall_grade, overall_status)
        
        return True, result_data, "Result generated successfully"
    
    def _save_result(self, student_id: int, semester: int, total_marks: float,
                    marks_obtained: float, percentage: float, sgpa: float,
                    cgpa: float, overall_grade: str, status: str):
        """Save or update result in database"""
        # Check if result exists
        existing = db.execute_query(
            "SELECT result_id FROM results WHERE student_id = ? AND semester = ?",
            (student_id, semester)
        )
        
        if existing and len(existing) > 0:
            # Update existing result
            query = """
                UPDATE results
                SET total_marks = ?, marks_obtained = ?, percentage = ?,
                    sgpa = ?, cgpa = ?, overall_grade = ?, status = ?,
                    generated_at = CURRENT_TIMESTAMP
                WHERE student_id = ? AND semester = ?
            """
            success, _ = db.execute_update(query, (total_marks, marks_obtained, percentage,
                                     sgpa, cgpa, overall_grade, status,
                                     student_id, semester))
        else:
            # Insert new result
            query = """
                INSERT INTO results (student_id, semester, total_marks, marks_obtained,
                                   percentage, sgpa, cgpa, overall_grade, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, _ = db.execute_update(query, (student_id, semester, total_marks, marks_obtained,
                                     percentage, sgpa, cgpa, overall_grade, status))
    
    def calculate_ranks(self, department_id: int, semester: int):
        """Calculate and update ranks for students in a department and semester"""
        # Get all results for the department and semester
        query = """
            SELECT r.result_id, r.student_id, r.cgpa
            FROM results r
            LEFT JOIN students s ON r.student_id = s.student_id
            WHERE s.department_id = ? AND r.semester = ?
            ORDER BY r.cgpa DESC
        """
        results = db.execute_query(query, (department_id, semester))
        
        if not results:
            return
        
        # Update ranks
        rank = 1
        for result in results:
            update_query = "UPDATE results SET rank = ? WHERE result_id = ?"
            success, _ = db.execute_update(update_query, (rank, result['result_id']))
            rank += 1
    
    def get_topper_list(self, department_id: int, semester: int, limit: int = 10) -> List[dict]:
        """Get topper list for a department and semester"""
        query = """
            SELECT r.*, s.roll_number, s.name as student_name, d.department_name
            FROM results r
            LEFT JOIN students s ON r.student_id = s.student_id
            LEFT JOIN departments d ON s.department_id = d.department_id
            WHERE s.department_id = ? AND r.semester = ?
            ORDER BY r.cgpa DESC, r.percentage DESC
            LIMIT ?
        """
        result = db.execute_query(query, (department_id, semester, limit))
        return [dict(row) for row in result] if result else []
    
    def get_pass_fail_statistics(self, department_id: Optional[int] = None, 
                                 semester: Optional[int] = None) -> Dict:
        """Get pass/fail statistics"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Pass' THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN status = 'Fail' THEN 1 ELSE 0 END) as failed
            FROM results r
            LEFT JOIN students s ON r.student_id = s.student_id
            WHERE 1=1
        """
        params = []
        
        if department_id is not None:
            query += " AND s.department_id = ?"
            params.append(department_id)
        
        if semester is not None:
            query += " AND r.semester = ?"
            params.append(semester)
        
        result = db.execute_query(query, tuple(params))
        
        if result and result[0]['total'] > 0:
            row = result[0]
            return {
                'total': row['total'],
                'passed': row['passed'],
                'failed': row['failed'],
                'pass_percentage': round((row['passed'] / row['total']) * 100, 2) if row['total'] > 0 else 0
            }
        
        return {'total': 0, 'passed': 0, 'failed': 0, 'pass_percentage': 0}


# Global result controller instance
result_controller = ResultController()
