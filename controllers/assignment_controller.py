"""
Assignment Controller
Manages assignments and student submissions
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class AssignmentController:
    """Controller for assignment management"""
    
    def create_assignment(self, course_id: int, teacher_id: int, title: str,
                         description: str, due_date: date, total_marks: int = 10) -> Tuple[bool, str]:
        """Create a new assignment"""
        try:
            query = """
                INSERT INTO assignments (course_id, teacher_id, title, description, due_date, total_marks)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            success, assignment_id = db.execute_update(
                query, (course_id, teacher_id, title, description, due_date, total_marks)
            )
            
            if success:
                # Auto-create pending submissions for all students in the course
                self._create_pending_submissions(assignment_id, course_id)
                return True, f"Assignment created successfully (ID: {assignment_id})"
            return False, "Failed to create assignment"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def _create_pending_submissions(self, assignment_id: int, course_id: int):
        """Create pending submission records for all students enrolled in the course"""
        try:
            # Get students from the same department and semester as the course
            query = """
                INSERT INTO assignment_submissions (assignment_id, student_id, status)
                SELECT ?, s.student_id, 'Pending'
                FROM students s
                JOIN courses c ON s.department_id = c.department_id AND s.semester = c.semester
                WHERE c.course_id = ? AND s.is_active = 1
            """
            db.execute_update(query, (assignment_id, course_id))
        except Exception as e:
            print(f"Error creating pending submissions: {e}")
    
    def submit_assignment(self, assignment_id: int, student_id: int,
                         file_path: str = None, remarks: str = None) -> Tuple[bool, str]:
        """Mark assignment as submitted by student"""
        try:
            # Check if submission exists
            check_query = """
                SELECT submission_id, assignment_id FROM assignment_submissions
                WHERE assignment_id = ? AND student_id = ?
            """
            existing = db.execute_query(check_query, (assignment_id, student_id))
            
            # Check if late
            assignment = db.execute_query(
                "SELECT due_date FROM assignments WHERE assignment_id = ?", (assignment_id,)
            )
            
            status = 'Submitted'
            if assignment and assignment[0]['due_date']:
                due_date = datetime.strptime(assignment[0]['due_date'], '%Y-%m-%d').date()
                if date.today() > due_date:
                    status = 'Late'
            
            if existing:
                query = """
                    UPDATE assignment_submissions
                    SET submission_date = CURRENT_TIMESTAMP, status = ?, file_path = ?, remarks = ?
                    WHERE assignment_id = ? AND student_id = ?
                """
                success, _ = db.execute_update(
                    query, (status, file_path, remarks, assignment_id, student_id)
                )
            else:
                query = """
                    INSERT INTO assignment_submissions
                    (assignment_id, student_id, status, file_path, remarks)
                    VALUES (?, ?, ?, ?, ?)
                """
                success, _ = db.execute_update(
                    query, (assignment_id, student_id, status, file_path, remarks)
                )
            
            if success:
                return True, f"Assignment {status.lower()} successfully"
            return False, "Failed to submit assignment"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def grade_assignment(self, submission_id: int, marks_obtained: float,
                        remarks: str = None) -> Tuple[bool, str]:
        """Grade a student's assignment submission"""
        try:
            query = """
                UPDATE assignment_submissions
                SET marks_obtained = ?, remarks = ?, status = 'Graded'
                WHERE submission_id = ?
            """
            success, _ = db.execute_update(query, (marks_obtained, remarks, submission_id))
            
            if success:
                return True, "Assignment graded successfully"
            return False, "Failed to grade assignment"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_assignments(self, course_id: int = None, teacher_id: int = None,
                       is_active: bool = True) -> List[Dict]:
        """Get assignments with filters"""
        try:
            query = """
                SELECT a.*, c.course_name, c.course_code, u.full_name as teacher_name,
                       d.department_name,
                       (SELECT COUNT(*) FROM assignment_submissions 
                        WHERE assignment_id = a.assignment_id AND status = 'Submitted') as submitted_count,
                       (SELECT COUNT(*) FROM assignment_submissions 
                        WHERE assignment_id = a.assignment_id AND status = 'Pending') as pending_count,
                       (SELECT COUNT(*) FROM assignment_submissions 
                        WHERE assignment_id = a.assignment_id AND status = 'Late') as late_count
                FROM assignments a
                JOIN courses c ON a.course_id = c.course_id
                JOIN users u ON a.teacher_id = u.user_id
                JOIN departments d ON c.department_id = d.department_id
                WHERE 1=1
            """
            params = []
            
            if course_id:
                query += " AND a.course_id = ?"
                params.append(course_id)
            if teacher_id:
                query += " AND a.teacher_id = ?"
                params.append(teacher_id)
            if is_active is not None:
                query += " AND a.is_active = ?"
                params.append(1 if is_active else 0)
            
            query += " ORDER BY a.due_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting assignments: {e}")
            return []
    
    def get_student_assignments(self, student_id: int, status: str = None) -> List[Dict]:
        """Get assignments for a specific student"""
        try:
            query = """
                SELECT a.*, c.course_name, c.course_code, u.full_name as teacher_name,
                       asub.submission_id, asub.submission_date, asub.status as submission_status,
                       asub.marks_obtained, asub.remarks as submission_remarks,
                       CASE 
                           WHEN date(a.due_date) < date('now') AND asub.status = 'Pending' THEN 1
                           ELSE 0
                       END as is_overdue
                FROM assignments a
                JOIN courses c ON a.course_id = c.course_id
                JOIN users u ON a.teacher_id = u.user_id
                LEFT JOIN assignment_submissions asub ON a.assignment_id = asub.assignment_id 
                    AND asub.student_id = ?
                JOIN students s ON s.department_id = c.department_id AND s.semester = c.semester
                WHERE s.student_id = ? AND a.is_active = 1
            """
            params = [student_id, student_id]
            
            if status:
                query += " AND asub.status = ?"
                params.append(status)
            
            query += " ORDER BY a.due_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting student assignments: {e}")
            return []
    
    def get_assignment_submissions(self, assignment_id: int, status: str = None) -> List[Dict]:
        """Get all submissions for an assignment"""
        try:
            query = """
                SELECT asub.*, s.roll_number, s.name as student_name, s.student_id
                FROM assignment_submissions asub
                JOIN students s ON asub.student_id = s.student_id
                WHERE asub.assignment_id = ?
            """
            params = [assignment_id]
            
            if status:
                query += " AND asub.status = ?"
                params.append(status)
            
            query += " ORDER BY asub.submission_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting assignment submissions: {e}")
            return []
    
    def delete_assignment(self, assignment_id: int) -> Tuple[bool, str]:
        """Delete an assignment (soft delete)"""
        try:
            query = "UPDATE assignments SET is_active = 0 WHERE assignment_id = ?"
            success, _ = db.execute_update(query, (assignment_id,))
            
            if success:
                return True, "Assignment deleted successfully"
            return False, "Failed to delete assignment"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_assignment_statistics(self, teacher_id: int = None) -> Dict:
        """Get assignment statistics"""
        try:
            query = """
                SELECT 
                    COUNT(DISTINCT a.assignment_id) as total_assignments,
                    COUNT(DISTINCT CASE WHEN asub.status = 'Submitted' THEN asub.submission_id END) as total_submitted,
                    COUNT(DISTINCT CASE WHEN asub.status = 'Pending' THEN asub.submission_id END) as total_pending,
                    COUNT(DISTINCT CASE WHEN asub.status = 'Late' THEN asub.submission_id END) as total_late,
                    COUNT(DISTINCT CASE WHEN asub.status = 'Graded' THEN asub.submission_id END) as total_graded
                FROM assignments a
                LEFT JOIN assignment_submissions asub ON a.assignment_id = asub.assignment_id
                WHERE a.is_active = 1
            """
            params = []
            
            if teacher_id:
                query += " AND a.teacher_id = ?"
                params.append(teacher_id)
            
            result = db.execute_query(query, tuple(params))
            return result[0] if result else {}
        except Exception as e:
            print(f"Error getting assignment statistics: {e}")
            return {}

# Global instance
assignment_controller = AssignmentController()
