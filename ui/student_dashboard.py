"""
Student Dashboard - Personalized view for student users
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.student_controller import student_controller
from controllers.result_controller import result_controller


class StudentDashboard(QWidget):
    """Personalized dashboard showing only student's own data"""
    
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_id = student_id
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📊 My Dashboard")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Student Info Card
        info_group = QGroupBox("👤 My Information")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("Loading...")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Academic Stats
        stats_group = QGroupBox("📈 My Academic Statistics")
        stats_layout = QVBoxLayout()
        self.stats_label = QLabel("Loading...")
        self.stats_label.setWordWrap(True)
        stats_layout.addWidget(self.stats_label)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Quick Actions
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QHBoxLayout()
        
        view_results_btn = QPushButton("📋 View My Results")
        view_results_btn.setObjectName("primaryButton")
        view_results_btn.setMinimumHeight(50)
        view_results_btn.clicked.connect(self.view_results)
        actions_layout.addWidget(view_results_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(50)
        refresh_btn.clicked.connect(self.load_data)
        actions_layout.addWidget(refresh_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
    
    def load_data(self):
        """Load student's own data"""
        if not self.student_id:
            self.info_label.setText("❌ No student ID found")
            return
        
        try:
            # Get student info
            students = student_controller.get_all_students()
            student = next((s for s in students if s['student_id'] == self.student_id), None)
            
            if student:
                info_text = f"""
<b>Name:</b> {student['name']}<br>
<b>Roll Number:</b> {student['roll_number']}<br>
<b>Department:</b> {student.get('department_name', 'N/A')}<br>
<b>Semester:</b> {student['semester']}<br>
<b>Email:</b> {student.get('email', 'N/A')}
                """
                self.info_label.setText(info_text.strip())
            else:
                self.info_label.setText("❌ Student information not found")
            
            # Get academic stats
            results = result_controller.get_student_results(self.student_id)
            
            if results:
                total_courses = len(results)
                stats_text = f"""
<b>Total Courses:</b> {total_courses}<br>
<b>Semester:</b> {student['semester']}<br>
<i>View detailed results in "My Results" tab</i>
                """
                self.stats_label.setText(stats_text.strip())
            else:
                self.stats_label.setText("No results available yet")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {str(e)}")
    
    def view_results(self):
        """Navigate to My Results tab"""
        parent = self.parent()
        while parent and not hasattr(parent, 'tabs'):
            parent = parent.parent()
        if parent and hasattr(parent, 'tabs'):
            for i in range(parent.tabs.count()):
                if "My Results" in parent.tabs.tabText(i):
                    parent.tabs.setCurrentIndex(i)
                    break
