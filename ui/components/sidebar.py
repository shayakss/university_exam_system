"""
Modern Sidebar Navigation Component
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SidebarButton(QPushButton):
    """Custom styled button for sidebar"""
    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
        # Style
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 20px;
                border: none;
                background-color: transparent;
                color: #ecf0f1;
                font-size: 14px;
                font-weight: 500;
                border-left: 3px solid transparent;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #34495e;
                border-left: 3px solid #3498db;
                color: #3498db;
                font-weight: bold;
            }
        """)

class Sidebar(QWidget):
    """Left Sidebar Navigation"""
    
    # Signal to switch pages (index)
    page_changed = pyqtSignal(int)
    
    def __init__(self, user_role):
        super().__init__()
        self.user_role = user_role
        self.buttons = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #2c3e50;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # App Logo/Title Area
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #1a252f;")
        header_layout = QHBoxLayout(header)
        
        logo_label = QLabel("🎓")
        logo_label.setStyleSheet("font-size: 32px; border: none;")
        header_layout.addWidget(logo_label)
        
        title_label = QLabel("UniSystem")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white; border: none;")
        header_layout.addWidget(title_label)
        
        layout.addWidget(header)
        
        # Navigation Buttons
        self.nav_container = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(0, 10, 0, 0)
        self.nav_layout.setSpacing(2)
        
        # Define menu items based on role
        self.menu_items = self.get_menu_items()
        
        for i, (text, icon) in enumerate(self.menu_items):
            btn = SidebarButton(text)
            btn.clicked.connect(lambda checked, idx=i: self.handle_click(idx))
            self.nav_layout.addWidget(btn)
            self.buttons.append(btn)
            
            # Select first button by default
            if i == 0:
                btn.setChecked(True)
        
        self.nav_layout.addStretch()
        layout.addWidget(self.nav_container)
        
        # User Profile / Logout Area
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet("background-color: #1a252f;")
        footer_layout = QHBoxLayout(footer)
        
        user_icon = QLabel("👤")
        user_icon.setStyleSheet("color: white; font-size: 18px; border: none;")
        footer_layout.addWidget(user_icon)
        
        role_label = QLabel(f"{self.user_role}")
        role_label.setStyleSheet("color: #95a5a6; font-size: 12px; border: none;")
        footer_layout.addWidget(role_label)
        
        layout.addWidget(footer)

    def get_menu_items(self):
        """Get menu items based on role"""
        # Common items
        items = [("📊 Dashboard", "dashboard")]
        
        if self.user_role == 'Student':
            items.extend([
                ("📋 My Results", "results"),
                ("👤 My Profile", "profile"),
                ("📅 Timetable", "timetable"),
                ("🚀 Extra Features", "extra")
            ])
            
        elif self.user_role == 'Teacher':
            items.extend([
                ("👥 My Students", "students"),
                ("📅 Attendance", "attendance"),
                ("📚 Courses", "courses"),
                ("✏️ Marks Entry", "marks"),
                ("📋 Results", "results"),
                ("📈 Reports", "reports"),
                ("🚀 Extra Features", "extra")
            ])
            
        else: # Admin / DataEntry
            items.extend([
                ("👥 Students", "students"),
                ("🏛️ Departments", "departments"),
                ("📚 Courses", "courses"),
                ("📅 Attendance", "attendance"),
                ("✏️ Marks Entry", "marks"),
                ("📋 Results", "results"),
                ("📈 Reports", "reports"),
                ("🚀 Extra Features", "extra")
            ])
            
            if self.user_role == 'Admin':
                items.extend([
                    ("💾 Backup", "backup"),
                    ("👤 Users", "users")
                ])
        
        return items

    def handle_click(self, index):
        """Handle button click"""
        self.page_changed.emit(index)
