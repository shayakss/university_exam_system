"""
Student Promotion UI
Handles student promotion to next semester
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.promotion_controller import promotion_controller
from controllers.department_controller import department_controller

class StudentPromotionPage(QWidget):
    """Page for promoting students to next semester"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.user_id = user_data.get('user_id')
        self.user_role = user_data.get('role', 'Student')
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🎓 Student Promotion")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        if self.user_role == 'Admin':
            rules_btn = QPushButton("⚙️ Promotion Rules")
            rules_btn.clicked.connect(self.show_rules_dialog)
            header_layout.addWidget(rules_btn)
            
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_promotion_tab(), "Promotion Wizard")
        self.tabs.addTab(self.create_history_tab(), "Promotion History")
        layout.addWidget(self.tabs)
        
    def create_promotion_tab(self):
        """Create the promotion wizard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Selection Area
        selection_group = QGroupBox("Select Class to Promote")
        selection_layout = QGridLayout(selection_group)
        
        selection_layout.addWidget(QLabel("Department:"), 0, 0)
        self.dept_combo = QComboBox()
        self.load_departments()
        selection_layout.addWidget(self.dept_combo, 0, 1)
        
        selection_layout.addWidget(QLabel("Current Semester:"), 0, 2)
        self.sem_combo = QComboBox()
        self.sem_combo.addItems([str(i) for i in range(1, 9)])
        selection_layout.addWidget(self.sem_combo, 0, 3)
        
        check_btn = QPushButton("Check Eligibility")
        check_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        check_btn.clicked.connect(self.check_eligibility)
        selection_layout.addWidget(check_btn, 0, 4)
        
        layout.addWidget(selection_group)
        
        # Results Area
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Roll No", "Name", "Status", "Reason", "Action"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)
        
        # Bulk Action Area
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.promote_all_btn = QPushButton("Promote All Eligible")
        self.promote_all_btn.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; padding: 10px 20px;")
        self.promote_all_btn.clicked.connect(self.promote_all)
        self.promote_all_btn.setEnabled(False)
        action_layout.addWidget(self.promote_all_btn)
        
        layout.addLayout(action_layout)
        
        return widget
        
    def create_history_tab(self):
        """Create the history tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["Date", "Student", "From Sem", "To Sem", "Promoted By", "Remarks"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        return widget
        
    def load_departments(self):
        """Load departments into combo box"""
        try:
            departments = department_controller.get_all_departments()
            for dept in departments:
                self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        except Exception as e:
            print(f"Error loading departments: {e}")
            
    def check_eligibility(self):
        """Check eligibility for selected class"""
        dept_id = self.dept_combo.currentData()
        semester = int(self.sem_combo.currentText())
        
        # This is a bit tricky because the controller has bulk_promote but not bulk_check
        # So we'll use bulk_promote logic but without committing, or just iterate students
        # For now, let's just use the bulk_promote method but catch the result without doing it? 
        # No, that would promote them. We need to iterate.
        
        try:
            # Get students directly (need to import student_controller or use db)
            from database.db_manager import db
            students_query = "SELECT student_id, roll_number, name FROM students WHERE department_id = ? AND semester = ? AND is_active = 1"
            students = db.execute_query(students_query, (dept_id, semester))
            
            self.results_table.setRowCount(0)
            eligible_count = 0
            
            for row, student in enumerate(students):
                self.results_table.insertRow(row)
                self.results_table.setItem(row, 0, QTableWidgetItem(student['roll_number']))
                self.results_table.setItem(row, 1, QTableWidgetItem(student['name']))
                
                eligible, message, details = promotion_controller.check_promotion_eligibility(student['student_id'], semester)
                
                status_item = QTableWidgetItem("Eligible" if eligible else "Not Eligible")
                status_item.setForeground(Qt.green if eligible else Qt.red)
                self.results_table.setItem(row, 2, status_item)
                
                self.results_table.setItem(row, 3, QTableWidgetItem(message))
                
                if eligible:
                    eligible_count += 1
                    btn = QPushButton("Promote")
                    btn.setStyleSheet("background-color: #2ecc71; color: white;")
                    btn.clicked.connect(lambda checked, s=student: self.promote_single(s, semester))
                    self.results_table.setCellWidget(row, 4, btn)
                else:
                    self.results_table.setItem(row, 4, QTableWidgetItem("-"))
            
            self.promote_all_btn.setEnabled(eligible_count > 0)
            QMessageBox.information(self, "Check Complete", f"Found {eligible_count} eligible students out of {len(students)}")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to check eligibility: {str(e)}")

    def promote_single(self, student, semester):
        """Promote a single student"""
        confirm = QMessageBox.question(self, "Confirm Promotion", 
                                     f"Are you sure you want to promote {student['name']} to semester {semester + 1}?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            success, message = promotion_controller.promote_student(student['student_id'], semester, self.user_id)
            if success:
                QMessageBox.information(self, "Success", message)
                self.check_eligibility() # Refresh
            else:
                QMessageBox.warning(self, "Error", message)

    def promote_all(self):
        """Promote all eligible students"""
        dept_id = self.dept_combo.currentData()
        semester = int(self.sem_combo.currentText())
        
        confirm = QMessageBox.question(self, "Confirm Bulk Promotion", 
                                     f"Are you sure you want to promote ALL eligible students in this class?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            success, message, summary = promotion_controller.bulk_promote_students(dept_id, semester, self.user_id)
            if success:
                QMessageBox.information(self, "Success", message)
                self.check_eligibility() # Refresh
            else:
                QMessageBox.warning(self, "Error", message)

    def load_history(self):
        """Load promotion history"""
        try:
            history = promotion_controller.get_promotion_history()
            self.history_table.setRowCount(len(history))
            
            for row, record in enumerate(history):
                self.history_table.setItem(row, 0, QTableWidgetItem(record['promotion_date']))
                self.history_table.setItem(row, 1, QTableWidgetItem(f"{record['roll_number']} - {record['student_name']}"))
                self.history_table.setItem(row, 2, QTableWidgetItem(str(record['from_semester'])))
                self.history_table.setItem(row, 3, QTableWidgetItem(str(record['to_semester'])))
                self.history_table.setItem(row, 4, QTableWidgetItem(record['promoted_by_name']))
                self.history_table.setItem(row, 5, QTableWidgetItem(record['remarks'] or "-"))
        except Exception as e:
            print(f"Error loading history: {e}")

    def show_rules_dialog(self):
        """Show dialog to manage promotion rules"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Promotion Rules")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # List existing rules
        rules_table = QTableWidget()
        rules_table.setColumnCount(5)
        rules_table.setHorizontalHeaderLabels(["Name", "Min CGPA", "Max F Grades", "Min Attendance %", "Active"])
        rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        rules = promotion_controller.get_promotion_rules()
        rules_table.setRowCount(len(rules))
        for row, rule in enumerate(rules):
            rules_table.setItem(row, 0, QTableWidgetItem(rule['rule_name']))
            rules_table.setItem(row, 1, QTableWidgetItem(str(rule['min_cgpa'])))
            rules_table.setItem(row, 2, QTableWidgetItem(str(rule['max_f_grades'])))
            rules_table.setItem(row, 3, QTableWidgetItem(str(rule['min_attendance_percentage'])))
            rules_table.setItem(row, 4, QTableWidgetItem("Yes" if rule['is_active'] else "No"))
            
        layout.addWidget(rules_table)
        
        # Add new rule form
        form_group = QGroupBox("Add New Rule")
        form_layout = QGridLayout(form_group)
        
        name_edit = QLineEdit()
        cgpa_spin = QDoubleSpinBox()
        cgpa_spin.setValue(2.0)
        f_spin = QSpinBox()
        att_spin = QDoubleSpinBox()
        att_spin.setValue(75.0)
        
        form_layout.addWidget(QLabel("Rule Name:"), 0, 0)
        form_layout.addWidget(name_edit, 0, 1)
        form_layout.addWidget(QLabel("Min CGPA:"), 0, 2)
        form_layout.addWidget(cgpa_spin, 0, 3)
        form_layout.addWidget(QLabel("Max F Grades:"), 1, 0)
        form_layout.addWidget(f_spin, 1, 1)
        form_layout.addWidget(QLabel("Min Attendance %:"), 1, 2)
        form_layout.addWidget(att_spin, 1, 3)
        
        add_btn = QPushButton("Add Rule")
        add_btn.clicked.connect(lambda: self.add_rule(name_edit.text(), cgpa_spin.value(), f_spin.value(), att_spin.value(), dialog))
        form_layout.addWidget(add_btn, 2, 0, 1, 4)
        
        layout.addWidget(form_group)
        
        dialog.exec_()

    def add_rule(self, name, cgpa, f_grades, att, dialog):
        """Add a new promotion rule"""
        if not name:
            QMessageBox.warning(dialog, "Error", "Rule name is required")
            return
            
        success, msg = promotion_controller.create_promotion_rule(name, cgpa, f_grades, att)
        if success:
            QMessageBox.information(dialog, "Success", msg)
            dialog.accept() # Close to refresh
            self.show_rules_dialog() # Reopen
        else:
            QMessageBox.warning(dialog, "Error", msg)
