"""
Validation utilities for input data
"""
from typing import Tuple, Optional
from datetime import datetime
import re


def validate_roll_number(roll_number: str) -> Tuple[bool, str]:
    """Validate roll number format"""
    if not roll_number or not roll_number.strip():
        return False, "Roll number is required"
    if len(roll_number.strip()) < 3:
        return False, "Roll number must be at least 3 characters"
    if len(roll_number.strip()) > 20:
        return False, "Roll number must not exceed 20 characters"
    return True, "Valid"


def validate_name(name: str) -> Tuple[bool, str]:
    """Validate person name"""
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    
    if not re.match(r'^[A-Za-z\s\.]+$', name):
        return False, "Name can only contain letters, spaces, and dots"
    
    return True, "Valid name"


def validate_semester(semester: int) -> Tuple[bool, str]:
    """Validate semester number"""
    if semester < 1 or semester > 8:
        return False, "Semester must be between 1 and 8"
    
    return True, "Valid semester"


def validate_date(date_string: str) -> Tuple[bool, Optional[datetime], str]:
    """
    Validate and parse date string
    
    Args:
        date_string: Date in format YYYY-MM-DD
    
    Returns:
        Tuple of (is_valid: bool, parsed_date: datetime, message: str)
    """
    try:
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
        
        # Check if date is not in future
        if parsed_date > datetime.now():
            return False, None, "Date cannot be in the future"
        
        # Check if date is reasonable (not too old)
        if parsed_date.year < 1950:
            return False, None, "Date is too old"
        
        return True, parsed_date, "Valid date"
    except ValueError:
        return False, None, "Invalid date format. Use YYYY-MM-DD"


def validate_credits(credits: int) -> Tuple[bool, str]:
    """Validate course credits"""
    if credits < 1 or credits > 10:
        return False, "Credits must be between 1 and 10"
    
    return True, "Valid credits"


def validate_department_code(code: str) -> Tuple[bool, str]:
    """Validate department code"""
    if not code or len(code.strip()) < 2:
        return False, "Department code must be at least 2 characters"
    
    if len(code.strip()) > 10:
        return False, "Department code must not exceed 10 characters"
    
    if not re.match(r'^[A-Z0-9]+$', code.upper()):
        return False, "Department code can only contain uppercase letters and numbers"
    
    return True, "Valid department code"


def validate_course_code(code: str) -> Tuple[bool, str]:
    """Validate course code"""
    if not code or len(code) < 3 or len(code) > 15:
        return False, "Course code must be 3-15 characters"
    
    if not re.match(r'^[A-Z0-9\-]+$', code.upper()):
        return False, "Course code can only contain uppercase letters, numbers, and hyphens"
    
    return True, "Valid course code"


def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username"""
    if not username or len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Valid username"


def validate_gender(gender: str) -> Tuple[bool, str]:
    """Validate gender"""
    valid_genders = ['Male', 'Female', 'Other']
    if gender not in valid_genders:
        return False, f"Gender must be one of: {', '.join(valid_genders)}"
    
    return True, "Valid gender"


def validate_role(role: str) -> Tuple[bool, str]:
    """Validate user role"""
    valid_roles = ['Admin', 'DataEntry', 'Viewer', 'Teacher', 'Student']
    if role not in valid_roles:
        return False, f"Role must be one of: {', '.join(valid_roles)}"
    
    return True, "Valid role"


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not email or not email.strip():
        return False, "Email is required"
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email.strip()):
        return False, "Invalid email format"
    
    return True, "Valid email"


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    
    Args:
        password: Password to validate
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Strong password"
