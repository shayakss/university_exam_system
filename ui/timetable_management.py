"""
Timetable Management UI
Allows creating and viewing class and exam schedules
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.timetable_controller import timetable_controller
from controllers.course_controller import course_controller
from controllers.department_controller import department_controller
from controllers.user_controller import user_controller

class TimetableManagement(QWidget):
    """Timetable Management Interface"""
    
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data
        self.user_role = user_data.get('role', 'Student') if user_data else 'Student'
        self.department_id = user_data.get('department_id') if user_data else None
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📅 Timetable Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Tabs for Class and Exam Schedules
        self.tabs = QTabWidget()
        self.class_tab = QWidget()
        self.exam_tab = QWidget()
        
        self.tabs.addTab(self.class_tab, "Class Schedule")
        self.tabs.addTab(self.exam_tab, "Exam Schedule")
        
        self.init_class_tab()
        self.init_exam_tab()
        
        layout.addWidget(self.tabs)
    
    def init_class_tab(self):
        """Initialize Class Schedule Tab"""
        layout = QVBoxLayout(self.class_tab)
        
        # Add Schedule Form - Only for Admin and Teacher
        if self.user_role in ['Admin', 'Teacher', 'DataEntry']:
            form_group = QGroupBox("Add Class Schedule")
            form_layout = QGridLayout()
            
            form_layout.addWidget(QLabel("Department:"), 0, 0)
            self.dept_combo = QComboBox()
            self.dept_combo.currentIndexChanged.connect(self.load_courses_teachers)
            form_layout.addWidget(self.dept_combo, 0, 1)
            
            # Lock department for Teacher
            if self.user_role == 'Teacher' and self.department_id:
                self.dept_combo.setEnabled(False)
            
            form_layout.addWidget(QLabel("Semester:"), 0, 2)
            self.sem_combo = QComboBox()
            self.sem_combo.addItems([str(i) for i in range(1, 9)])
            self.sem_combo.currentIndexChanged.connect(self.load_courses_teachers)
            form_layout.addWidget(self.sem_combo, 0, 3)
            
            form_layout.addWidget(QLabel("Course:"), 1, 0)
            self.course_combo = QComboBox()
            form_layout.addWidget(self.course_combo, 1, 1)
            
            form_layout.addWidget(QLabel("Teacher:"), 1, 2)
            self.teacher_combo = QComboBox()
            form_layout.addWidget(self.teacher_combo, 1, 3)
            
            form_layout.addWidget(QLabel("Day:"), 2, 0)
            self.day_combo = QComboBox()
            self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
            form_layout.addWidget(self.day_combo, 2, 1)
            
            form_layout.addWidget(QLabel("Room:"), 2, 2)
            self.room_edit = QLineEdit()
            form_layout.addWidget(self.room_edit, 2, 3)
            
            form_layout.addWidget(QLabel("Start Time:"), 3, 0)
            self.start_time = QTimeEdit()
            self.start_time.setDisplayFormat("HH:mm")
            form_layout.addWidget(self.start_time, 3, 1)
            
            form_layout.addWidget(QLabel("End Time:"), 3, 2)
            self.end_time = QTimeEdit()
            self.end_time.setDisplayFormat("HH:mm")
            form_layout.addWidget(self.end_time, 3, 3)
            
            add_btn = QPushButton("➕ Add Schedule")
            add_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px;")
            add_btn.clicked.connect(self.add_class_schedule)
            form_layout.addWidget(add_btn, 4, 3)
            
            form_group.setLayout(form_layout)
            layout.addWidget(form_group)
        
        # Schedule Table
        self.class_table = QTableWidget()
        self.class_table.setColumnCount(7)
        self.class_table.setHorizontalHeaderLabels([
            "Day", "Time", "Course", "Teacher", "Room", "Department", "Action"
        ])
        self.class_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.class_table)
        
        # Refresh Button
        refresh_btn = QPushButton("🔄 Refresh List")
        refresh_btn.clicked.connect(self.load_class_schedules)
        layout.addWidget(refresh_btn)

    def init_exam_tab(self):
        """Initialize Exam Schedule Tab"""
        layout = QVBoxLayout(self.exam_tab)
        layout.addWidget(QLabel("Exam Schedule functionality coming soon..."))
        # Placeholder for now
    
    def load_data(self):
        """Load initial data"""
        if not hasattr(self, 'dept_combo'):
            # For Student role, just load schedules without filters
            self.load_class_schedules()
            return
            
        departments = department_controller.get_all_departments()
        self.dept_combo.clear()
        for dept in departments:
            self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        
        self.load_courses_teachers()
        self.load_class_schedules()
    
    def load_courses_teachers(self):
        """Load courses and teachers based on selection"""
        if not hasattr(self, 'dept_combo') or not hasattr(self, 'sem_combo'):
            return
            
        dept_id = self.dept_combo.currentData()
        semester = int(self.sem_combo.currentText()) if self.sem_combo.currentText() else 1
        
        if not dept_id:
            return
            
        # Load courses
        if hasattr(self, 'course_combo'):
            self.course_combo.clear()
            courses = course_controller.get_courses_by_department(dept_id, semester) or []
            for course in courses:
                self.course_combo.addItem(course['course_name'], course['course_id'])
            
        # Load teachers
        if hasattr(self, 'teacher_combo'):
            self.teacher_combo.clear()
            teachers = user_controller.get_users_by_role('Teacher') or []
            for teacher in teachers:
                self.teacher_combo.addItem(teacher['full_name'], teacher['user_id'])
            
    def add_class_schedule(self):
        """Add new class schedule"""
        course_id = self.course_combo.currentData()
        teacher_id = self.teacher_combo.currentData()
        dept_id = self.dept_combo.currentData()
        semester = int(self.sem_combo.currentText())
        day = self.day_combo.currentText()
        room = self.room_edit.text()
        start = self.start_time.time().toString("HH:mm")
        end = self.end_time.time().toString("HH:mm")
        
        if not all([course_id, teacher_id, room]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        success, message = timetable_controller.create_class_schedule(
            course_id, teacher_id, dept_id, semester, day, start, end, room
        )
        
        if success:
            QMessageBox.information(self, "Success", "Schedule added successfully!")
            self.load_class_schedules()
        else:
            QMessageBox.warning(self, "Error", message)
            
    def load_class_schedules(self):
        """Load all class schedules"""
        # Get filter values if available
        dept_id = self.dept_combo.currentData() if hasattr(self, 'dept_combo') else self.department_id
        semester = int(self.sem_combo.currentText()) if hasattr(self, 'sem_combo') and self.sem_combo.currentText() else 1
        
        schedules = timetable_controller.get_class_schedules(department_id=dept_id, semester=semester) or []
        
        self.class_table.setRowCount(len(schedules))
        for row, sch in enumerate(schedules):
            self.class_table.setItem(row, 0, QTableWidgetItem(sch.get('day_of_week', '')))
            self.class_table.setItem(row, 1, QTableWidgetItem(f"{sch.get('start_time', '')} - {sch.get('end_time', '')}"))
            self.class_table.setItem(row, 2, QTableWidgetItem(sch.get('course_name', '') or ''))
            self.class_table.setItem(row, 3, QTableWidgetItem(sch.get('teacher_name', '') or ''))
            self.class_table.setItem(row, 4, QTableWidgetItem(sch.get('room_number', '') or ''))
            self.class_table.setItem(row, 5, QTableWidgetItem(sch.get('department_name', '') or ''))
            
            if self.user_role in ['Admin', 'Teacher', 'DataEntry']:
                del_btn = QPushButton("🗑️")
                del_btn.clicked.connect(lambda checked, sid=sch['schedule_id']: self.delete_schedule(sid))
                self.class_table.setCellWidget(row, 6, del_btn)
            
    def delete_schedule(self, schedule_id):
        """Delete a schedule"""
        reply = QMessageBox.question(self, 'Confirm', 'Delete this schedule?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            timetable_controller.delete_class_schedule(schedule_id)
            self.load_class_schedules()

