"""
Main Application Entry Point
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from database.db_manager import db
from controllers.auth_controller import auth
from utils.security import hash_password
from resources.styles.main_style import MAIN_STYLESHEET
import config
import matplotlib.axes
import matplotlib.transforms as mtransforms

# Global monkeypatch to permanently fix 'box_aspect' and 'fig_aspect' must be positive error
def patch_matplotlib():
    try:
        # 1. Patch shrunk_to_aspect in transforms
        _original_shrunk_to_aspect = mtransforms.BboxBase.shrunk_to_aspect
        def _safe_shrunk_to_aspect(self, box_aspect, container=None, fig_aspect=1.0):
            try:
                if box_aspect <= 0 or fig_aspect <= 0:
                    return container if container is not None else self
            except Exception:
                return container if container is not None else self
                
            try:
                return _original_shrunk_to_aspect(self, box_aspect, container, fig_aspect)
            except (ValueError, Exception):
                return container if container is not None else self
        
        mtransforms.BboxBase.shrunk_to_aspect = _safe_shrunk_to_aspect
        
        # 2. Patch apply_aspect in Axes as a double safety measure
        _original_apply_aspect = matplotlib.axes.Axes.apply_aspect
        def _safe_apply_aspect(self, position=None):
            try:
                return _original_apply_aspect(self, position)
            except ValueError:
                return
        matplotlib.axes.Axes.apply_aspect = _safe_apply_aspect
        print("✓ Matplotlib stability patches applied")
    except Exception as e:
        print(f"⚠ Could not apply Matplotlib patches: {e}")

# Apply patches immediately
patch_matplotlib()


def initialize_database():
    """Initialize database and create default admin user"""
    print("=" * 50)
    print("University Exam Result Management System")
    print("=" * 50)
    
    # Initialize schema
    if not db.table_exists('users'):
        print("\n📦 Initializing database...")
        if db.initialize_schema():
            # Create default admin user
            print("👤 Creating default admin user...")
            password_hash = hash_password(config.DEFAULT_ADMIN_PASSWORD)
            
            # Try with assigned_subject_id first (new schema)
            try:
                query = """
                    INSERT INTO users (username, password_hash, role, full_name, assigned_subject_id)
                    VALUES (?, ?, ?, ?, NULL)
                """
                success, user_id = db.execute_update(
                    query,
                    (config.DEFAULT_ADMIN_USERNAME, password_hash, 'Admin', config.DEFAULT_ADMIN_FULLNAME)
                )
            except Exception:
                # Fallback to old schema if column doesn't exist yet (shouldn't happen on fresh init but good for safety)
                query = """
                    INSERT INTO users (username, password_hash, role, full_name)
                    VALUES (?, ?, ?, ?)
                """
                success, user_id = db.execute_update(
                    query,
                    (config.DEFAULT_ADMIN_USERNAME, password_hash, 'Admin', config.DEFAULT_ADMIN_FULLNAME)
                )
            
            if success:
                print(f"✓ Default admin created: {config.DEFAULT_ADMIN_USERNAME}")
                print(f"  Password: {config.DEFAULT_ADMIN_PASSWORD}")
                print("  ⚠️  Please change the password after first login!")
            else:
                print("✗ Failed to create default admin user")
                from PyQt5.QtWidgets import QMessageBox
                # We need a dummy app to show message box if main app hasn't started
                if not QApplication.instance():
                    _ = QApplication(sys.argv)
                QMessageBox.critical(None, "Initialization Error", "Failed to create default admin user.")
        else:
            print("✗ Failed to initialize database schema")
            from PyQt5.QtWidgets import QMessageBox
            if not QApplication.instance():
                _ = QApplication(sys.argv)
            QMessageBox.critical(None, "Initialization Error", "Failed to initialize database schema.\nPlease check logs.")
    else:
        print("\n✓ Database already initialized")
    
    print("\n" + "=" * 50)


def main():
    """Main application entry point"""
    # Initialize database
    initialize_database()
    
    # Start automatic backup service
    try:
        from utils.backup_service import backup_service
        backup_service.start()
    except Exception as e:
        print(f"⚠ Backup service failed to start: {e}")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply stylesheet
    app.setStyleSheet(MAIN_STYLESHEET)
    
    # Import and show login window
    from ui.login_window import LoginWindow
    login_window = LoginWindow()
    login_window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
