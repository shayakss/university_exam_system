"""
Quick Test Script - Verify all imports and basic functionality
"""
import sys
print("=" * 60)
print("University Exam System - Import Test")
print("=" * 60)

try:
    print("\n✓ Testing Python version...")
    print(f"  Python {sys.version}")
    
    print("\n✓ Testing PyQt5...")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    print("  PyQt5 imported successfully")
    
    print("\n✓ Testing bcrypt...")
    import bcrypt
    print("  bcrypt imported successfully")
    
    print("\n✓ Testing reportlab...")
    from reportlab.lib.pagesizes import A4
    print("  reportlab imported successfully")
    
    print("\n✓ Testing pandas...")
    import pandas as pd
    print("  pandas imported successfully")
    
    print("\n✓ Testing openpyxl...")
    import openpyxl
    print("  openpyxl imported successfully")
    
    print("\n✓ Testing database module...")
    from database.db_manager import db
    print("  Database manager imported successfully")
    
    print("\n✓ Testing controllers...")
    from controllers.auth_controller import auth
    from controllers.student_controller import student_controller
    from controllers.department_controller import department_controller
    from controllers.course_controller import course_controller
    from controllers.marks_controller import marks_controller
    from controllers.result_controller import result_controller
    print("  All controllers imported successfully")
    
    print("\n✓ Testing utilities...")
    from utils.security import hash_password
    from utils.validators import validate_name
    from utils.pdf_generator import pdf_generator
    from utils.excel_exporter import excel_exporter
    print("  All utilities imported successfully")
    
    print("\n✓ Testing UI modules...")
    from ui.login_window import LoginWindow
    from ui.main_window import MainWindow
    print("  UI modules imported successfully")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe application is ready to run.")
    print("Execute: python main.py")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
