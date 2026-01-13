"""
Main Window - Dashboard and navigation
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTabWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.auth_controller import auth
import config


class MainWindow(QMainWindow):
    """Main application window with dashboard and navigation"""
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.load_user_theme()
        self.init_ui()
    
    def load_user_theme(self):
        """Load and apply user's theme preference"""
        from utils.theme_manager import theme_manager
        from PyQt5.QtWidgets import QApplication
        
        # Load user's theme preference
        saved_theme = theme_manager.load_user_preference(self.user_data['user_id'])
        theme_manager.set_theme(saved_theme)
        
        # Apply to application
        app = QApplication.instance()
        if app:
            app.setStyleSheet(theme_manager.get_theme(saved_theme))
    
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle(f"{config.APP_NAME}")
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header bar
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Import pages
        from ui.dashboard import ModernDashboard
        from ui.student_dashboard import StudentDashboard
        from ui.teacher_dashboard import TeacherDashboard
        from ui.my_results import MyResultsPage
        from ui.my_profile import MyProfilePage
        from ui.student_management import StudentManagementPage
        from ui.department_management import DepartmentManagementPage
        from ui.course_management import CourseManagementPage
        from ui.marks_entry import MarksEntryPage
        from ui.result_generation import ResultGenerationPage
        from ui.reports import ReportsPage
        from ui.backup_restore import BackupRestorePage
        from ui.user_management import UserManagementPage
        
        # Analytics Import (Keeping this one as requested)
        from ui.advanced_analytics import AdvancedAnalyticsPage
        
        # Add tabs based on role
        user_role = self.user_data['role']
        student_id = self.user_data.get('student_id')
        department_id = self.user_data.get('department_id')
        
        # STUDENT ROLE - Only own data
        if user_role == 'Student':
            if not student_id:
                QMessageBox.warning(self, "Error", "Student ID not found. Please contact administrator.")
                return
            
            self.tabs.addTab(StudentDashboard(self, student_id), "\U0001F4CA My Dashboard")
            self.tabs.addTab(MyResultsPage(self, student_id), "\U0001F4CB My Results")
            self.tabs.addTab(MyProfilePage(self, student_id, self.user_data), "\U0001F464 My Profile")
            
            # Keeping core student tabs
        
        # TEACHER ROLE - Department data only
        elif user_role == 'Teacher':
            assigned_subject_id = self.user_data.get('assigned_subject_id')
            
            if department_id:
                self.tabs.addTab(TeacherDashboard(self, department_id), "\U0001F4CA My Dashboard")
            else:
                self.tabs.addTab(ModernDashboard(self), "\U0001F4CA Dashboard")
            
            # Students (filtered by department)
            self.tabs.addTab(StudentManagementPage(self, department_id), "👥 My Students")
            
            # Only show Courses tab if teacher doesn't have an assigned subject
            if not assigned_subject_id:
                self.tabs.addTab(CourseManagementPage(self, department_id), "📚 Courses")
            
            # Marks Entry (filtered by department)
            self.tabs.addTab(MarksEntryPage(self, department_id), "✏️ Marks Entry")
            
            # Results (filtered by department)
            self.tabs.addTab(ResultGenerationPage(self, department_id), "📋 Results")
            
            # Only show Reports tab if teacher doesn't have an assigned subject
            if not assigned_subject_id:
                self.tabs.addTab(ReportsPage(self, department_id), "📈 Reports")
            
            # Keeping core teacher tabs
            self.tabs.addTab(AdvancedAnalyticsPage(self.user_data), "\U0001F4CA Analytics")
        
        # ADMIN & DATAENTRY ROLES - Full access
        else:
            # Dashboard (all users)
            self.tabs.addTab(ModernDashboard(self), "\U0001F4CA Dashboard")
            
            # All roles can view these
            self.tabs.addTab(StudentManagementPage(self), "\U0001F465 Students")
            self.tabs.addTab(DepartmentManagementPage(self), "\U0001F3DB Departments")
            self.tabs.addTab(CourseManagementPage(self), "\U0001F4DA Courses")
            
            # DataEntry and Admin can enter marks
            if user_role in ['Admin', 'DataEntry']:
                self.tabs.addTab(MarksEntryPage(self), "\u270F\uFE0F Marks Entry")
                self.tabs.addTab(ResultGenerationPage(self), "\U0001F4CB Results")
            
            # All roles can view reports
            self.tabs.addTab(ReportsPage(self), "📈 Reports")
            
            # Core Analytics for Admin/DataEntry
            self.tabs.addTab(AdvancedAnalyticsPage(self.user_data), "\U0001F4CA Analytics")
            
            # Admin only features
            if user_role == 'Admin':
                self.tabs.addTab(BackupRestorePage(self), "💾 Backup")
                self.tabs.addTab(UserManagementPage(self), "👤 Users")
                
                # Keeping core admin tabs
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background-color: #1e293b;
                color: white;
                padding: 8px;
                font-size: 12px;
            }}
        """)
        self.statusBar().showMessage(
            f"  👤 {self.user_data['full_name']} ({self.user_data['role']})"
        )
    
    def create_header(self):
        """Create professional header bar"""
        header = QWidget()
        header.setStyleSheet(f"""
            QWidget {{
                background-color: #1e293b;
            }}
        """)
        header.setFixedHeight(70)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # App title
        title = QLabel(config.APP_NAME)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: white;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # User info
        user_label = QLabel(f"Welcome, {self.user_data['full_name']}")
        user_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            padding-right: 15px;
        """)
        layout.addWidget(user_label)
        
        # Theme toggle button
        from utils.theme_manager import theme_manager
        current_theme = theme_manager.get_current_theme()
        theme_text = "\u2600\uFE0F Light Mode" if current_theme == 'Dark' else "\U0001F319 Dark Mode"
        
        self.theme_btn = QPushButton(theme_text)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: 600;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # Logout button
        logout_btn = QPushButton("\U0001F6AA Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return header
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, 'Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            auth.logout()
            self.close()
            
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        from utils.theme_manager import theme_manager
        from PyQt5.QtWidgets import QApplication
        
        # Get current theme
        current = theme_manager.get_current_theme()
        
        # Toggle to opposite theme
        if current == 'Light':
            new_theme = 'Dark'
            self.theme_btn.setText("☀️ Light Mode")
        else:
            new_theme = 'Light'
            self.theme_btn.setText("🌙 Dark Mode")
        
        # Apply theme
        theme_manager.set_theme(new_theme)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(theme_manager.get_theme(new_theme))
        
        # Save preference
        theme_manager.save_user_preference(self.user_data['user_id'], new_theme)

