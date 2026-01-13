"""
Analytics Controller
Generates analytics data and statistics for visualization
"""
from database.db_manager import db
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

class AnalyticsController:
    """Controller for analytics and reporting"""
    
    def get_student_distribution_by_department(self) -> List[Dict]:
        """Get student count by department for pie/bar charts"""
        try:
            query = """
                SELECT d.department_name, d.department_code,
                       COUNT(s.student_id) as student_count,
                       SUM(CASE WHEN s.gender = 'Male' THEN 1 ELSE 0 END) as male_count,
                       SUM(CASE WHEN s.gender = 'Female' THEN 1 ELSE 0 END) as female_count
                FROM departments d
                LEFT JOIN students s ON d.department_id = s.department_id AND s.is_active = 1
                GROUP BY d.department_id
                ORDER BY student_count DESC
            """
            return db.execute_query(query)
        except Exception as e:
            print(f"Error getting student distribution: {e}")
            return []
    
    def get_performance_trends(self, department_id: int = None, months: int = 12) -> List[Dict]:
        """Get performance trends over time"""
        try:
            import config
            
            # Use MySQL-compatible syntax when using MySQL
            if config.USE_MYSQL:
                query = """
                    SELECT 
                        DATE_FORMAT(r.generated_at, '%%Y-%%m') as month,
                        AVG(r.cgpa) as avg_cgpa,
                        AVG(r.percentage) as avg_percentage,
                        COUNT(DISTINCT r.student_id) as student_count,
                        SUM(CASE WHEN r.status = 'Pass' THEN 1 ELSE 0 END) as pass_count,
                        SUM(CASE WHEN r.status = 'Fail' THEN 1 ELSE 0 END) as fail_count
                    FROM results r
                    JOIN students s ON r.student_id = s.student_id
                    WHERE r.generated_at >= DATE_SUB(NOW(), INTERVAL ? MONTH)
                """
            else:
                query = """
                    SELECT 
                        strftime('%Y-%m', r.generated_at) as month,
                        AVG(r.cgpa) as avg_cgpa,
                        AVG(r.percentage) as avg_percentage,
                        COUNT(DISTINCT r.student_id) as student_count,
                        SUM(CASE WHEN r.status = 'Pass' THEN 1 ELSE 0 END) as pass_count,
                        SUM(CASE WHEN r.status = 'Fail' THEN 1 ELSE 0 END) as fail_count
                    FROM results r
                    JOIN students s ON r.student_id = s.student_id
                    WHERE r.generated_at >= datetime('now', '-' || ? || ' months')
                """
            params = [months]
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            query += " GROUP BY month ORDER BY month"
            
            result = db.execute_query(query, tuple(params))
            return result if result else []
        except Exception as e:
            print(f"Error getting performance trends: {e}")
            return []
    
    def get_pass_fail_rates(self, department_id: int = None, semester: int = None) -> Dict:
        """Get pass/fail rates"""
        try:
            query = """
                SELECT 
                    COUNT(DISTINCT r.student_id) as total_students,
                    SUM(CASE WHEN r.status = 'Pass' THEN 1 ELSE 0 END) as passed,
                    SUM(CASE WHEN r.status = 'Fail' THEN 1 ELSE 0 END) as failed,
                    ROUND(CAST(SUM(CASE WHEN r.status = 'Pass' THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(DISTINCT r.student_id) * 100, 2) as pass_rate
                FROM results r
                JOIN students s ON r.student_id = s.student_id
                WHERE 1=1
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            if semester:
                query += " AND r.semester = ?"
                params.append(semester)
            
            result = db.execute_query(query, tuple(params))
            return result[0] if result else {}
        except Exception as e:
            print(f"Error getting pass/fail rates: {e}")
            return {}
    
    def get_attendance_statistics(self, department_id: int = None) -> List[Dict]:
        """Get attendance statistics by department"""
        try:
            query = """
                SELECT 
                    d.department_name,
                    COUNT(DISTINCT sa.student_id) as students_tracked,
                    COUNT(sa.attendance_id) as total_records,
                    SUM(CASE WHEN sa.status IN ('Present', 'Late') THEN 1 ELSE 0 END) as present_count,
                    ROUND(CAST(SUM(CASE WHEN sa.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(sa.attendance_id) * 100, 2) as avg_attendance_rate
                FROM departments d
                LEFT JOIN students s ON d.department_id = s.department_id
                LEFT JOIN student_attendance sa ON s.student_id = sa.student_id
                WHERE s.is_active = 1
            """
            params = []
            
            if department_id:
                query += " AND d.department_id = ?"
                params.append(department_id)
            
            query += " GROUP BY d.department_id HAVING total_records > 0"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting attendance statistics: {e}")
            return []
    
    def get_grade_distribution(self, department_id: int = None, semester: int = None) -> List[Dict]:
        """Get distribution of grades"""
        try:
            query = """
                SELECT 
                    r.overall_grade as grade,
                    COUNT(*) as count
                FROM results r
                JOIN students s ON r.student_id = s.student_id
                WHERE r.overall_grade IS NOT NULL
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            if semester:
                query += " AND r.semester = ?"
                params.append(semester)
            
            query += " GROUP BY r.overall_grade ORDER BY r.overall_grade"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting grade distribution: {e}")
            return []
    
    def get_top_performers(self, limit: int = 10, department_id: int = None) -> List[Dict]:
        """Get top performing students"""
        try:
            query = """
                SELECT s.roll_number, s.name, d.department_name, s.semester,
                       r.cgpa, r.overall_grade
                FROM students s
                JOIN departments d ON s.department_id = d.department_id
                JOIN results r ON s.student_id = r.student_id
                WHERE s.is_active = 1 AND r.cgpa IS NOT NULL
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            query += " ORDER BY r.cgpa DESC LIMIT ?"
            params.append(limit)
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting top performers: {e}")
            return []
    
    def get_course_performance(self, course_id: int = None) -> List[Dict]:
        """Get performance statistics by course"""
        try:
            query = """
                SELECT c.course_code, c.course_name, c.credits,
                       COUNT(DISTINCT m.student_id) as students_enrolled,
                       AVG(m.marks_obtained) as avg_marks,
                       SUM(CASE WHEN m.status = 'Pass' THEN 1 ELSE 0 END) as passed,
                       SUM(CASE WHEN m.status = 'Fail' THEN 1 ELSE 0 END) as failed,
                       ROUND(CAST(SUM(CASE WHEN m.status = 'Pass' THEN 1 ELSE 0 END) AS FLOAT) / 
                             COUNT(DISTINCT m.student_id) * 100, 2) as pass_rate
                FROM courses c
                LEFT JOIN marks m ON c.course_id = m.course_id
                WHERE c.is_active = 1
            """
            params = []
            
            if course_id:
                query += " AND c.course_id = ?"
                params.append(course_id)
            
            query += " GROUP BY c.course_id HAVING students_enrolled > 0"
            query += " ORDER BY pass_rate DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting course performance: {e}")
            return []
    
    def get_dashboard_summary(self) -> Dict:
        """Get comprehensive dashboard summary"""
        try:
            summary = {}
            
            # Student counts
            student_query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) as male,
                    SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) as female
                FROM students
            """
            student_data = db.execute_query(student_query)
            summary['students'] = student_data[0] if student_data else {}
            
            # Performance summary
            perf_query = """
                SELECT 
                    AVG(cgpa) as avg_cgpa,
                    AVG(percentage) as avg_percentage,
                    COUNT(DISTINCT student_id) as students_with_results
                FROM results
            """
            perf_data = db.execute_query(perf_query)
            summary['performance'] = perf_data[0] if perf_data else {}
            
            # Attendance summary
            att_query = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN status IN ('Present', 'Late') THEN 1 ELSE 0 END) as present,
                    ROUND(CAST(SUM(CASE WHEN status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(*) * 100, 2) as attendance_rate
                FROM student_attendance
            """
            att_data = db.execute_query(att_query)
            summary['attendance'] = att_data[0] if att_data else {}
            
            return summary
        except Exception as e:
            print(f"Error getting dashboard summary: {e}")
            return {}

# Global instance
analytics_controller = AnalyticsController()
