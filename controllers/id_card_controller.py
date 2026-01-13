"""
ID Card Controller
Manages ID card generation with QR codes for students and staff
"""
from database.db_manager import db
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
import json

class IDCardController:
    """Controller for ID card generation and management"""
    
    def generate_card_number(self, card_type: str, entity_id: int) -> str:
        """Generate unique ID card number"""
        try:
            prefix = {
                'Student': 'STU',
                'Teacher': 'TCH',
                'Staff': 'STF'
            }.get(card_type, 'UNK')
            
            year = datetime.now().year
            return f"{prefix}{year}{entity_id:06d}"
        except Exception as e:
            print(f"Error generating card number: {e}")
            return f"{card_type[:3].upper()}{entity_id:08d}"
    
    def create_qr_data(self, card_type: str, entity_data: Dict) -> str:
        """Create QR code data string"""
        try:
            qr_data = {
                'type': card_type,
                'id': entity_data.get('id'),
                'name': entity_data.get('name'),
                'card_number': entity_data.get('card_number'),
                'issue_date': entity_data.get('issue_date'),
                'expiry_date': entity_data.get('expiry_date')
            }
            
            if card_type == 'Student':
                qr_data.update({
                    'roll_number': entity_data.get('roll_number'),
                    'department': entity_data.get('department'),
                    'semester': entity_data.get('semester')
                })
            
            return json.dumps(qr_data)
        except Exception as e:
            print(f"Error creating QR data: {e}")
            return ""
    
    def generate_student_id_card(self, student_id: int, generated_by: int,
                                 photo_path: str = None, 
                                 validity_years: int = 4) -> Tuple[bool, str, Dict]:
        """Generate ID card for a student"""
        try:
            # Get student details
            student_query = """
                SELECT s.*, d.department_name, d.department_code
                FROM students s
                JOIN departments d ON s.department_id = d.department_id
                WHERE s.student_id = ?
            """
            students = db.execute_query(student_query, (student_id,))
            
            if not students:
                return False, "Student not found", {}
            
            student = students[0]
            
            # Check if card already exists and is active
            existing_query = """
                SELECT card_id FROM id_cards
                WHERE student_id = ? AND is_active = 1
            """
            existing = db.execute_query(existing_query, (student_id,))
            
            if existing:
                return False, "Active ID card already exists for this student", {}
            
            # Generate card details
            card_number = self.generate_card_number('Student', student_id)
            issue_date = date.today()
            expiry_date = issue_date + timedelta(days=365 * validity_years)
            
            # Create QR code data
            qr_data = self.create_qr_data('Student', {
                'id': student_id,
                'name': student['name'],
                'roll_number': student['roll_number'],
                'department': student['department_name'],
                'semester': student['semester'],
                'card_number': card_number,
                'issue_date': str(issue_date),
                'expiry_date': str(expiry_date)
            })
            
            # Insert ID card record
            insert_query = """
                INSERT INTO id_cards
                (student_id, card_type, card_number, issue_date, expiry_date,
                 qr_code_data, photo_path, generated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, card_id = db.execute_update(
                insert_query,
                ('Student', card_number, issue_date, expiry_date, qr_data, photo_path, generated_by),
                (student_id,)
            )
            
            if success:
                card_details = {
                    'card_id': card_id,
                    'card_number': card_number,
                    'student_name': student['name'],
                    'roll_number': student['roll_number'],
                    'department': student['department_name'],
                    'semester': student['semester'],
                    'issue_date': str(issue_date),
                    'expiry_date': str(expiry_date),
                    'qr_data': qr_data
                }
                return True, "ID card generated successfully", card_details
            
            return False, "Failed to generate ID card", {}
            
        except Exception as e:
            return False, f"Error: {str(e)}", {}
    
    def generate_staff_id_card(self, user_id: int, generated_by: int,
                              photo_path: str = None,
                              validity_years: int = 5) -> Tuple[bool, str, Dict]:
        """Generate ID card for staff/teacher"""
        try:
            # Get user details
            user_query = "SELECT * FROM users WHERE user_id = ?"
            users = db.execute_query(user_query, (user_id,))
            
            if not users:
                return False, "User not found", {}
            
            user = users[0]
            
            # Determine card type
            card_type = 'Teacher' if user['role'] == 'Teacher' else 'Staff'
            
            # Check if card already exists
            existing_query = """
                SELECT card_id FROM id_cards
                WHERE user_id = ? AND is_active = 1
            """
            existing = db.execute_query(existing_query, (user_id,))
            
            if existing:
                return False, f"Active ID card already exists for this {card_type.lower()}", {}
            
            # Generate card details
            card_number = self.generate_card_number(card_type, user_id)
            issue_date = date.today()
            expiry_date = issue_date + timedelta(days=365 * validity_years)
            
            # Create QR code data
            qr_data = self.create_qr_data(card_type, {
                'id': user_id,
                'name': user['full_name'],
                'username': user['username'],
                'role': user['role'],
                'card_number': card_number,
                'issue_date': str(issue_date),
                'expiry_date': str(expiry_date)
            })
            
            # Insert ID card record
            insert_query = """
                INSERT INTO id_cards
                (user_id, card_type, card_number, issue_date, expiry_date,
                 qr_code_data, photo_path, generated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, card_id = db.execute_update(
                insert_query,
                (user_id, card_type, card_number, issue_date, expiry_date,
                 qr_data, photo_path, generated_by)
            )
            
            if success:
                card_details = {
                    'card_id': card_id,
                    'card_number': card_number,
                    'name': user['full_name'],
                    'role': user['role'],
                    'issue_date': str(issue_date),
                    'expiry_date': str(expiry_date),
                    'qr_data': qr_data
                }
                return True, "ID card generated successfully", card_details
            
            return False, "Failed to generate ID card", {}
            
        except Exception as e:
            return False, f"Error: {str(e)}", {}
    
    def deactivate_id_card(self, card_id: int) -> Tuple[bool, str]:
        """Deactivate an ID card"""
        try:
            query = "UPDATE id_cards SET is_active = 0 WHERE card_id = ?"
            success, _ = db.execute_update(query, (card_id,))
            
            if success:
                return True, "ID card deactivated successfully"
            return False, "Failed to deactivate ID card"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_id_cards(self, card_type: str = None, is_active: bool = True) -> List[Dict]:
        """Get ID cards with filters"""
        try:
            query = """
                SELECT ic.*, 
                       s.roll_number, s.name as student_name, d.department_name,
                       u.full_name as staff_name, u.role,
                       g.full_name as generated_by_name
                FROM id_cards ic
                LEFT JOIN students s ON ic.student_id = s.student_id
                LEFT JOIN departments d ON s.department_id = d.department_id
                LEFT JOIN users u ON ic.user_id = u.user_id
                LEFT JOIN users g ON ic.generated_by = g.user_id
                WHERE 1=1
            """
            params = []
            
            if card_type:
                query += " AND ic.card_type = ?"
                params.append(card_type)
            
            if is_active is not None:
                query += " AND ic.is_active = ?"
                params.append(1 if is_active else 0)
            
            query += " ORDER BY ic.created_at DESC"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting ID cards: {e}")
            return []
    
    def verify_qr_code(self, qr_data_str: str) -> Tuple[bool, str, Dict]:
        """Verify QR code data"""
        try:
            qr_data = json.loads(qr_data_str)
            
            # Verify card exists and is active
            query = """
                SELECT * FROM id_cards
                WHERE card_number = ? AND is_active = 1
            """
            cards = db.execute_query(query, (qr_data.get('card_number'),))
            
            if not cards:
                return False, "Invalid or inactive ID card", {}
            
            card = cards[0]
            
            # Check expiry
            if card['expiry_date']:
                expiry = datetime.strptime(card['expiry_date'], '%Y-%m-%d').date()
                if date.today() > expiry:
                    return False, "ID card has expired", {}
            
            return True, "ID card is valid", qr_data
            
        except Exception as e:
            return False, f"Error verifying QR code: {str(e)}", {}

# Global instance
id_card_controller = IDCardController()
