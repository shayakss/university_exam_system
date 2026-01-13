"""
Application Configuration
"""
import os
import json
from pathlib import Path

# Application Info
APP_NAME = "University Exam Result Management System"
APP_VERSION = "1.0.0"

# Load database configuration from config.json if it exists
def load_db_config():
    """Load database configuration from config.json"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config
        except Exception as e:
            print(f"Warning: Failed to load config.json: {e}")
            return None
    return None

# Database configuration
DB_CONFIG = load_db_config()
USE_MYSQL = DB_CONFIG and DB_CONFIG.get('use') == 'mysql'

# MySQL Configuration (if enabled)
if USE_MYSQL:
    MYSQL_HOST = DB_CONFIG.get('mysql_host', 'localhost')
    MYSQL_USER = DB_CONFIG.get('mysql_user', 'root')
    MYSQL_PASSWORD = DB_CONFIG.get('mysql_password', '')
    MYSQL_DATABASE = DB_CONFIG.get('mysql_database', 'exam_management')
    MYSQL_PORT = DB_CONFIG.get('mysql_port', 3306)

# University Information (CUSTOMIZE THIS FOR YOUR UNIVERSITY)
UNIVERSITY_NAME = "ABC University"  # ← Change this to your university name
UNIVERSITY_ADDRESS = "123 University Street, City, State - 12345"
UNIVERSITY_PHONE = "+1 (555) 123-4567"
UNIVERSITY_EMAIL = "info@abcuniversity.edu"
UNIVERSITY_WEBSITE = "www.abcuniversity.edu"

# Database Settings
# Database Settings
import sys
if getattr(sys, 'frozen', False):
    # Running as executable - use the directory of the exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script - use the directory of the script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "exam_system.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Security Settings
PASSWORD_MIN_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15
SESSION_TIMEOUT_MINUTES = 30

# Grading Scale Configuration (4.0 GPA System)
GRADING_SCALE = {
    'A+': {'min': 90, 'max': 100, 'points': 4.0},
    'A': {'min': 80, 'max': 89, 'points': 4.0},
    'B+': {'min': 70, 'max': 79, 'points': 3.5},
    'B': {'min': 60, 'max': 69, 'points': 3.0},
    'C+': {'min': 50, 'max': 59, 'points': 2.5},
    'C': {'min': 40, 'max': 49, 'points': 2.0},
    'F': {'min': 0, 'max': 39, 'points': 0.0}
}

# Default Admin Credentials (will be hashed)
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_FULLNAME = "System Administrator"

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
THEME_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"

# Report Settings
LOGO_PATH = os.path.join(BASE_DIR, "resources", "images", "university_logo.png")
SIGNATURE_PRINCIPAL = "Principal"
SIGNATURE_CONTROLLER = "Controller of Examinations"

# Auto Backup Settings
AUTO_BACKUP_ENABLED = True
AUTO_BACKUP_INTERVAL_DAYS = 7

# Create necessary directories
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "resources", "images"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "resources", "icons"), exist_ok=True)
