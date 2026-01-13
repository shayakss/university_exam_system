"""
Marks Entry Page
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.marks_controller import marks_controller
from controllers.student_controller import student_controller
from controllers.course_controller import course_controller
from controllers.department_controller import department_controller
from controllers.auth_controller import auth


class MarksEntryPage(QWidget):
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.teacher_department_id = department_id  # For teacher filtering
        
        # Check for assigned subject
        self.assigned_subject_id = None
        user = auth.get_current_user()
        if user and user.get('role') == 'Teacher':
            self.assigned_subject_id = user.get('assigned_subject_id')
            
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Marks Entry")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Filters
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Department:"))
        self.dept_combo = QComboBox()
        self.dept_combo.currentIndexChanged.connect(self.on_department_changed)
        if self.teacher_department_id:
            # Teacher - disable department selection
            self.dept_combo.setEnabled(False)
        filter_layout.addWidget(self.dept_combo)
        
        # Refresh department button
        dept_refresh_btn = QPushButton("🔄")
        dept_refresh_btn.setFixedWidth(40)
        dept_refresh_btn.setToolTip("Refresh Departments")
        dept_refresh_btn.clicked.connect(self.load_departments)
        filter_layout.addWidget(dept_refresh_btn)
        
        filter_layout.addWidget(QLabel("Semester:"))
        self.semester_combo = QComboBox()
        for i in range(1, 9):
            self.semester_combo.addItem(f"Semester {i}", i)
        self.semester_combo.currentIndexChanged.connect(self.on_semester_changed)
        filter_layout.addWidget(self.semester_combo)
        
        filter_layout.addWidget(QLabel("Student:"))
        self.student_combo = QComboBox()
        self.student_combo.setMinimumWidth(250)  # Increased width for better visibility
        self.student_combo.currentIndexChanged.connect(self.on_student_changed)
        filter_layout.addWidget(self.student_combo)
        
        filter_layout.addWidget(QLabel("Course:"))
        self.course_combo = QComboBox()
        self.course_combo.setMinimumWidth(300)  # Increased width for better visibility
        self.course_combo.currentIndexChanged.connect(self.on_course_changed)
        if self.assigned_subject_id:
            self.course_combo.setEnabled(False)
        filter_layout.addWidget(self.course_combo)
        
        # Refresh course button
        course_refresh_btn = QPushButton("🔄")
        course_refresh_btn.setFixedWidth(40)
        course_refresh_btn.setToolTip("Refresh Courses")
        course_refresh_btn.clicked.connect(self.on_department_changed)
        filter_layout.addWidget(course_refresh_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Marks entry
        entry_layout = QFormLayout()
        
        self.max_marks_label = QLabel("--")
        entry_layout.addRow("Maximum Marks:", self.max_marks_label)
        
        self.pass_marks_label = QLabel("--")
        entry_layout.addRow("Pass Marks:", self.pass_marks_label)
        
        self.marks_input = QDoubleSpinBox()
        self.marks_input.setRange(0, 1000)
        self.marks_input.setDecimals(2)
        entry_layout.addRow("Marks Obtained:", self.marks_input)
        
        layout.addLayout(entry_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save Marks")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_marks)
        btn_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("🔄 Clear")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.load_departments()
    
    def load_departments(self):
        """Load departments into dropdown"""
        try:
            self.dept_combo.clear()
            self.dept_combo.addItem("Select Department", None)
            
            departments = department_controller.get_all_departments()
            for dept in departments:
                if self.teacher_department_id:
                    # Teacher - only show their department
                    if dept['department_id'] == self.teacher_department_id:
                        self.dept_combo.addItem(dept['department_name'], dept['department_id'])
                else:
                    # Admin - show all
                    self.dept_combo.addItem(dept['department_name'], dept['department_id'])
            
            # Auto-select teacher's department
            if self.teacher_department_id and self.dept_combo.count() > 1:
                self.dept_combo.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load departments: {str(e)}")
            print(f"Error in load_departments: {e}")
            import traceback
            traceback.print_exc()
    
    def on_department_changed(self):
        try:
            self.student_combo.clear()
            self.course_combo.clear()
            
            dept_id = self.dept_combo.currentData()
            semester = self.semester_combo.currentData()
            
            if dept_id:
                students = student_controller.get_students_by_department(dept_id, semester)
                for student in students:
                    self.student_combo.addItem(
                        f"{student['roll_number']} - {student['name']}", 
                        student['student_id']
                    )
                
                courses = course_controller.get_courses_by_department(dept_id, semester)
                for course in courses:
                    # If teacher has assigned subject, only show that one
                    if self.assigned_subject_id:
                        if course['course_id'] == self.assigned_subject_id:
                            self.course_combo.addItem(
                                f"{course['course_code']} - {course['course_name']}",
                                course['course_id']
                            )
                            self.course_combo.setCurrentIndex(0)
                    else:
                        self.course_combo.addItem(
                            f"{course['course_code']} - {course['course_name']}",
                            course['course_id']
                        )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load students/courses: {str(e)}")
            print(f"Error in on_department_changed: {e}")
            import traceback
            traceback.print_exc()
    
    def on_semester_changed(self):
        self.on_department_changed()
    
    def on_student_changed(self):
        # Load existing marks if any
        student_id = self.student_combo.currentData()
        course_id = self.course_combo.currentData()
        
        if student_id and course_id:
            existing = marks_controller.get_mark(student_id, course_id)
            if existing:
                self.marks_input.setValue(existing['marks_obtained'])
    
    def on_course_changed(self):
        # Update max/pass marks
        course_id = self.course_combo.currentData()
        
        if course_id:
            course = course_controller.get_course_by_id(course_id)
            if course:
                self.max_marks_label.setText(str(course['max_marks']))
                self.pass_marks_label.setText(str(course['pass_marks']))
                self.marks_input.setMaximum(course['max_marks'])
        
        # Also check for existing marks
        self.on_student_changed()
    
    def save_marks(self):
        try:
            student_id = self.student_combo.currentData()
            course_id = self.course_combo.currentData()
            marks = self.marks_input.value()
            
            # Validation
            if not student_id or not course_id:
                QMessageBox.warning(self, "Validation Error", "Please select both student and course")
                return
            
            # Check if department is selected
            if not self.dept_combo.currentData():
                QMessageBox.warning(self, "Validation Error", "Please select a department first")
                return
            
            user = auth.get_current_user()
            if not user:
                QMessageBox.critical(self, "Error", "User session expired. Please login again.")
                return
            
            success, msg, _ = marks_controller.enter_marks(
                student_id, course_id, marks, user['user_id']
            )
            
            if success:
                QMessageBox.information(self, "Success", msg)
                self.clear_form()
            else:
                QMessageBox.warning(self, "Error", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save marks: {str(e)}")
            print(f"Error in save_marks: {e}")
            import traceback
            traceback.print_exc()
    
    def clear_form(self):
        self.marks_input.setValue(0)
        self.max_marks_label.setText("--")
        self.pass_marks_label.setText("--")
