"""
Transcript Controller - Handles transcript data retrieval and PDF generation
"""
from typing import Tuple, List, Optional
from database.db_manager import db
from utils.pdf_generator import pdf_generator
import os


class TranscriptController:
    """Manages transcript operations"""
    
    def get_student_transcript_data(self, student_id: int) -> Tuple[Optional[dict], Optional[List[dict]]]:
        """
        Get complete transcript data for a student
        
        Returns:
            Tuple of (student_data, marks_data) or (None, None) if not found
        """
        try:
            print(f"[DEBUG] Fetching transcript for student_id: {student_id} (type: {type(student_id)})")
            
            # Get student information
            student_query = """
                SELECT s.*, d.department_name, d.department_code
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.department_id
                WHERE s.student_id = ?
            """
            student_result = db.execute_query(student_query, (student_id,))
            
            print(f"[DEBUG] Student query result: {student_result}")
            
            if not student_result or len(student_result) == 0:
                print(f"[DEBUG] No student found with ID: {student_id}")
                return None, None
            
            student_data = dict(student_result[0])
            print(f"[DEBUG] Student data retrieved: {student_data.get('name', 'Unknown')}")
            
            # Get all marks with course details
            marks_query = """
                SELECT 
                    c.course_name,
                    c.course_code,
                    c.credits,
                    c.semester,
                    c.max_marks as total_marks,
                    m.marks_obtained as obtained_marks,
                    m.grade,
                    m.status
                FROM marks m
                JOIN courses c ON m.course_id = c.course_id
                WHERE m.student_id = ?
                ORDER BY c.semester, c.course_name
            """
            marks_result = db.execute_query(marks_query, (student_id,))
            
            marks_data = [dict(row) for row in marks_result] if marks_result else []
            print(f"[DEBUG] Found {len(marks_data)} marks records")
            
            return student_data, marks_data
            
        except Exception as e:
            print(f"[ERROR] Error fetching transcript data: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def generate_transcript_pdf(self, student_id: int, output_path: str, university_data: dict = None) -> Tuple[bool, str]:
        """
        Generate transcript PDF for a student
        
        Args:
            student_id: Student ID
            output_path: Path to save PDF
            university_data: Optional university details
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Get transcript data
            student_data, marks_data = self.get_student_transcript_data(student_id)
            
            if not student_data:
                return False, "Student not found"
            
            if not marks_data:
                return False, "No marks data found for this student"
            
            # Generate PDF
            success = pdf_generator.generate_transcript(
                student_data=student_data,
                marks_data=marks_data,
                output_path=output_path,
                university_data=university_data
            )
            
            if success:
                return True, f"Transcript generated successfully: {output_path}"
            else:
                return False, "Failed to generate transcript PDF"
                
        except Exception as e:
            return False, f"Error generating transcript: {str(e)}"


# Global instance
transcript_controller = TranscriptController()
