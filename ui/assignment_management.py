"""
Assignment Management UI
Handles assignment creation, submission, and grading
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from controllers.assignment_controller import assignment_controller
from controllers.course_controller import course_controller
from datetime import datetime

class AssignmentManagementPage(QWidget):
    """Page for managing assignments (Teacher) and submissions (Student)"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.user_role = user_data.get('role', 'Student')
        self.user_id = user_data.get('user_id')
        self.student_id = user_data.get('student_id')
        
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """Initialize UI based on role"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📝 Assignment Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        if self.user_role in ['Teacher', 'Admin']:
            add_btn = QPushButton("➕ Create Assignment")
            add_btn.setFixedWidth(200)
            add_btn.clicked.connect(self.show_create_dialog)
            header_layout.addWidget(add_btn)
            
        layout.addLayout(header_layout)
        
        # Filter Area
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        filter_layout = QHBoxLayout(filter_frame)
        
        if self.user_role in ['Teacher', 'Admin']:
            self.course_combo = QComboBox()
            self.course_combo.addItem("All Courses", None)
            self.course_combo.currentIndexChanged.connect(self.load_data)
            filter_layout.addWidget(QLabel("Filter by Course:"))
            filter_layout.addWidget(self.course_combo)
            
        status_label = QLabel("Status:")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["All", "Pending", "Submitted", "Late", "Graded"])
        self.status_combo.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_combo)
        
        filter_layout.addStretch()
        layout.addWidget(filter_frame)
        
        # Assignments Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        # Configure columns based on role
        if self.user_role in ['Teacher', 'Admin']:
            columns = ["ID", "Title", "Course", "Due Date", "Total Marks", "Submitted", "Pending", "Actions"]
        else:
            columns = ["ID", "Title", "Course", "Due Date", "Status", "Marks", "Actions"]
            
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        
        # Load courses for filter
        if self.user_role in ['Teacher', 'Admin']:
            self.load_courses()

    def load_courses(self):
        """Load courses into combo box"""
        try:
            if self.user_role == 'Teacher':
                courses = course_controller.get_courses_by_teacher(self.user_id)
            else:
                courses = course_controller.get_all_courses()
                
            for course in courses:
                self.course_combo.addItem(f"{course['course_code']} - {course['course_name']}", course['course_id'])
        except Exception as e:
            print(f"Error loading courses: {e}")

    def load_data(self):
        """Load assignments based on filters"""
        try:
            self.table.setRowCount(0)
            
            if self.user_role in ['Teacher', 'Admin']:
                course_id = self.course_combo.currentData()
                teacher_id = self.user_id if self.user_role == 'Teacher' else None
                assignments = assignment_controller.get_assignments(course_id, teacher_id)
            else:
                status = self.status_combo.currentText()
                if status == "All":
                    status = None
                assignments = assignment_controller.get_student_assignments(self.student_id, status)
            
            for row, data in enumerate(assignments):
                self.table.insertRow(row)
                
                if self.user_role in ['Teacher', 'Admin']:
                    self.table.setItem(row, 0, QTableWidgetItem(str(data['assignment_id'])))
                    self.table.setItem(row, 1, QTableWidgetItem(data['title']))
                    self.table.setItem(row, 2, QTableWidgetItem(f"{data['course_code']} - {data['course_name']}"))
                    self.table.setItem(row, 3, QTableWidgetItem(data['due_date']))
                    self.table.setItem(row, 4, QTableWidgetItem(str(data['total_marks'])))
                    self.table.setItem(row, 5, QTableWidgetItem(str(data['submitted_count'])))
                    self.table.setItem(row, 6, QTableWidgetItem(str(data['pending_count'])))
                    
                    # Actions
                    btn_widget = QWidget()
                    btn_layout = QHBoxLayout(btn_widget)
                    btn_layout.setContentsMargins(0, 0, 0, 0)
                    
                    view_btn = QPushButton("View Submissions")
                    view_btn.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
                    view_btn.clicked.connect(lambda checked, aid=data['assignment_id']: self.view_submissions(aid))
                    btn_layout.addWidget(view_btn)
                    
                    self.table.setCellWidget(row, 7, btn_widget)
                    
                else:
                    self.table.setItem(row, 0, QTableWidgetItem(str(data['assignment_id'])))
                    self.table.setItem(row, 1, QTableWidgetItem(data['title']))
                    self.table.setItem(row, 2, QTableWidgetItem(f"{data['course_code']} - {data['course_name']}"))
                    self.table.setItem(row, 3, QTableWidgetItem(data['due_date']))
                    
                    status_item = QTableWidgetItem(data['submission_status'])
                    if data['submission_status'] == 'Pending':
                        status_item.setForeground(Qt.red)
                    elif data['submission_status'] == 'Submitted':
                        status_item.setForeground(Qt.blue)
                    elif data['submission_status'] == 'Graded':
                        status_item.setForeground(Qt.green)
                    self.table.setItem(row, 4, status_item)
                    
                    marks = f"{data['marks_obtained']}/{data['total_marks']}" if data['marks_obtained'] is not None else "-"
                    self.table.setItem(row, 5, QTableWidgetItem(marks))
                    
                    # Actions
                    btn_widget = QWidget()
                    btn_layout = QHBoxLayout(btn_widget)
                    btn_layout.setContentsMargins(0, 0, 0, 0)
                    
                    if data['submission_status'] in ['Pending', 'Late']:
                        submit_btn = QPushButton("Submit")
                        submit_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 5px;")
                        submit_btn.clicked.connect(lambda checked, aid=data['assignment_id']: self.show_submit_dialog(aid))
                        btn_layout.addWidget(submit_btn)
                    else:
                        view_btn = QPushButton("View Details")
                        view_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 5px;")
                        view_btn.clicked.connect(lambda checked, d=data: self.show_submission_details(d))
                        btn_layout.addWidget(view_btn)
                        
                    self.table.setCellWidget(row, 6, btn_widget)
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load assignments: {str(e)}")

    def show_create_dialog(self):
        """Show dialog to create new assignment"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Assignment")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Course Selection
        layout.addWidget(QLabel("Course:"))
        course_combo = QComboBox()
        courses = course_controller.get_courses_by_teacher(self.user_id) if self.user_role == 'Teacher' else course_controller.get_all_courses()
        for course in courses:
            course_combo.addItem(f"{course['course_code']} - {course['course_name']}", course['course_id'])
        layout.addWidget(course_combo)
        
        # Title
        layout.addWidget(QLabel("Title:"))
        title_edit = QLineEdit()
        layout.addWidget(title_edit)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        desc_edit = QTextEdit()
        desc_edit.setMaximumHeight(100)
        layout.addWidget(desc_edit)
        
        # Due Date
        layout.addWidget(QLabel("Due Date:"))
        due_date_edit = QDateEdit()
        due_date_edit.setDate(QDate.currentDate().addDays(7))
        due_date_edit.setCalendarPopup(True)
        layout.addWidget(due_date_edit)
        
        # Total Marks
        layout.addWidget(QLabel("Total Marks:"))
        marks_spin = QSpinBox()
        marks_spin.setRange(1, 100)
        marks_spin.setValue(10)
        layout.addWidget(marks_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Create")
        save_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            course_id = course_combo.currentData()
            title = title_edit.text()
            desc = desc_edit.toPlainText()
            due_date = due_date_edit.date().toPyDate()
            marks = marks_spin.value()
            
            if not title:
                QMessageBox.warning(self, "Error", "Title is required")
                return
                
            success, message = assignment_controller.create_assignment(
                course_id, self.user_id, title, desc, due_date, marks
            )
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", message)

    def view_submissions(self, assignment_id):
        """View submissions for an assignment"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Assignment Submissions")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Student ID", "Name", "Status", "Submitted On", "Marks", "Action"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        submissions = assignment_controller.get_assignment_submissions(assignment_id)
        table.setRowCount(len(submissions))
        
        for row, sub in enumerate(submissions):
            table.setItem(row, 0, QTableWidgetItem(sub['roll_number']))
            table.setItem(row, 1, QTableWidgetItem(sub['student_name']))
            table.setItem(row, 2, QTableWidgetItem(sub['status']))
            table.setItem(row, 3, QTableWidgetItem(str(sub['submission_date'] or '-')))
            
            marks = str(sub['marks_obtained']) if sub['marks_obtained'] is not None else "-"
            table.setItem(row, 4, QTableWidgetItem(marks))
            
            if sub['status'] in ['Submitted', 'Late', 'Graded']:
                grade_btn = QPushButton("Grade")
                grade_btn.clicked.connect(lambda checked, s=sub: self.show_grade_dialog(s, dialog))
                table.setCellWidget(row, 5, grade_btn)
            else:
                table.setItem(row, 5, QTableWidgetItem("Pending"))
                
        layout.addWidget(table)
        dialog.exec_()

    def show_grade_dialog(self, submission, parent_dialog):
        """Show dialog to grade a submission"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Grade Submission - {submission['student_name']}")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel(f"Submission Date: {submission['submission_date']}"))
        layout.addWidget(QLabel(f"Remarks: {submission['remarks'] or 'None'}"))
        
        layout.addWidget(QLabel("Marks Obtained:"))
        marks_spin = QDoubleSpinBox()
        marks_spin.setRange(0, 100) # Should ideally be capped at total marks
        if submission['marks_obtained']:
            marks_spin.setValue(float(submission['marks_obtained']))
        layout.addWidget(marks_spin)
        
        layout.addWidget(QLabel("Feedback:"))
        feedback_edit = QTextEdit()
        feedback_edit.setMaximumHeight(100)
        if submission['remarks']: # This field is overloaded in controller for student remarks vs teacher feedback
             feedback_edit.setText(submission['remarks']) # Need to check if controller separates these
        layout.addWidget(feedback_edit)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Grade")
        save_btn.clicked.connect(dialog.accept)
        layout.addLayout(btn_layout)
        btn_layout.addWidget(save_btn)
        
        if dialog.exec_() == QDialog.Accepted:
            success, msg = assignment_controller.grade_assignment(
                submission['submission_id'], marks_spin.value(), feedback_edit.toPlainText()
            )
            if success:
                QMessageBox.information(self, "Success", msg)
                parent_dialog.accept() # Close list to refresh
                self.view_submissions(submission['assignment_id']) # Reopen list
            else:
                QMessageBox.warning(self, "Error", msg)

    def show_submit_dialog(self, assignment_id):
        """Show dialog for student to submit assignment"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Submit Assignment")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Submission Text / Link:"))
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        
        btn_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(dialog.accept)
        layout.addLayout(btn_layout)
        btn_layout.addWidget(submit_btn)
        
        if dialog.exec_() == QDialog.Accepted:
            success, msg = assignment_controller.submit_assignment(
                assignment_id, self.student_id, remarks=text_edit.toPlainText()
            )
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", msg)

    def show_submission_details(self, data):
        """Show details of a submitted assignment"""
        QMessageBox.information(self, "Submission Details",
            f"Title: {data['title']}\n"
            f"Status: {data['submission_status']}\n"
            f"Marks: {data['marks_obtained']}/{data['total_marks']}\n"
            f"Feedback: {data['submission_remarks'] or 'None'}"
        )
