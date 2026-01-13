"""
Teacher Dashboard - Department-filtered view for teachers
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.student_controller import student_controller
from controllers.course_controller import course_controller


class TeacherDashboard(QWidget):
    """Dashboard showing only teacher's department data"""
    
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.department_id = department_id
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📊 My Department Dashboard")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Statistics Cards
        stats_layout = QHBoxLayout()
        
        self.students_card = self.create_stat_card("👥 My Students", "0", "#4CAF50")
        self.courses_card = self.create_stat_card("📚 My Courses", "0", "#2196F3")
        
        stats_layout.addWidget(self.students_card)
        stats_layout.addWidget(self.courses_card)
        
        layout.addLayout(stats_layout)
        
        # Department Info
        info_group = QGroupBox("🏛️ Department Information")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("Loading...")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Quick Actions
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QHBoxLayout()
        
        view_students_btn = QPushButton("👥 View My Students")
        view_students_btn.setObjectName("primaryButton")
        view_students_btn.setMinimumHeight(50)
        view_students_btn.clicked.connect(self.view_students)
        actions_layout.addWidget(view_students_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(50)
        refresh_btn.clicked.connect(self.load_data)
        actions_layout.addWidget(refresh_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
    
    def create_stat_card(self, title, value, color):
        """Create statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        card.setMinimumHeight(120)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def load_data(self):
        """Load department-specific data"""
        if not self.department_id:
            self.info_label.setText("❌ No department assigned")
            return
        
        try:
            # Get students in department
            all_students = student_controller.get_all_students()
            dept_students = [s for s in all_students if s.get('department_id') == self.department_id]
            
            # Get courses in department
            all_courses = course_controller.get_all_courses()
            dept_courses = [c for c in all_courses if c.get('department_id') == self.department_id]
            
            # Update cards
            self.students_card.value_label.setText(str(len(dept_students)))
            self.courses_card.value_label.setText(str(len(dept_courses)))
            
            # Get current user info for assigned subject
            from controllers.auth_controller import auth
            user = auth.get_current_user()
            assigned_subject_name = "None"
            
            if user and user.get('assigned_subject_id'):
                subject = course_controller.get_course_by_id(user['assigned_subject_id'])
                if subject:
                    assigned_subject_name = f"{subject['course_code']} - {subject['course_name']}"
            
            # Update info
            if dept_students:
                dept_name = dept_students[0].get('department_name', 'Unknown')
                info_text = f"""
<b>Department:</b> {dept_name}<br>
<b>Assigned Subject:</b> {assigned_subject_name}<br>
<b>Total Students:</b> {len(dept_students)}<br>
<b>Total Courses:</b> {len(dept_courses)}<br>
<i>You can only view and manage data from your department</i>
                """
                self.info_label.setText(info_text.strip())
            else:
                self.info_label.setText(f"Department: {self.department_id}<br>Assigned Subject: {assigned_subject_name}<br>No students found.")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {str(e)}")
    
    def view_students(self):
        """Navigate to Students tab"""
        parent = self.parent()
        while parent and not hasattr(parent, 'tabs'):
            parent = parent.parent()
        if parent and hasattr(parent, 'tabs'):
            for i in range(parent.tabs.count()):
                if "Students" in parent.tabs.tabText(i):
                    parent.tabs.setCurrentIndex(i)
                    break
