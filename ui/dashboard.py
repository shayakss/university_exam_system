"""
Modern Dashboard Page - Redesigned with Charts and Insights
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from controllers.student_controller import student_controller
from controllers.department_controller import department_controller
from controllers.course_controller import course_controller
from controllers.user_controller import user_controller
from controllers.attendance_controller import attendance_controller
from datetime import date, timedelta


class ModernDashboard(QWidget):
    """Modern Dashboard with comprehensive statistics and charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F5F7FA;")
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Top Bar (Header)
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: #F5F7FA; border: none; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)
        
        # 2. Stats Overview Row (4 Compact Cards)
        stats_row = self.create_stats_row()
        content_layout.addWidget(stats_row)
        
        # 3. Quick Actions Card
        quick_actions = self.create_quick_actions()
        content_layout.addWidget(quick_actions)
        
        # 4. Insights Section (Charts Row)
        charts_row = self.create_charts_row()
        content_layout.addLayout(charts_row)
        
        # 5. Summary Cards Row
        summary_row = self.create_summary_row()
        content_layout.addWidget(summary_row)
        
        # 6. System Status & Logs
        system_status = self.create_system_status()
        content_layout.addWidget(system_status)
        
        content_layout.addStretch()
        
        # 7. Footer
        footer = self.create_footer()
        content_layout.addWidget(footer)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def create_header(self):
        """Create top bar header"""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1A73E8, stop:1 #4A90E2);
                border: none;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)
        
        # Logo + Title
        title_layout = QHBoxLayout()
        logo = QLabel("🎓")
        logo.setStyleSheet("font-size: 32px; background: transparent; border: none;")
        title_layout.addWidget(logo)
        
        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: white;
            background: transparent;
            border: none;
        """)
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # User Avatar / Settings
        user_btn = QPushButton("👤 Admin")
        user_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        layout.addWidget(user_btn)
        
        return header
    
    def create_stats_row(self):
        """Create stats overview row with 4 compact cards"""
        container = QFrame()
        container.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        
        # Create 4 stat cards
        self.students_card = self.create_stat_card("👥", "0", "Total Students", "#1A73E8")
        self.courses_card = self.create_stat_card("📚", "0", "Total Courses", "#34C759")
        self.departments_card = self.create_stat_card("🏛️", "0", "Departments", "#FF9500")
        self.users_card = self.create_stat_card("👤", "0", "Active Users", "#9C27B0")
        
        layout.addWidget(self.students_card)
        layout.addWidget(self.courses_card)
        layout.addWidget(self.departments_card)
        layout.addWidget(self.users_card)
        
        return container
    
    def create_stat_card(self, icon, value, title, color):
        """Create a compact stat card with gradient icon"""
        card = QFrame()
        card.setMinimumWidth(180)
        card.setMaximumWidth(250)
        card.setMinimumHeight(140)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Icon with gradient background
        icon_container = QFrame()
        icon_container.setFixedSize(56, 56)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 28px;
                border: none;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 28px; background: transparent; border: none; color: white;")
        icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_container)
        
        # Value (big, bold)
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #1F1F1F;
            background: transparent;
            border: none;
        """)
        layout.addWidget(value_label)
        
        # Title (smaller)
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 13px;
            color: #666;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def create_quick_actions(self):
        """Create quick actions card with horizontal buttons"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Quick Actions")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #1F1F1F;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Add Student
        add_student_btn = self.create_action_button("➕ Add Student", "#34C759")
        buttons_layout.addWidget(add_student_btn)
        
        # Add Course
        add_course_btn = self.create_action_button("➕ Add Course", "#34C759")
        buttons_layout.addWidget(add_course_btn)
        
        # Add Department
        add_dept_btn = self.create_action_button("➕ Add Dept", "#34C759")
        buttons_layout.addWidget(add_dept_btn)
        
        # Add User
        add_user_btn = self.create_action_button("➕ Add User", "#34C759")
        buttons_layout.addWidget(add_user_btn)
        
        # Refresh
        refresh_btn = self.create_action_button("🔄 Refresh", "#1A73E8")
        refresh_btn.clicked.connect(self.load_statistics)
        buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(buttons_layout)
        
        return card
    
    def create_action_button(self, text, color):
        """Create a quick action button"""
        btn = QPushButton(text)
        btn.setMinimumWidth(180)
        btn.setMaximumWidth(220)
        btn.setMinimumHeight(45)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)
        return btn
    
    def create_charts_row(self):
        """Create insights section with charts"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Left: Attendance Trend Chart (70%)
        attendance_card = QFrame()
        attendance_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        attendance_layout = QVBoxLayout(attendance_card)
        attendance_layout.setContentsMargins(25, 25, 25, 25)
        
        att_title = QLabel("📊 Attendance Overview (Last 30 Days)")
        att_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F1F1F; background: transparent; border: none;")
        attendance_layout.addWidget(att_title)
        
        # Placeholder for chart
        chart_placeholder = QLabel("Line chart will be displayed here")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setMinimumHeight(250)
        chart_placeholder.setStyleSheet("color: #999; background: #F5F7FA; border-radius: 8px; border: none;")
        attendance_layout.addWidget(chart_placeholder)
        
        layout.addWidget(attendance_card, 7)
        
        # Right: Department Breakdown (30%)
        dept_card = QFrame()
        dept_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        dept_layout = QVBoxLayout(dept_card)
        dept_layout.setContentsMargins(25, 25, 25, 25)
        
        dept_title = QLabel("🥧 Departments Overview")
        dept_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F1F1F; background: transparent; border: none;")
        dept_layout.addWidget(dept_title)
        
        # Placeholder for pie chart
        pie_placeholder = QLabel("Pie chart")
        pie_placeholder.setAlignment(Qt.AlignCenter)
        pie_placeholder.setMinimumHeight(250)
        pie_placeholder.setStyleSheet("color: #999; background: #F5F7FA; border-radius: 8px; border: none;")
        dept_layout.addWidget(pie_placeholder)
        
        layout.addWidget(dept_card, 3)
        
        return layout
    
    def create_summary_row(self):
        """Create summary cards row"""
        container = QFrame()
        container.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        
        # Active Students
        self.active_students_card = self.create_summary_card("Active Students", "0", "#34C759")
        layout.addWidget(self.active_students_card)
        
        # Inactive Students
        self.inactive_students_card = self.create_summary_card("Inactive Students", "0", "#FF3B30")
        layout.addWidget(self.inactive_students_card)
        
        # Today's Attendance
        self.today_attendance_card = self.create_summary_card("Today's Attendance", "0%", "#1A73E8")
        layout.addWidget(self.today_attendance_card)
        
        return container
    
    def create_summary_card(self, title, value, color):
        """Create compact summary card"""
        card = QFrame()
        card.setMinimumHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border-left: 4px solid {color};
                border-top: none;
                border-right: none;
                border-bottom: none;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; color: #666; background: transparent; border: none;")
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: bold;
            color: {color};
            background: transparent;
            border: none;
        """)
        layout.addWidget(value_label)
        
        card.value_label = value_label
        
        return card
    
    def create_system_status(self):
        """Create system status and logs section"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 12px;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # System Status
        status_title = QLabel("System Status: 🟢 Operational")
        status_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1F1F1F;
            background: transparent;
            border: none;
        """)
        layout.addWidget(status_title)
        
        # Status info
        self.status_info = QLabel("Loading...")
        self.status_info.setStyleSheet("""
            font-size: 14px;
            color: #333;
            background: transparent;
            border: none;
            line-height: 1.6;
        """)
        self.status_info.setWordWrap(True)
        layout.addWidget(self.status_info)
        
        # Logs section
        logs_title = QLabel("Logs")
        logs_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1F1F1F;
            background: transparent;
            border: none;
            margin-top: 10px;
        """)
        layout.addWidget(logs_title)
        
        logs_info = QLabel("""
• Last sync: 2 minutes ago
• Cache rebuilt successfully
• System healthy
        """)
        logs_info.setStyleSheet("""
            font-size: 14px;
            color: #333;
            background: transparent;
            border: none;
        """)
        layout.addWidget(logs_info)
        
        return card
    
    def create_footer(self):
        """Create footer"""
        footer = QLabel("© 2025 University Exam System — All Rights Reserved")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            font-size: 12px;
            color: #999;
            background: transparent;
            border: none;
            padding: 20px;
        """)
        return footer
    
    def load_statistics(self):
        """Load and display statistics"""
        try:
            # Get counts
            students = student_controller.get_all_students()
            departments = department_controller.get_all_departments()
            courses = course_controller.get_all_courses()
            users = user_controller.get_all_users()
            
            # Get today's attendance
            today = date.today()
            attendance_stats = attendance_controller.get_attendance_statistics(today, today)
            attendance_percentage = attendance_stats.get('average_percentage', 0) if attendance_stats else 0
            
            # Update stat cards
            self.students_card.value_label.setText(f"{len(students):,}")
            self.courses_card.value_label.setText(str(len(courses)))
            self.departments_card.value_label.setText(str(len(departments)))
            self.users_card.value_label.setText(str(len(users)))
            
            # Update summary cards
            active_students = sum(1 for s in students if s.get('is_active', 1))
            inactive_students = len(students) - active_students
            
            self.active_students_card.value_label.setText(f"{active_students:,}")
            self.inactive_students_card.value_label.setText(f"{inactive_students:,}")
            self.today_attendance_card.value_label.setText(f"{attendance_percentage:.0f}%")
            
            # Update system status
            active_users = sum(1 for u in users if u.get('is_active', 1))
            status_text = f"""
Students: {len(students):,} total (Active: {active_students:,})
Courses: {len(courses)}
Departments: {len(departments)}
Users: {len(users)} ({active_users} active)
Attendance Today: {attendance_percentage:.1f}%
            """
            self.status_info.setText(status_text.strip())
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load statistics: {str(e)}")
