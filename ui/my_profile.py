"""
My Profile Page - Student's personal information
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.student_controller import student_controller


class MyProfilePage(QWidget):
    """Display student's profile (read-only)"""
    
    def __init__(self, parent=None, student_id=None, user_data=None):
        super().__init__(parent)
        self.student_id = student_id
        self.user_data = user_data
        self.init_ui()
        self.load_profile()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("👤 My Profile")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Profile Info (Read-only)
        info_group = QGroupBox("Personal Information")
        info_layout = QFormLayout()
        
        self.name_label = QLabel()
        info_layout.addRow("Name:", self.name_label)
        
        self.roll_label = QLabel()
        info_layout.addRow("Roll Number:", self.roll_label)
        
        self.dept_label = QLabel()
        info_layout.addRow("Department:", self.dept_label)
        
        self.semester_label = QLabel()
        info_layout.addRow("Semester:", self.semester_label)
        
        self.email_label = QLabel()
        info_layout.addRow("Email:", self.email_label)
        
        self.phone_label = QLabel()
        info_layout.addRow("Phone:", self.phone_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
    
    def load_profile(self):
        """Load student profile"""
        if not self.student_id:
            return
        
        try:
            students = student_controller.get_all_students()
            student = next((s for s in students if s['student_id'] == self.student_id), None)
            
            if student:
                self.name_label.setText(student['name'])
                self.roll_label.setText(student['roll_number'])
                self.dept_label.setText(student.get('department_name', 'N/A'))
                self.semester_label.setText(str(student['semester']))
                self.email_label.setText(student.get('email', 'N/A'))
                self.phone_label.setText(student.get('phone', 'N/A'))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load profile: {str(e)}")
