"""
Attendance Management UI
Allows teachers to mark and track student attendance
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import date, datetime
from controllers.attendance_controller import attendance_controller
from controllers.student_controller import student_controller
from controllers.course_controller import course_controller
from controllers.department_controller import department_controller

class AttendanceManagement(QWidget):
    """Attendance Management Interface"""
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.current_user_id = user_data.get('user_id')
        self.user_role = user_data.get('role', 'Viewer')
        self.department_id = user_data.get('department_id')
        self.assigned_subject_id = user_data.get('assigned_subject_id')
        
        self.init_ui()
        self.load_departments()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📅 Attendance Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Filters
        filter_group = QGroupBox("Filters")
        filter_layout = QGridLayout()
        
        filter_layout.addWidget(QLabel("Department:"), 0, 0)
        self.department_combo = QComboBox()
        self.department_combo.currentIndexChanged.connect(self.load_students)
        filter_layout.addWidget(self.department_combo, 0, 1)
        
        # Lock department for Teacher
        if self.user_role == 'Teacher' and self.department_id:
            self.department_combo.setEnabled(False)
        
        filter_layout.addWidget(QLabel("Semester:"), 0, 2)
        self.semester_combo = QComboBox()
        self.semester_combo.addItems([str(i) for i in range(1, 9)])
        self.semester_combo.currentIndexChanged.connect(self.load_students)
        filter_layout.addWidget(self.semester_combo, 0, 3)
        
        filter_layout.addWidget(QLabel("Course:"), 1, 0)
        self.course_combo = QComboBox()
        filter_layout.addWidget(self.course_combo, 1, 1)
        
        # Lock course for Teacher if assigned subject
        if self.user_role == 'Teacher' and self.assigned_subject_id:
            self.course_combo.setEnabled(False)
        
        filter_layout.addWidget(QLabel("Date:"), 1, 2)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        filter_layout.addWidget(self.date_edit, 1, 3)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Attendance Table
        table_label = QLabel("Student Attendance")
        table_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Roll Number", "Name", "Department", "Semester", "Status", "Action"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        mark_all_present_btn = QPushButton("✓ Mark All Present")
        mark_all_present_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        mark_all_present_btn.clicked.connect(lambda: self.mark_all("Present"))
        button_layout.addWidget(mark_all_present_btn)
        
        mark_all_absent_btn = QPushButton("✗ Mark All Absent")
        mark_all_absent_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; font-weight: bold;")
        mark_all_absent_btn.clicked.connect(lambda: self.mark_all("Absent"))
        button_layout.addWidget(mark_all_absent_btn)
        
        save_btn = QPushButton("💾 Save Attendance")
        save_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px; font-weight: bold;")
        save_btn.clicked.connect(self.save_attendance)
        button_layout.addWidget(save_btn)
        
        view_report_btn = QPushButton("📊 View Reports")
        view_report_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px; font-weight: bold;")
        view_report_btn.clicked.connect(self.view_reports)
        button_layout.addWidget(view_report_btn)
        
        layout.addLayout(button_layout)
        
        # Statistics
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("background-color: #ecf0f1; padding: 10px; border-radius: 5px; margin-top: 10px;")
        layout.addWidget(self.stats_label)
    
    def load_departments(self):
        """Load departments"""
        self.department_combo.clear()
        departments = department_controller.get_all_departments()
        for dept in departments:
            # Filter for Teacher
            if self.user_role == 'Teacher' and self.department_id:
                if dept['department_id'] == self.department_id:
                    self.department_combo.addItem(dept['department_name'], dept['department_id'])
            else:
                self.department_combo.addItem(dept['department_name'], dept['department_id'])
        
        if departments:
            self.load_courses()
    
    def load_courses(self):
        """Load courses for selected department and semester"""
        self.course_combo.clear()
        dept_id = self.department_combo.currentData()
        semester = int(self.semester_combo.currentText())
        
        if dept_id:
            courses = course_controller.get_courses_by_department(dept_id, semester)
            for course in courses:
                # Filter for Teacher with assigned subject
                if self.user_role == 'Teacher' and self.assigned_subject_id:
                    if course['course_id'] == self.assigned_subject_id:
                        self.course_combo.addItem(
                            f"{course['course_code']} - {course['course_name']}", 
                            course['course_id']
                        )
                else:
                    self.course_combo.addItem(
                        f"{course['course_code']} - {course['course_name']}", 
                        course['course_id']
                    )
    
    def load_students(self):
        """Load students for selected department and semester"""
        dept_id = self.department_combo.currentData()
        semester = int(self.semester_combo.currentText())
        
        if not dept_id:
            return
        
        students = student_controller.get_students_by_department(dept_id, semester)
        
        self.table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(student['roll_number']))
            self.table.setItem(row, 1, QTableWidgetItem(student['name']))
            self.table.setItem(row, 2, QTableWidgetItem(student.get('department_name', '')))
            self.table.setItem(row, 3, QTableWidgetItem(str(student['semester'])))
            
            # Status combo
            status_combo = QComboBox()
            status_combo.addItems(["Present", "Absent", "Leave", "Late"])
            self.table.setCellWidget(row, 4, status_combo)
            
            # Store student_id
            self.table.item(row, 0).setData(Qt.UserRole, student['student_id'])
        
        self.update_statistics()
    
    def mark_all(self, status):
        """Mark all students with given status"""
        for row in range(self.table.rowCount()):
            status_combo = self.table.cellWidget(row, 4)
            if status_combo:
                status_combo.setCurrentText(status)
    
    def save_attendance(self):
        """Save attendance for all students"""
        course_id = self.course_combo.currentData()
        attendance_date = self.date_edit.date().toPyDate()
        
        if not course_id:
            QMessageBox.warning(self, "Error", "Please select a course")
            return
        
        success_count = 0
        error_count = 0
        
        for row in range(self.table.rowCount()):
            student_id = self.table.item(row, 0).data(Qt.UserRole)
            status_combo = self.table.cellWidget(row, 4)
            status = status_combo.currentText()
            
            success, message = attendance_controller.mark_student_attendance(
                student_id=student_id,
                course_id=course_id,
                attendance_date=attendance_date,
                status=status,
                marked_by=self.current_user_id
            )
            
            if success:
                success_count += 1
            else:
                error_count += 1
        
        QMessageBox.information(
            self, 
            "Success", 
            f"Attendance saved!\n\nSuccess: {success_count}\nErrors: {error_count}"
        )
        
        self.update_statistics()
    
    def view_reports(self):
        """View attendance reports"""
        dept_id = self.department_combo.currentData()
        semester = int(self.semester_combo.currentText())
        
        # Get low attendance students
        low_attendance = attendance_controller.get_low_attendance_students(
            department_id=dept_id,
            semester=semester,
            threshold=75.0
        )
        
        # Create report dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Attendance Report")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        label = QLabel(f"<h3>Low Attendance Students (< 75%)</h3>")
        layout.addWidget(label)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Roll Number", "Name", "Attendance %", "Status"])
        table.setRowCount(len(low_attendance))
        
        for row, student in enumerate(low_attendance):
            table.setItem(row, 0, QTableWidgetItem(student['roll_number']))
            table.setItem(row, 1, QTableWidgetItem(student['name']))
            table.setItem(row, 2, QTableWidgetItem(f"{student['attendance_percentage']:.1f}%"))
            
            status = "⚠️ Warning" if student['attendance_percentage'] < 60 else "⚡ Alert"
            table.setItem(row, 3, QTableWidgetItem(status))
        
        layout.addWidget(table)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
    
    def update_statistics(self):
        """Update statistics display"""
        dept_id = self.department_combo.currentData()
        semester = int(self.semester_combo.currentText())
        
        if dept_id:
            stats = attendance_controller.get_attendance_statistics(dept_id, semester)
            
            if stats:
                self.stats_label.setText(
                    f"📊 Statistics: Total Records: {stats.get('total_records', 0)} | "
                    f"Present: {stats.get('present_count', 0)} | "
                    f"Absent: {stats.get('absent_count', 0)} | "
                    f"Average Attendance: {stats.get('average_percentage', 0):.1f}%"
                )
