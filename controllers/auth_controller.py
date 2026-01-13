"""
Authentication Controller - Handles user authentication and session management
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from database.db_manager import db
from utils.security import hash_password, verify_password
import config


class AuthController:
    """Handles user authentication and authorization"""
    
    def __init__(self):
        self.current_user = None
        self.session_start = None
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Authenticate user and create session
        
        Args:
            username: Username
            password: Password
        
        Returns:
            Tuple of (success: bool, message: str, user_data: dict)
        """
        # Validate input
        if not username or not password:
            return False, "Username and password are required", None
        
        # Get user from database
        query = """
            SELECT user_id, username, password_hash, role, full_name, 
                   is_active, failed_login_attempts, is_locked, email, department_id, student_id, assigned_subject_id
            FROM users 
            WHERE username = ?
        """
        result = db.execute_query(query, (username,))
        
        if not result or len(result) == 0:
            return False, "Invalid username or password", None
        
        user = dict(result[0])
        
        # Check if account is active
        if not user['is_active']:
            return False, "Account is disabled. Contact administrator.", None
        
        # Check if account is locked
        if user.get('is_locked', 0):
            return False, "Account is locked. Contact administrator.", None
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            # Increment failed login attempts
            failed_attempts = user.get('failed_login_attempts', 0) + 1
            self._record_failed_login(user['user_id'], failed_attempts)
            
            # Lock account if max attempts reached
            if failed_attempts >= 5:
                self._lock_account(user['user_id'])
                return False, "Too many failed login attempts. Account locked.", None
            
            remaining = 5 - failed_attempts
            return False, f"Invalid username or password. {remaining} attempts remaining.", None
        
        # Successful login - reset failed attempts
        self._reset_failed_attempts(user['user_id'])
        
        # Update last login time
        self._update_last_login(user['user_id'])
        
        # Create session
        self.current_user = {
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
            'full_name': user['full_name'],
            'email': user.get('email'),
            'department_id': user.get('department_id'),
            'student_id': user.get('student_id'),
            'assigned_subject_id': user.get('assigned_subject_id')
        }
        self.session_start = datetime.now()
        
        return True, "Login successful", self.current_user
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.session_start = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if not self.current_user or not self.session_start:
            return False
        
        # Check session timeout (8 hours)
        session_duration = datetime.now() - self.session_start
        if session_duration > timedelta(hours=8):
            self.logout()
            return False
        
        return True
    
    def has_permission(self, required_role: str) -> bool:
        """
        Check if current user has required permission
        
        Role hierarchy: Admin > DataEntry > Viewer
        """
        if not self.is_authenticated():
            return False
        
        role_hierarchy = {'Admin': 3, 'DataEntry': 2, 'Viewer': 1, 'Teacher': 1, 'Student': 1}
        current_role_level = role_hierarchy.get(self.current_user['role'], 0)
        required_role_level = role_hierarchy.get(required_role, 0)
        
        return current_role_level >= required_role_level
    
    def _record_failed_login(self, user_id: int, attempts: int):
        """Record failed login attempt"""
        query = "UPDATE users SET failed_login_attempts = ? WHERE user_id = ?"
        success, _ = db.execute_update(query, (attempts, user_id))
    
    def _reset_failed_attempts(self, user_id: int):
        """Reset failed login attempts"""
        query = "UPDATE users SET failed_login_attempts = 0, is_locked = 0 WHERE user_id = ?"
        success, _ = db.execute_update(query, (user_id,))
    
    def _lock_account(self, user_id: int):
        """Lock user account"""
        query = "UPDATE users SET is_locked = 1 WHERE user_id = ?"
        success, _ = db.execute_update(query, (user_id,))
    
    def _update_last_login(self, user_id: int):
        """Update last login timestamp"""
        query = "UPDATE users SET last_login = ? WHERE user_id = ?"
        success, _ = db.execute_update(query, (datetime.now().isoformat(), user_id))
    
    def get_current_user(self) -> Optional[dict]:
        """Get current authenticated user"""
        return self.current_user if self.is_authenticated() else None


# Global auth controller instance
auth = AuthController()
