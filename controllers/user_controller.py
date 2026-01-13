"""
User Controller - Manages user CRUD operations
"""
from database.db_manager import DatabaseManager
from utils.security import hash_password, verify_password


class UserController:
    """Handles user management operations"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    
    def get_all_users(self):
        """Get all users"""
        query = """
            SELECT user_id, username, full_name, role, email, created_at, is_active, department_id, assigned_subject_id
            FROM users
            ORDER BY created_at DESC
        """
        return self.db.execute_query(query)
    
    def get_users_by_role(self, role):
        """Get all users with a specific role"""
        query = """
            SELECT user_id, username, full_name, role, email, created_at, is_active, department_id, assigned_subject_id
            FROM users
            WHERE role = ? AND is_active = 1
            ORDER BY full_name
        """
        return self.db.execute_query(query, (role,))
    
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = ?"
        results = self.db.execute_query(query, (user_id,))
        return results[0] if results else None
    
    
    def get_user_by_username(self, username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = ?"
        results = self.db.execute_query(query, (username,))
        return results[0] if results else None
    
    def create_user(self, username, password, full_name, role='Viewer', email=None, department_id=None, roll_number=None, assigned_subject_id=None):
        """Create a new user"""
        # Check if username already exists
        if self.get_user_by_username(username):
            return False, "Username already exists", None
        
        # Validate role
        valid_roles = ['Admin', 'DataEntry', 'Viewer', 'Teacher', 'Student']
        if role not in valid_roles:
            return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}", None
        
        # Email is required for Teacher and Student roles
        if role in ['Teacher', 'Student']:
            if not email or not email.strip():
                return False, f"Email is required for {role} role", None
            
            # Validate email format
            from utils.validators import validate_email
            is_valid, msg = validate_email(email)
            if not is_valid:
                return False, msg, None
        
        # Department is required for Teacher role
        if role == 'Teacher' and not department_id:
            return False, "Department is required for Teacher role", None
        
        # Roll number is required for Student role
        student_id = None
        if role == 'Student':
            if not roll_number or not roll_number.strip():
                return False, "Roll number is required for Student role", None
            
            # Find student by roll number
            from controllers.student_controller import student_controller
            students = student_controller.search_students(roll_number)
            
            matching_student = None
            for student in students:
                if student['roll_number'].lower() == roll_number.lower().strip():
                    matching_student = student
                    break
            
            if not matching_student:
                return False, f"No student found with roll number: {roll_number}", None
            
            student_id = matching_student['student_id']
            
            
            # Check if student already has a user account
            existing = self.db.execute_query("SELECT user_id FROM users WHERE student_id = ?", (student_id,))
            if existing:
                return False, "This student already has a user account", None
        
        # Validate password strength
        from utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength(password)
        if not is_valid:
            return False, msg, None
        
        # Hash password
        hashed_password = hash_password(password)
        
        query = """
            INSERT INTO users (username, password_hash, full_name, role, email, department_id, student_id, is_active, assigned_subject_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
        """
        
        try:
            success, user_id = self.db.execute_update(query, (username, hashed_password, full_name, role, email, department_id, student_id, assigned_subject_id))
            if success:
                return True, "User created successfully", user_id
            else:
                return False, "Failed to create user", None
        except Exception as e:
            return False, f"Failed to create user: {str(e)}", None


# Global user controller instance
user_controller = UserController()
