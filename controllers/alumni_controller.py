"""
Alumni Controller
Manages alumni database and employment tracking
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class AlumniController:
    """Controller for alumni management"""
    
    def move_to_alumni(self, student_id: int, graduation_year: int,
                      graduation_date: date, final_cgpa: float, final_grade: str,
                      current_status: str = 'Unemployed') -> Tuple[bool, str]:
        """Move a graduated student to alumni database"""
        try:
            # Check if student exists
            student_query = "SELECT * FROM students WHERE student_id = ?"
            students = db.execute_query(student_query, (student_id,))
            
            if not students:
                return False, "Student not found"
            
            student = students[0]
            
            # Check if already in alumni
            alumni_check = "SELECT alumni_id FROM alumni WHERE student_id = ?"
            existing = db.execute_query(alumni_check, (student_id,))
            
            if existing:
                return False, "Student is already in alumni database"
            
            # Insert into alumni
            insert_query = """
                INSERT INTO alumni
                (student_id, graduation_year, graduation_date, final_cgpa, final_grade,
                 current_status, contact_email, contact_phone, current_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, alumni_id = db.execute_update(
                insert_query,
                (student_id, graduation_year, graduation_date, final_cgpa, final_grade,
                 current_status, student.get('email'), student.get('phone'), student.get('address'))
            )
            
            if success:
                # Optionally deactivate student record
                db.execute_update("UPDATE students SET is_active = 0 WHERE student_id = ?", (student_id,))
                return True, f"Student moved to alumni database (Alumni ID: {alumni_id})"
            
            return False, "Failed to move student to alumni"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def add_employment_record(self, alumni_id: int, company_name: str, job_title: str,
                             start_date: date, end_date: date = None, is_current: bool = False,
                             salary_range: str = None, location: str = None) -> Tuple[bool, str]:
        """Add employment record for an alumnus"""
        try:
            # If marking as current, unmark other current employments
            if is_current:
                db.execute_update(
                    "UPDATE alumni_employment SET is_current = 0 WHERE alumni_id = ?",
                    (alumni_id,)
                )
            
            query = """
                INSERT INTO alumni_employment
                (alumni_id, company_name, job_title, start_date, end_date,
                 is_current, salary_range, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, emp_id = db.execute_update(
                query,
                (alumni_id, company_name, job_title, start_date, end_date,
                 1 if is_current else 0, salary_range, location)
            )
            
            if success:
                # Update alumni current status
                if is_current:
                    db.execute_update(
                        "UPDATE alumni SET current_status = 'Employed' WHERE alumni_id = ?",
                        (alumni_id,)
                    )
                return True, f"Employment record added (ID: {emp_id})"
            
            return False, "Failed to add employment record"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def update_alumni_info(self, alumni_id: int, **kwargs) -> Tuple[bool, str]:
        """Update alumni information"""
        try:
            update_fields = []
            params = []
            
            allowed_fields = ['current_status', 'contact_email', 'contact_phone', 'current_address']
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    params.append(value)
            
            if not update_fields:
                return False, "No valid fields to update"
            
            params.append(alumni_id)
            query = f"UPDATE alumni SET {', '.join(update_fields)} WHERE alumni_id = ?"
            
            success, _ = db.execute_update(query, tuple(params))
            
            if success:
                return True, "Alumni information updated successfully"
            return False, "Failed to update alumni information"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def search_alumni(self, graduation_year: int = None, department_id: int = None,
                     current_status: str = None, search_term: str = None) -> List[Dict]:
        """Search alumni with various filters"""
        try:
            query = """
                SELECT a.*, s.roll_number, s.name, s.gender, s.email as student_email,
                       d.department_name, d.department_code
                FROM alumni a
                JOIN students s ON a.student_id = s.student_id
                JOIN departments d ON s.department_id = d.department_id
                WHERE 1=1
            """
            params = []
            
            if graduation_year:
                query += " AND a.graduation_year = ?"
                params.append(graduation_year)
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            if current_status:
                query += " AND a.current_status = ?"
                params.append(current_status)
            
            if search_term:
                query += " AND (s.name LIKE ? OR s.roll_number LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern])
            
            query += " ORDER BY a.graduation_year DESC, s.name"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error searching alumni: {e}")
            return []
    
    def get_alumni_employment_history(self, alumni_id: int) -> List[Dict]:
        """Get employment history for an alumnus"""
        try:
            query = """
                SELECT * FROM alumni_employment
                WHERE alumni_id = ?
                ORDER BY is_current DESC, start_date DESC
            """
            return db.execute_query(query, (alumni_id,))
        except Exception as e:
            print(f"Error getting employment history: {e}")
            return []
    
    def get_alumni_statistics(self, department_id: int = None) -> Dict:
        """Get alumni statistics"""
        try:
            query = """
                SELECT 
                    COUNT(DISTINCT a.alumni_id) as total_alumni,
                    COUNT(DISTINCT CASE WHEN a.current_status = 'Employed' THEN a.alumni_id END) as employed,
                    COUNT(DISTINCT CASE WHEN a.current_status = 'Self-Employed' THEN a.alumni_id END) as self_employed,
                    COUNT(DISTINCT CASE WHEN a.current_status = 'Higher Studies' THEN a.alumni_id END) as higher_studies,
                    COUNT(DISTINCT CASE WHEN a.current_status = 'Unemployed' THEN a.alumni_id END) as unemployed,
                    AVG(a.final_cgpa) as avg_cgpa,
                    MIN(a.graduation_year) as earliest_year,
                    MAX(a.graduation_year) as latest_year
                FROM alumni a
                JOIN students s ON a.student_id = s.student_id
                WHERE 1=1
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            result = db.execute_query(query, tuple(params))
            return result[0] if result else {}
        except Exception as e:
            print(f"Error getting alumni statistics: {e}")
            return {}
    
    def get_alumni_by_year(self, graduation_year: int) -> List[Dict]:
        """Get all alumni from a specific graduation year"""
        try:
            query = """
                SELECT a.*, s.roll_number, s.name, d.department_name
                FROM alumni a
                JOIN students s ON a.student_id = s.student_id
                JOIN departments d ON s.department_id = d.department_id
                WHERE a.graduation_year = ?
                ORDER BY s.name
            """
            return db.execute_query(query, (graduation_year,))
        except Exception as e:
            print(f"Error getting alumni by year: {e}")
            return []
    
    def get_top_performers(self, limit: int = 10, graduation_year: int = None) -> List[Dict]:
        """Get top performing alumni based on CGPA"""
        try:
            query = """
                SELECT a.*, s.roll_number, s.name, d.department_name
                FROM alumni a
                JOIN students s ON a.student_id = s.student_id
                JOIN departments d ON s.department_id = d.department_id
                WHERE a.final_cgpa IS NOT NULL
            """
            params = []
            
            if graduation_year:
                query += " AND a.graduation_year = ?"
                params.append(graduation_year)
            
            query += " ORDER BY a.final_cgpa DESC LIMIT ?"
            params.append(limit)
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting top performers: {e}")
            return []

# Global instance
alumni_controller = AlumniController()
