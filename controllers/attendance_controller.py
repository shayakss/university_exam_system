"""
Attendance Controller
Manages student and teacher attendance tracking
"""
from database.db_manager import db
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

class AttendanceController:
    """Controller for attendance management"""
    
    def mark_student_attendance(self, student_id: int, course_id: Optional[int], 
                               attendance_date: date, status: str, marked_by: int,
                               remarks: str = None) -> Tuple[bool, str]:
        """Mark attendance for a student"""
        try:
            # Check if attendance already marked
            check_query = """
                SELECT attendance_id FROM student_attendance
                WHERE student_id = ? AND course_id = ? AND attendance_date = ?
            """
            existing = db.execute_query(check_query, (student_id, course_id, attendance_date))
            
            if existing:
                # Update existing
                query = """
                    UPDATE student_attendance
                    SET status = ?, marked_by = ?, remarks = ?
                    WHERE student_id = ? AND course_id = ? AND attendance_date = ?
                """
                success, _ = db.execute_update(
                    query, (status, marked_by, remarks, student_id, course_id, attendance_date)
                )
            else:
                # Insert new
                query = """
                    INSERT INTO student_attendance 
                    (student_id, course_id, attendance_date, status, marked_by, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                success, _ = db.execute_update(
                    query, (student_id, course_id, attendance_date, status, marked_by, remarks)
                )
            
            if success:
                return True, "Attendance marked successfully"
            return False, "Failed to mark attendance"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def mark_bulk_attendance(self, student_ids: List[int], course_id: Optional[int],
                            attendance_date: date, status: str, marked_by: int) -> Tuple[bool, str]:
        """Mark attendance for multiple students at once"""
        try:
            success_count = 0
            for student_id in student_ids:
                success, _ = self.mark_student_attendance(
                    student_id, course_id, attendance_date, status, marked_by
                )
                if success:
                    success_count += 1
            
            return True, f"Marked attendance for {success_count}/{len(student_ids)} students"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_student_attendance(self, student_id: int, start_date: date = None,
                              end_date: date = None, course_id: int = None) -> List[Dict]:
        """Get attendance records for a student"""
        try:
            query = """
                SELECT sa.*, c.course_name, c.course_code, u.full_name as marked_by_name
                FROM student_attendance sa
                LEFT JOIN courses c ON sa.course_id = c.course_id
                LEFT JOIN users u ON sa.marked_by = u.user_id
                WHERE sa.student_id = ?
            """
            params = [student_id]
            
            if start_date:
                query += " AND sa.attendance_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND sa.attendance_date <= ?"
                params.append(end_date)
            if course_id:
                query += " AND sa.course_id = ?"
                params.append(course_id)
            
            query += " ORDER BY sa.attendance_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting student attendance: {e}")
            return []
    
    def calculate_attendance_percentage(self, student_id: int, course_id: int = None,
                                       start_date: date = None, end_date: date = None) -> float:
        """Calculate attendance percentage for a student"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status IN ('Present', 'Late') THEN 1 ELSE 0 END) as present
                FROM student_attendance
                WHERE student_id = ?
            """
            params = [student_id]
            
            if course_id:
                query += " AND course_id = ?"
                params.append(course_id)
            if start_date:
                query += " AND attendance_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND attendance_date <= ?"
                params.append(end_date)
            
            result = db.execute_query(query, tuple(params))
            if result and result[0]['total'] > 0:
                return (result[0]['present'] / result[0]['total']) * 100
            return 0.0
        except Exception as e:
            print(f"Error calculating attendance: {e}")
            return 0.0
    
    def get_low_attendance_students(self, threshold: float = 75.0, 
                                   department_id: int = None,
                                   semester: int = None) -> List[Dict]:
        """Get students with attendance below threshold"""
        try:
            query = """
                SELECT 
                    s.student_id, s.roll_number, s.name,
                    d.department_name, s.semester,
                    COUNT(sa.attendance_id) as total_days,
                    SUM(CASE WHEN sa.status IN ('Present', 'Late') THEN 1 ELSE 0 END) as present_days,
                    ROUND(CAST(SUM(CASE WHEN sa.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(sa.attendance_id) * 100, 2) as attendance_percentage
                FROM students s
                LEFT JOIN student_attendance sa ON s.student_id = sa.student_id
                LEFT JOIN departments d ON s.department_id = d.department_id
                WHERE s.is_active = 1
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            if semester:
                query += " AND s.semester = ?"
                params.append(semester)
            
            query += """
                GROUP BY s.student_id
                HAVING attendance_percentage < ? AND total_days > 0
                ORDER BY attendance_percentage ASC
            """
            params.append(threshold)
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting low attendance students: {e}")
            return []
    
    def get_attendance_report(self, department_id: int = None, semester: int = None,
                             start_date: date = None, end_date: date = None) -> List[Dict]:
        """Generate attendance report"""
        try:
            if not start_date:
                start_date = date.today() - timedelta(days=30)
            if not end_date:
                end_date = date.today()
            
            query = """
                SELECT 
                    s.student_id, s.roll_number, s.name,
                    d.department_name, s.semester,
                    COUNT(sa.attendance_id) as total_days,
                    SUM(CASE WHEN sa.status = 'Present' THEN 1 ELSE 0 END) as present,
                    SUM(CASE WHEN sa.status = 'Absent' THEN 1 ELSE 0 END) as absent,
                    SUM(CASE WHEN sa.status = 'Leave' THEN 1 ELSE 0 END) as leave,
                    SUM(CASE WHEN sa.status = 'Late' THEN 1 ELSE 0 END) as late,
                    ROUND(CAST(SUM(CASE WHEN sa.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(sa.attendance_id) * 100, 2) as percentage
                FROM students s
                LEFT JOIN student_attendance sa ON s.student_id = sa.student_id
                LEFT JOIN departments d ON s.department_id = d.department_id
                WHERE s.is_active = 1
                    AND sa.attendance_date BETWEEN ? AND ?
            """
            params = [start_date, end_date]
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            if semester:
                query += " AND s.semester = ?"
                params.append(semester)
            
            query += " GROUP BY s.student_id ORDER BY s.roll_number"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error generating attendance report: {e}")
            return []
    
    def mark_teacher_attendance(self, user_id: int, attendance_date: date,
                               status: str, marked_by: int, remarks: str = None) -> Tuple[bool, str]:
        """Mark attendance for a teacher"""
        try:
            # Check if already marked
            check_query = """
                SELECT attendance_id FROM teacher_attendance
                WHERE user_id = ? AND attendance_date = ?
            """
            existing = db.execute_query(check_query, (user_id, attendance_date))
            
            if existing:
                query = """
                    UPDATE teacher_attendance
                    SET status = ?, marked_by = ?, remarks = ?
                    WHERE user_id = ? AND attendance_date = ?
                """
                success, _ = db.execute_update(
                    query, (status, marked_by, remarks, user_id, attendance_date)
                )
            else:
                query = """
                    INSERT INTO teacher_attendance
                    (user_id, attendance_date, status, marked_by, remarks)
                    VALUES (?, ?, ?, ?, ?)
                """
                success, _ = db.execute_update(
                    query, (user_id, attendance_date, status, marked_by, remarks)
                )
            
            if success:
                return True, "Teacher attendance marked successfully"
            return False, "Failed to mark teacher attendance"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_teacher_attendance(self, user_id: int = None, start_date: date = None,
                              end_date: date = None) -> List[Dict]:
        """Get teacher attendance records"""
        try:
            query = """
                SELECT ta.*, u.full_name, u.username, m.full_name as marked_by_name
                FROM teacher_attendance ta
                LEFT JOIN users u ON ta.user_id = u.user_id
                LEFT JOIN users m ON ta.marked_by = m.user_id
                WHERE 1=1
            """
            params = []
            
            if user_id:
                query += " AND ta.user_id = ?"
                params.append(user_id)
            if start_date:
                query += " AND ta.attendance_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND ta.attendance_date <= ?"
                params.append(end_date)
            
            query += " ORDER BY ta.attendance_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting teacher attendance: {e}")
            return []

    def get_attendance_statistics(self, department_id: int = None, semester: int = None) -> Dict:
        """Get overall attendance statistics"""
        try:
            query = """
                SELECT 
                    COUNT(sa.attendance_id) as total_records,
                    SUM(CASE WHEN sa.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                    SUM(CASE WHEN sa.status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
                    SUM(CASE WHEN sa.status = 'Leave' THEN 1 ELSE 0 END) as leave_count,
                    SUM(CASE WHEN sa.status = 'Late' THEN 1 ELSE 0 END) as late_count
                FROM student_attendance sa
                LEFT JOIN students s ON sa.student_id = s.student_id
                WHERE 1=1
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            if semester:
                query += " AND s.semester = ?"
                params.append(semester)
            
            result = db.execute_query(query, tuple(params))
            
            if result and result[0]['total_records'] > 0:
                stats = result[0]
                present_plus_late = stats['present_count'] + stats['late_count']
                stats['average_percentage'] = (present_plus_late / stats['total_records']) * 100
                return stats
            
            return {
                'total_records': 0,
                'present_count': 0,
                'absent_count': 0,
                'leave_count': 0,
                'late_count': 0,
                'average_percentage': 0.0
            }
        except Exception as e:
            print(f"Error getting attendance statistics: {e}")
            return {}

# Global instance
attendance_controller = AttendanceController()
