"""
Feature Launcher UI
Hub for accessing all new features
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.attendance_management import AttendanceManagement
from ui.timetable_management import TimetableManagement
from ui.ai_insights import AIInsightsPage
from ui.assignment_management import AssignmentManagementPage
from ui.student_promotion import StudentPromotionPage
from ui.id_card_generator import IDCardGeneratorPage
from ui.alumni_management import AlumniManagementPage
from ui.rbac_editor import RBACEditorPage
from ui.audit_viewer import AuditViewerPage
from ui.archive_manager import ArchiveManagerPage
from ui.cloud_backup_settings import CloudBackupSettingsPage
from ui.advanced_analytics import AdvancedAnalyticsPage
from ui.report_builder import ReportBuilderPage

class FeatureLauncher(QWidget):
    """Hub for accessing new features"""
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("🚀 Extra Features")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2C3E50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Scroll Area for many features
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Grid for feature cards
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # Define features with role access control
        # Format: (Name, Description, Icon, Handler, Allowed Roles)
        all_features = [
            ("📅 Attendance Manager", "Mark and track attendance", "attendance_icon.png", self.open_attendance, ['Admin', 'Teacher', 'DataEntry']),
            ("📅 Timetable Manager", "Class and exam scheduling", "timetable_icon.png", self.open_timetable, ['Admin', 'Teacher', 'Student', 'DataEntry']),
            ("📝 Assignment Manager", "Create and grade assignments", "assignment_icon.png", self.open_assignments, ['Admin', 'Teacher', 'Student']),
            ("🤖 AI Insights", "Student risk analysis & predictions", "ai_icon.png", self.open_ai_insights, ['Admin', 'Teacher']),
            ("🎓 Student Promotion", "Automate semester promotions", "promotion_icon.png", self.open_promotion, ['Admin']),
            ("🪪 ID Card Generator", "Generate QR-coded ID cards", "id_card_icon.png", self.open_id_cards, ['Admin', 'DataEntry']),
            ("🎓 Alumni Database", "Manage graduated students", "alumni_icon.png", self.open_alumni, ['Admin', 'DataEntry']),
            ("🔐 RBAC Editor", "Manage roles and permissions", "rbac_icon.png", self.open_rbac, ['Admin']),
            ("📜 Audit Logs", "View system activity logs", "audit_icon.png", self.open_audit, ['Admin']),
            ("🗄️ Archive Manager", "Archive old academic years", "archive_icon.png", self.open_archive, ['Admin']),
            ("☁️ Cloud Backup", "Configure Google Drive/Dropbox", "cloud_icon.png", self.open_backup, ['Admin']),
            ("📊 Advanced Analytics", "Interactive performance charts", "analytics_icon.png", self.open_analytics, ['Admin', 'Teacher']),
            ("📑 Report Builder", "Generate custom Excel/PDF reports", "report_icon.png", self.open_reports, ['Admin', 'Teacher', 'DataEntry'])
        ]
        
        user_role = self.user_data.get('role', 'Viewer')
        
        row = 0
        col = 0
        for name, desc, icon, handler, allowed_roles in all_features:
            if user_role in allowed_roles:
                card = self.create_feature_card(name, desc, handler)
                grid.addWidget(card, row, col)
                
                col += 1
                if col > 1: # 2 columns
                    col = 0
                    row += 1
        
        scroll_layout.addLayout(grid)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
    def create_feature_card(self, name, desc, handler):
        """Create a clickable feature card"""
        card = QFrame()
        # Modern card styling with hover effects (removed box-shadow as it's not supported in QSS)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
            }
            QFrame:hover {
                background-color: #f8f9fa;
                border-color: #3498db;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        card.setCursor(Qt.PointingHandCursor)
        card.mousePressEvent = lambda e: handler()
        card.setMinimumHeight(180)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        
        name_label = QLabel(name)
        # Use specific style to ensure priority
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(name_label)
        
        desc_label = QLabel(desc)
        desc_label.setStyleSheet("color: #7f8c8d; font-size: 13px; line-height: 1.4;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        btn = QPushButton("Open")
        btn.clicked.connect(handler)
        layout.addWidget(btn)
        
        return card

    def open_attendance(self):
        self.attendance_window = QMainWindow()
        self.attendance_window.setWindowTitle("Attendance Management")
        self.attendance_window.setCentralWidget(AttendanceManagement(self.user_data))
        self.attendance_window.resize(1000, 700)
        self.attendance_window.show()

    def open_timetable(self):
        self.timetable_window = QMainWindow()
        self.timetable_window.setWindowTitle("Timetable Management")
        self.timetable_window.setCentralWidget(TimetableManagement(self.user_data))
        self.timetable_window.resize(1000, 700)
        self.timetable_window.show()

    def open_assignments(self):
        self.assignment_window = QMainWindow()
        self.assignment_window.setWindowTitle("Assignment Management")
        self.assignment_window.setCentralWidget(AssignmentManagementPage(user_data=self.user_data))
        self.assignment_window.resize(1000, 700)
        self.assignment_window.show()

    def open_ai_insights(self):
        self.ai_window = QMainWindow()
        self.ai_window.setWindowTitle("AI Insights")
        self.ai_window.setCentralWidget(AIInsightsPage())
        self.ai_window.resize(1000, 700)
        self.ai_window.show()

    def open_promotion(self):
        self.promotion_window = QMainWindow()
        self.promotion_window.setWindowTitle("Student Promotion")
        self.promotion_window.setCentralWidget(StudentPromotionPage(user_data=self.user_data))
        self.promotion_window.resize(1000, 700)
        self.promotion_window.show()

    def open_id_cards(self):
        self.id_card_window = QMainWindow()
        self.id_card_window.setWindowTitle("ID Card Generator")
        self.id_card_window.setCentralWidget(IDCardGeneratorPage(user_data=self.user_data))
        self.id_card_window.resize(1000, 700)
        self.id_card_window.show()

    def open_alumni(self):
        self.alumni_window = QMainWindow()
        self.alumni_window.setWindowTitle("Alumni Management")
        self.alumni_window.setCentralWidget(AlumniManagementPage(user_data=self.user_data))
        self.alumni_window.resize(1000, 700)
        self.alumni_window.show()

    def open_rbac(self):
        self.rbac_window = QMainWindow()
        self.rbac_window.setWindowTitle("RBAC Editor")
        self.rbac_window.setCentralWidget(RBACEditorPage(user_data=self.user_data))
        self.rbac_window.resize(1000, 700)
        self.rbac_window.show()

    def open_audit(self):
        self.audit_window = QMainWindow()
        self.audit_window.setWindowTitle("Audit Logs")
        self.audit_window.setCentralWidget(AuditViewerPage(user_data=self.user_data))
        self.audit_window.resize(1000, 700)
        self.audit_window.show()

    def open_archive(self):
        self.archive_window = QMainWindow()
        self.archive_window.setWindowTitle("Archive Manager")
        self.archive_window.setCentralWidget(ArchiveManagerPage(user_data=self.user_data))
        self.archive_window.resize(1000, 700)
        self.archive_window.show()

    def open_backup(self):
        self.backup_window = QMainWindow()
        self.backup_window.setWindowTitle("Cloud Backup Settings")
        self.backup_window.setCentralWidget(CloudBackupSettingsPage(user_data=self.user_data))
        self.backup_window.resize(800, 600)
        self.backup_window.show()

    def open_analytics(self):
        self.analytics_window = QMainWindow()
        self.analytics_window.setWindowTitle("Advanced Analytics")
        self.analytics_window.setCentralWidget(AdvancedAnalyticsPage(self.user_data))
        self.analytics_window.resize(1000, 700)
        self.analytics_window.show()

    def open_reports(self):
        self.reports_window = QMainWindow()
        self.reports_window.setWindowTitle("Report Builder")
        self.reports_window.setCentralWidget(ReportBuilderPage(self.user_data))
        self.reports_window.resize(800, 600)
        self.reports_window.show()
