"""
Student Promotion Controller
Manages automated student promotion based on eligibility criteria
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class PromotionController:
    """Controller for student promotion management"""
    
    def check_promotion_eligibility(self, student_id: int, current_semester: int) -> Tuple[bool, str, Dict]:
        """Check if a student is eligible for promotion"""
        try:
            # Get default promotion rule
            rule_query = "SELECT * FROM promotion_rules WHERE is_active = 1 ORDER BY rule_id LIMIT 1"
            rules = db.execute_query(rule_query)
            
            if not rules:
                return False, "No active promotion rules found", {}
            
            rule = rules[0]
            
            # Get student's CGPA
            cgpa_query = """
                SELECT cgpa FROM results 
                WHERE student_id = ? AND semester = ?
                ORDER BY generated_at DESC LIMIT 1
            """
            cgpa_result = db.execute_query(cgpa_query, (student_id, current_semester))
            cgpa = cgpa_result[0]['cgpa'] if cgpa_result and cgpa_result[0]['cgpa'] else 0.0
            
            # Count F grades in current semester
            f_grades_query = """
                SELECT COUNT(*) as f_count
                FROM marks m
                JOIN courses c ON m.course_id = c.course_id
                WHERE m.student_id = ? AND c.semester = ? AND m.grade = 'F'
            """
            f_result = db.execute_query(f_grades_query, (student_id, current_semester))
            f_count = f_result[0]['f_count'] if f_result else 0
            
            # Calculate attendance percentage
            attendance_query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status IN ('Present', 'Late') THEN 1 ELSE 0 END) as present
                FROM student_attendance
                WHERE student_id = ?
            """
            att_result = db.execute_query(attendance_query, (student_id,))
            attendance_pct = 0.0
            if att_result and att_result[0]['total'] > 0:
                attendance_pct = (att_result[0]['present'] / att_result[0]['total']) * 100
            
            # Check eligibility
            eligible = True
            reasons = []
            
            if cgpa < rule['min_cgpa']:
                eligible = False
                reasons.append(f"CGPA {cgpa:.2f} is below minimum {rule['min_cgpa']}")
            
            if f_count > rule['max_f_grades']:
                eligible = False
                reasons.append(f"Has {f_count} F grades (maximum allowed: {rule['max_f_grades']})")
            
            if attendance_pct < rule['min_attendance_percentage']:
                eligible = False
                reasons.append(f"Attendance {attendance_pct:.1f}% is below minimum {rule['min_attendance_percentage']}%")
            
            details = {
                'cgpa': cgpa,
                'f_grades': f_count,
                'attendance_percentage': attendance_pct,
                'rule_name': rule['rule_name']
            }
            
            if eligible:
                return True, "Student is eligible for promotion", details
            else:
                return False, "; ".join(reasons), details
                
        except Exception as e:
            return False, f"Error checking eligibility: {str(e)}", {}
    
    def promote_student(self, student_id: int, from_semester: int, 
                       promoted_by: int, remarks: str = None) -> Tuple[bool, str]:
        """Promote a student to the next semester"""
        try:
            # Check eligibility first
            eligible, message, details = self.check_promotion_eligibility(student_id, from_semester)
            
            if not eligible:
                return False, f"Student not eligible for promotion: {message}"
            
            to_semester = from_semester + 1
            
            # Check if already at max semester (8)
            if to_semester > 8:
                return False, "Student is already in final semester"
            
            # Update student's semester
            update_query = "UPDATE students SET semester = ? WHERE student_id = ?"
            success, _ = db.execute_update(update_query, (to_semester, student_id))
            
            if not success:
                return False, "Failed to update student semester"
            
            # Record promotion history
            history_query = """
                INSERT INTO promotion_history 
                (student_id, from_semester, to_semester, promotion_date, cgpa, promoted_by, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_update(
                history_query,
                (student_id, from_semester, to_semester, date.today(), 
                 details.get('cgpa', 0), promoted_by, remarks)
            )
            
            return True, f"Student promoted from semester {from_semester} to {to_semester}"
            
        except Exception as e:
            return False, f"Error promoting student: {str(e)}"
    
    def bulk_promote_students(self, department_id: int, semester: int, 
                             promoted_by: int) -> Tuple[bool, str, Dict]:
        """Promote all eligible students in a department/semester"""
        try:
            # Get all students in the department/semester
            students_query = """
                SELECT student_id, roll_number, name
                FROM students
                WHERE department_id = ? AND semester = ? AND is_active = 1
            """
            students = db.execute_query(students_query, (department_id, semester))
            
            if not students:
                return False, "No students found", {}
            
            promoted = []
            not_eligible = []
            errors = []
            
            for student in students:
                success, message = self.promote_student(
                    student['student_id'], semester, promoted_by
                )
                
                if success:
                    promoted.append({
                        'roll_number': student['roll_number'],
                        'name': student['name']
                    })
                else:
                    if "not eligible" in message.lower():
                        not_eligible.append({
                            'roll_number': student['roll_number'],
                            'name': student['name'],
                            'reason': message
                        })
                    else:
                        errors.append({
                            'roll_number': student['roll_number'],
                            'name': student['name'],
                            'error': message
                        })
            
            summary = {
                'total': len(students),
                'promoted': len(promoted),
                'not_eligible': len(not_eligible),
                'errors': len(errors),
                'promoted_list': promoted,
                'not_eligible_list': not_eligible,
                'error_list': errors
            }
            
            message = f"Promoted {len(promoted)}/{len(students)} students. "
            message += f"{len(not_eligible)} not eligible, {len(errors)} errors."
            
            return True, message, summary
            
        except Exception as e:
            return False, f"Error in bulk promotion: {str(e)}", {}
    
    def get_promotion_history(self, student_id: int = None) -> List[Dict]:
        """Get promotion history"""
        try:
            query = """
                SELECT ph.*, s.roll_number, s.name as student_name,
                       u.full_name as promoted_by_name
                FROM promotion_history ph
                JOIN students s ON ph.student_id = s.student_id
                LEFT JOIN users u ON ph.promoted_by = u.user_id
                WHERE 1=1
            """
            params = []
            
            if student_id:
                query += " AND ph.student_id = ?"
                params.append(student_id)
            
            query += " ORDER BY ph.promotion_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting promotion history: {e}")
            return []
    
    def create_promotion_rule(self, rule_name: str, min_cgpa: float = 2.0,
                             max_f_grades: int = 0, 
                             min_attendance_percentage: float = 75.0) -> Tuple[bool, str]:
        """Create a new promotion rule"""
        try:
            query = """
                INSERT INTO promotion_rules 
                (rule_name, min_cgpa, max_f_grades, min_attendance_percentage)
                VALUES (?, ?, ?, ?)
            """
            success, rule_id = db.execute_update(
                query, (rule_name, min_cgpa, max_f_grades, min_attendance_percentage)
            )
            
            if success:
                return True, f"Promotion rule created (ID: {rule_id})"
            return False, "Failed to create promotion rule"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_promotion_rules(self, is_active: bool = True) -> List[Dict]:
        """Get all promotion rules"""
        try:
            query = "SELECT * FROM promotion_rules WHERE 1=1"
            params = []
            
            if is_active is not None:
                query += " AND is_active = ?"
                params.append(1 if is_active else 0)
            
            query += " ORDER BY created_at DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting promotion rules: {e}")
            return []

# Global instance
promotion_controller = PromotionController()
