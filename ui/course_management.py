"""
Course Management Page
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.course_controller import course_controller
from controllers.department_controller import department_controller


class CourseManagementPage(QWidget):
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.courses_data = []
        self.department_id = department_id  # For teacher filtering
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Course Management")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()
        
        add_btn = QPushButton("➕ Add Course")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_course)
        header.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_courses)
        header.addWidget(refresh_btn)
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Code", "Course Name", "Department", "Credits", "Semester"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_course_from_selection)
        action_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_course_from_selection)
        action_layout.addWidget(delete_btn)
        
        layout.addLayout(action_layout)
        
        self.load_courses()
    
    def load_courses(self):
        """Load all courses into table"""
        if self.department_id:
            # Teacher view - only their department
            courses = course_controller.get_courses_by_department(self.department_id)
        else:
            # Admin view - all courses
            courses = course_controller.get_all_courses()
        self.courses_data = courses
        
        # CRITICAL: Clear table first
        self.table.clearContents()
        self.table.setRowCount(0)
        
        # Set new row count
        self.table.setRowCount(len(courses))
        
        for row, course in enumerate(courses):
            self.table.setItem(row, 0, QTableWidgetItem(course['course_code']))
            self.table.setItem(row, 1, QTableWidgetItem(course['course_name']))
            self.table.setItem(row, 2, QTableWidgetItem(course.get('department_name', '')))
            self.table.setItem(row, 3, QTableWidgetItem(str(course['credits'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(course['semester'])))
        
        self.table.resizeColumnsToContents()
    
    def add_course(self):
        dialog = CourseDialog(self)
        if dialog.exec_():
            self.load_courses()
    
    def edit_course_from_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a course to edit")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.courses_data):
            return
        
        course = self.courses_data[row]
        dialog = CourseDialog(self, course)
        if dialog.exec_():
            self.load_courses()
    
    def delete_course_from_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a course to delete")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.courses_data):
            return
        
        course = self.courses_data[row]
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Are you sure you want to delete {course['course_name']}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, msg = course_controller.delete_course(course['course_id'])
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_courses()
            else:
                QMessageBox.warning(self, "Error", msg)


class CourseDialog(QDialog):
    def __init__(self, parent=None, course=None):
        super().__init__(parent)
        self.course = course
        self.setWindowTitle("Add Course" if not course else "Edit Course")
        self.setFixedSize(450, 400)
        
        layout = QFormLayout(self)
        
        self.code_input = QLineEdit()
        layout.addRow("Course Code:*", self.code_input)
        
        self.name_input = QLineEdit()
        layout.addRow("Course Name:*", self.name_input)
        
        self.dept_combo = QComboBox()
        departments = department_controller.get_all_departments()
        for dept in departments:
            self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        layout.addRow("Department:*", self.dept_combo)
        
        self.semester_combo = QComboBox()
        for i in range(1, 9):
            self.semester_combo.addItem(f"Semester {i}", i)
        layout.addRow("Semester:*", self.semester_combo)
        
        self.max_marks_input = QSpinBox()
        self.max_marks_input.setRange(1, 1000)
        self.max_marks_input.setValue(100)
        layout.addRow("Max Marks:", self.max_marks_input)
        
        self.pass_marks_input = QSpinBox()
        self.pass_marks_input.setRange(1, 1000)
        self.pass_marks_input.setValue(40)
        layout.addRow("Pass Marks:", self.pass_marks_input)
        
        self.credits_input = QSpinBox()
        self.credits_input.setRange(1, 10)
        self.credits_input.setValue(3)
        layout.addRow("Credits:*", self.credits_input)
        
        if course:
            self.code_input.setText(course['course_code'])
            self.name_input.setText(course['course_name'])
            for i in range(self.dept_combo.count()):
                if self.dept_combo.itemData(i) == course['department_id']:
                    self.dept_combo.setCurrentIndex(i)
                    break
            self.semester_combo.setCurrentIndex(course['semester'] - 1)
            self.max_marks_input.setValue(course['max_marks'])
            self.pass_marks_input.setValue(course['pass_marks'])
            self.credits_input.setValue(course['credits'])
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow("", btn_layout)
    
    def save(self):
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        dept_id = self.dept_combo.currentData()
        semester = self.semester_combo.currentData()
        max_marks = self.max_marks_input.value()
        pass_marks = self.pass_marks_input.value()
        credits = self.credits_input.value()
        
        if not code or not name:
            QMessageBox.warning(self, "Error", "Please fill all required fields")
            return
        
        if self.course:
            success, msg = course_controller.update_course(
                self.course['course_id'], code, name, dept_id, semester, max_marks, pass_marks, credits
            )
        else:
            success, msg, _ = course_controller.create_course(
                code, name, dept_id, semester, max_marks, pass_marks, credits
            )
        
        if success:
            QMessageBox.information(self, "Success", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", msg)
