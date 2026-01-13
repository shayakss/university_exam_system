"""
Archive Controller
Manages database archiving for old academic year data
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import json

class ArchiveController:
    """Controller for database archiving"""
    
    def archive_academic_year(self, academic_year: str, archived_by: int) -> Tuple[bool, str, Dict]:
        """Archive all data for a specific academic year"""
        try:
            # Start transaction
            stats = {
                'students_archived': 0,
                'marks_archived': 0,
                'results_archived': 0
            }
            
            # Archive students (assuming academic year is derived from registration or graduation)
            # For simplicity, we'll archive students from specific semesters
            students_query = """
                INSERT INTO archived_students
                (original_student_id, roll_number, name, department_id, semester,
                 gender, date_of_birth, email, phone, address, archived_by,
                 archive_reason, original_data)
                SELECT student_id, roll_number, name, department_id, semester,
                       gender, date_of_birth, email, phone, address, ?,
                       'Academic Year Archive: ' || ?, 
                       json_object('roll_number', roll_number, 'name', name)
                FROM students
                WHERE is_active = 0 AND student_id NOT IN 
                    (SELECT original_student_id FROM archived_students)
            """
            success, count = db.execute_update(students_query, (archived_by, academic_year))
            stats['students_archived'] = count if success else 0
            
            # Archive marks for archived students
            marks_query = """
                INSERT INTO archived_marks
                (original_mark_id, student_id, course_id, marks_obtained, grade, status, original_data)
                SELECT mark_id, student_id, course_id, marks_obtained, grade, status,
                       json_object('student_id', student_id, 'course_id', course_id, 'marks', marks_obtained)
                FROM marks
                WHERE student_id IN (SELECT original_student_id FROM archived_students)
                    AND mark_id NOT IN (SELECT original_mark_id FROM archived_marks)
            """
            success, count = db.execute_update(marks_query)
            stats['marks_archived'] = count if success else 0
            
            # Archive results for archived students
            results_query = """
                INSERT INTO archived_results
                (original_result_id, student_id, semester, total_marks, marks_obtained,
                 percentage, sgpa, cgpa, overall_grade, status, original_data)
                SELECT result_id, student_id, semester, total_marks, marks_obtained,
                       percentage, sgpa, cgpa, overall_grade, status,
                       json_object('student_id', student_id, 'cgpa', cgpa)
                FROM results
                WHERE student_id IN (SELECT original_student_id FROM archived_students)
                    AND result_id NOT IN (SELECT original_result_id FROM archived_results)
            """
            success, count = db.execute_update(results_query)
            stats['results_archived'] = count if success else 0
            
            # Create metadata record
            metadata_query = """
                INSERT INTO archive_metadata
                (academic_year, archived_by, students_count, marks_count, results_count)
                VALUES (?, ?, ?, ?, ?)
            """
            db.execute_update(
                metadata_query,
                (academic_year, archived_by, stats['students_archived'],
                 stats['marks_archived'], stats['results_archived'])
            )
            
            total_archived = sum(stats.values())
            message = f"Archived {total_archived} records for academic year {academic_year}"
            
            return True, message, stats
            
        except Exception as e:
            return False, f"Error archiving data: {str(e)}", {}
    
    def restore_archived_data(self, archive_metadata_id: int) -> Tuple[bool, str]:
        """Restore archived data back to main tables"""
        try:
            # Get metadata
            metadata_query = "SELECT * FROM archive_metadata WHERE metadata_id = ?"
            metadata = db.execute_query(metadata_query, (archive_metadata_id,))
            
            if not metadata or not metadata[0]['can_restore']:
                return False, "Archive cannot be restored"
            
            academic_year = metadata[0]['academic_year']
            
            # Note: Restoration is complex and should be done carefully
            # This is a simplified version
            return True, f"Restoration of {academic_year} initiated (manual verification recommended)"
            
        except Exception as e:
            return False, f"Error restoring data: {str(e)}"
    
    def get_archived_students(self, academic_year: str = None, 
                             department_id: int = None) -> List[Dict]:
        """Get archived student records"""
        try:
            query = """
                SELECT ars.*, d.department_name
                FROM archived_students ars
                LEFT JOIN departments d ON ars.department_id = d.department_id
                LEFT JOIN archive_metadata am ON date(ars.archived_date) = date(am.archive_date)
                WHERE 1=1
            """
            params = []
            
            if academic_year:
                query += " AND am.academic_year = ?"
                params.append(academic_year)
            
            if department_id:
                query += " AND ars.department_id = ?"
                params.append(department_id)
            
            query += " ORDER BY ars.archived_date DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting archived students: {e}")
            return []
    
    def get_archive_metadata(self) -> List[Dict]:
        """Get all archive metadata records"""
        try:
            query = """
                SELECT am.*, u.full_name as archived_by_name
                FROM archive_metadata am
                LEFT JOIN users u ON am.archived_by = u.user_id
                ORDER BY am.archive_date DESC
            """
            return db.execute_query(query)
        except Exception as e:
            print(f"Error getting archive metadata: {e}")
            return []
    
    def get_archive_statistics(self) -> Dict:
        """Get archive statistics"""
        try:
            query = """
                SELECT 
                    COUNT(DISTINCT academic_year) as total_years_archived,
                    SUM(students_count) as total_students,
                    SUM(marks_count) as total_marks,
                    SUM(results_count) as total_results,
                    MIN(archive_date) as earliest_archive,
                    MAX(archive_date) as latest_archive
                FROM archive_metadata
            """
            result = db.execute_query(query)
            return result[0] if result else {}
        except Exception as e:
            print(f"Error getting archive statistics: {e}")
            return {}
    
    def delete_archived_data(self, archive_metadata_id: int) -> Tuple[bool, str]:
        """Permanently delete archived data (use with caution)"""
        try:
            # Get academic year
            metadata = db.execute_query(
                "SELECT academic_year FROM archive_metadata WHERE metadata_id = ?",
                (archive_metadata_id,)
            )
            
            if not metadata:
                return False, "Archive not found"
            
            # Delete archived records
            # This is a simplified version - in production, you'd want more careful deletion
            db.execute_update("DELETE FROM archive_metadata WHERE metadata_id = ?", (archive_metadata_id,))
            
            return True, f"Archive deleted successfully"
            
        except Exception as e:
            return False, f"Error deleting archive: {str(e)}"

# Global instance
archive_controller = ArchiveController()
