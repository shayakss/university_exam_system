"""
Security utilities for password hashing, validation, and input sanitization
"""
import bcrypt
import re
from typing import Tuple


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password to verify
        hashed_password: Stored hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Args:
        password: Password to validate
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"


def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent SQL injection and XSS
    
    Args:
        input_string: User input string
    
    Returns:
        Sanitized string
    """
    if input_string is None:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = input_string.strip()
    
    # Remove SQL comment markers
    sanitized = sanitized.replace("--", "")
    sanitized = sanitized.replace("/*", "")
    sanitized = sanitized.replace("*/", "")
    
    return sanitized


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (11 digits)
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's 11 digits
    pattern = r'^\d{11}$'
    return bool(re.match(pattern, cleaned))


def validate_roll_number(roll_number: str) -> Tuple[bool, str]:
    """
    Validate roll number format
    
    Args:
        roll_number: Roll number to validate
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not roll_number or len(roll_number) < 3:
        return False, "Roll number must be at least 3 characters"
    
    # Allow alphanumeric with hyphens and underscores
    if not re.match(r'^[A-Za-z0-9\-_]+$', roll_number):
        return False, "Roll number can only contain letters, numbers, hyphens, and underscores"
    
    return True, "Valid roll number"


def validate_marks(marks: float, max_marks: float) -> Tuple[bool, str]:
    """
    Validate marks value
    
    Args:
        marks: Marks obtained
        max_marks: Maximum marks possible
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if marks < 0:
        return False, "Marks cannot be negative"
    
    if marks > max_marks:
        return False, f"Marks cannot exceed maximum marks ({max_marks})"
    
    return True, "Valid marks"
