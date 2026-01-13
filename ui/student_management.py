"""
Student Management Page - CRUD operations for students
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QDialog,
                             QFormLayout, QComboBox, QDateEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from controllers.student_controller import student_controller
from controllers.department_controller import department_controller


class StudentManagementPage(QWidget):
    """Student management interface"""
    
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.students_data = []
        self.department_id = department_id  # For teacher filtering
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("👥 Student Management")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Header with search and actions
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Search
        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 16px;")
        header_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search students by name, roll number, or email...")
        self.search_input.textChanged.connect(self.search_students)
        self.search_input.setMinimumWidth(300)
        header_layout.addWidget(self.search_input)
        
        header_layout.addStretch()
        
        # Action buttons
        add_btn = QPushButton("➕ Add Student")
        add_btn.setObjectName("primaryButton")
        add_btn.setToolTip("Add a new student")
        add_btn.clicked.connect(self.add_student)
        header_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setObjectName("secondaryButton")
        edit_btn.setToolTip("Edit selected student")
        edit_btn.clicked.connect(self.edit_student_from_selection)
        header_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.setToolTip("Delete selected student")
        delete_btn.clicked.connect(self.delete_student_from_selection)
        header_layout.addWidget(delete_btn)
        
        export_transcript_btn = QPushButton("📄 Transcript")
        export_transcript_btn.setObjectName("secondaryButton")
        export_transcript_btn.setToolTip("Export student transcript as PDF")
        export_transcript_btn.clicked.connect(self.export_transcript)
        header_layout.addWidget(export_transcript_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.setToolTip("Refresh student list")
        refresh_btn.clicked.connect(self.load_students)
        header_layout.addWidget(refresh_btn)
        
        import_btn = QPushButton("📁 Import")
        import_btn.setObjectName("secondaryButton")
        import_btn.setToolTip("Import students from CSV/Excel")
        import_btn.clicked.connect(self.import_students)
        header_layout.addWidget(import_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "Roll Number", "Name", "Father Name", "Registration No", "Department", 
            "Semester", "Gender", "DOB", "Phone", "Guardian Phone", "CNIC", "Email", "Address"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        self.load_students()
    
    def load_students(self):
        """Load all students into table"""
        if self.department_id:
            # Teacher view - only their department
            students = student_controller.get_students_by_department(self.department_id)
        else:
            # Admin view - all students
            students = student_controller.get_all_students()
        self.display_students(students)
    
    def search_students(self):
        """Search students"""
        search_term = self.search_input.text().strip()
        if search_term:
            all_students = student_controller.search_students(search_term)
        else:
            if self.department_id:
                all_students = student_controller.get_students_by_department(self.department_id)
            else:
                all_students = student_controller.get_all_students()
        
        self.display_students(all_students)
    
    def display_students(self, students):
        """Display students in table"""
        self.students_data = students
        
        # CRITICAL: Clear table first to prevent invisible rows
        self.table.clearContents()
        self.table.setRowCount(0)
        
        # Set new row count
        self.table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(student['roll_number']))
            self.table.setItem(row, 1, QTableWidgetItem(student['name']))
            self.table.setItem(row, 2, QTableWidgetItem(student.get('father_name', '') or ''))
            self.table.setItem(row, 3, QTableWidgetItem(student.get('registration_no', '') or ''))
            self.table.setItem(row, 4, QTableWidgetItem(student.get('department_name', '')))
            self.table.setItem(row, 5, QTableWidgetItem(str(student['semester'])))
            self.table.setItem(row, 6, QTableWidgetItem(student.get('gender', '')))
            
            # Convert date_of_birth to string
            dob = student.get('date_of_birth', '')
            if dob:
                dob_str = str(dob) if not isinstance(dob, str) else dob
            else:
                dob_str = "N/A"
            self.table.setItem(row, 7, QTableWidgetItem(dob_str))
            
            self.table.setItem(row, 8, QTableWidgetItem(student.get('phone', '') or ''))
            self.table.setItem(row, 9, QTableWidgetItem(student.get('guardian_phone', '') or ''))
            self.table.setItem(row, 10, QTableWidgetItem(student.get('cnic', '') or ''))
            self.table.setItem(row, 11, QTableWidgetItem(student.get('email', '') or ''))
            self.table.setItem(row, 12, QTableWidgetItem(student.get('address', '') or ''))
        
        self.table.resizeColumnsToContents()
    
    def add_student(self):
        """Open add student dialog"""
        dialog = StudentDialog(self)
        if dialog.exec_():
            self.load_students()
    
    def edit_student_from_selection(self):
        """Edit selected student"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a student to edit")
            return
        
        if len(selected_rows) > 1:
            QMessageBox.warning(self, "Multiple Selection", "Please select only one student to edit")
            return
        
        row = selected_rows[0].row()
        if row < 0 or row >= len(self.students_data):
            return
        
        student = self.students_data[row]
        dialog = StudentDialog(self, student)
        if dialog.exec_():
            self.load_students()
    
    def delete_student_from_selection(self):
        """Delete selected student(s)"""
        try:
            selected_rows = self.table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select student(s) to delete")
                return
            
            count = len(selected_rows)
            msg = f"Are you sure you want to delete {count} student(s)?\n\nThis will also delete all related marks and results."
            if count == 1:
                row = selected_rows[0].row()
                student = self.students_data[row]
                msg = f"Are you sure you want to delete {student['name']}?\n\nThis will also delete all related marks and results."

            reply = QMessageBox.question(
                self, 'Confirm Delete',
                msg,
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success_count = 0
                fail_count = 0
                
                for index in selected_rows:
                    row = index.row()
                    if row < 0 or row >= len(self.students_data):
                        continue
                        
                    student = self.students_data[row]
                    success, _ = student_controller.delete_student(student['student_id'])
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                
                if fail_count == 0:
                    QMessageBox.information(self, "Success", f"Successfully deleted {success_count} student(s).")
                else:
                    QMessageBox.warning(self, "Warning", f"Deleted {success_count} student(s). Failed to delete {fail_count} student(s).")
                
                self.load_students()
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            print(f"Error in delete_student: {e}")
            import traceback
            traceback.print_exc()
            # Refresh table even on error
            self.load_students()
    
    def export_transcript(self):
        """Export transcript for selected student"""
        try:
            selected = self.table.selectedItems()
            if not selected:
                QMessageBox.warning(self, "No Selection", "Please select a student to export transcript")
                return
            
            row = self.table.currentRow()
            if row < 0 or row >= len(self.students_data):
                return
            
            student = self.students_data[row]
            
            # Open transcript export dialog
            from ui.transcript_export import TranscriptExportDialog
            dialog = TranscriptExportDialog(student['student_id'], student['name'], self)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export transcript: {str(e)}")
            print(f"Error in export_transcript: {e}")
            import traceback
            traceback.print_exc()
    
    def import_students(self):
        """Import students from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            success, msg, count = student_controller.bulk_import_students(file_path)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_students()
            else:
                QMessageBox.warning(self, "Error", msg)


class StudentDialog(QDialog):
    """Dialog for adding/editing students"""
    
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()
        if student:
            self.load_student_data()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Edit Student" if self.student else "Add Student")
        self.setFixedSize(600, 650)  # Increased size for new fields
        
        layout = QFormLayout(self)
        
        self.roll_input = QLineEdit()
        layout.addRow("Roll Number:*", self.roll_input)
        
        self.name_input = QLineEdit()
        layout.addRow("Name:*", self.name_input)
        
        self.registration_input = QLineEdit()
        layout.addRow("Registration No:", self.registration_input)
        
        self.dept_combo = QComboBox()
        departments = department_controller.get_all_departments()
        for dept in departments:
            self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        layout.addRow("Department:*", self.dept_combo)
        
        self.semester_combo = QComboBox()
        for i in range(1, 9):
            self.semester_combo.addItem(f"Semester {i}", i)
        layout.addRow("Semester:*", self.semester_combo)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        layout.addRow("Gender:*", self.gender_combo)
        
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate().addYears(-18))
        layout.addRow("Date of Birth:*", self.dob_input)
        
        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("03XX-XXXXXXX")
        layout.addRow("Phone:", self.phone_input)
        
        self.guardian_phone_input = QLineEdit()
        self.guardian_phone_input.setPlaceholderText("03XX-XXXXXXX")
        layout.addRow("Guardian Phone:", self.guardian_phone_input)
        
        self.cnic_input = QLineEdit()
        self.cnic_input.setPlaceholderText("XXXXX-XXXXXXX-X")
        layout.addRow("CNIC:", self.cnic_input)
        
        self.father_name_input = QLineEdit()
        layout.addRow("Father Name:", self.father_name_input)
        
        self.father_cnic_input = QLineEdit()
        self.father_cnic_input.setPlaceholderText("XXXXX-XXXXXXX-X")
        layout.addRow("Father CNIC:", self.father_cnic_input)
        
        self.address_input = QLineEdit()
        layout.addRow("Address:", self.address_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_student)
        btn_layout.addWidget(save_btn)
        
        layout.addRow("", btn_layout)
    
    def load_student_data(self):
        """Load student data into form"""
        self.roll_input.setText(self.student['roll_number'])
        self.name_input.setText(self.student['name'])
        
        # Set department
        for i in range(self.dept_combo.count()):
            if self.dept_combo.itemData(i) == self.student['department_id']:
                self.dept_combo.setCurrentIndex(i)
                break
        
        # Set semester
        self.semester_combo.setCurrentIndex(self.student['semester'] - 1)
        
        # Set gender
        gender = self.student.get('gender', 'Male')
        index = self.gender_combo.findText(gender)
        if index >= 0:
            self.gender_combo.setCurrentIndex(index)
        
        # Set DOB
        dob = self.student.get('date_of_birth')
        if dob:
            if isinstance(dob, str):
                date = QDate.fromString(dob, "yyyy-MM-dd")
            else:
                date = QDate.fromString(str(dob), "yyyy-MM-dd")
            if date.isValid():
                self.dob_input.setDate(date)
        
        # Set other fields
        self.father_name_input.setText(self.student.get('father_name', ''))
        self.cnic_input.setText(self.student.get('cnic', ''))
        self.phone_input.setText(self.student.get('phone', ''))
        self.email_input.setText(self.student.get('email', ''))
        self.address_input.setText(self.student.get('address', ''))
        self.father_cnic_input.setText(self.student.get('father_cnic', ''))
        self.guardian_phone_input.setText(self.student.get('guardian_phone', ''))
        self.registration_input.setText(self.student.get('registration_no', ''))
    
    def save_student(self):
        """Save student data"""
        # Validate inputs
        roll_number = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        department_id = self.dept_combo.currentData()
        semester = self.semester_combo.currentIndex() + 1
        
        if not roll_number or not name:
            QMessageBox.warning(self, "Validation Error", "Roll number and name are required!")
            return
        
        if not department_id:
            QMessageBox.warning(self, "Validation Error", "Please select a department!")
            return
        
        # Prepare student data
        student_data = {
            'roll_number': roll_number,
            'name': name,
            'father_name': self.father_name_input.text().strip(),
            'department_id': department_id,
            'semester': semester,
            'gender': self.gender_combo.currentText(),
            'date_of_birth': self.dob_input.date().toString("yyyy-MM-dd"),
            'cnic': self.cnic_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip(),
            'address': self.address_input.text().strip(),
            'father_cnic': self.father_cnic_input.text().strip(),
            'guardian_phone': self.guardian_phone_input.text().strip(),
            'registration_no': self.registration_input.text().strip()
        }
        
        try:
            if self.student:
                # Update existing student
                success, msg = student_controller.update_student(
                    student_id=self.student['student_id'],
                    roll_number=student_data['roll_number'],
                    name=student_data['name'],
                    department_id=student_data['department_id'],
                    semester=student_data['semester'],
                    gender=student_data['gender'],
                    date_of_birth=student_data['date_of_birth'],
                    email=student_data.get('email'),
                    phone=student_data.get('phone'),
                    address=student_data.get('address'),
                    registration_no=student_data.get('registration_no'),
                    cnic=student_data.get('cnic'),
                    father_name=student_data.get('father_name'),
                    father_cnic=student_data.get('father_cnic'),
                    guardian_phone=student_data.get('guardian_phone')
                )
                if success:
                    QMessageBox.information(self, "Success", msg)
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", msg)
            else:
                # Add new student
                success, msg, student_id = student_controller.create_student(
                    roll_number=student_data['roll_number'],
                    name=student_data['name'],
                    department_id=student_data['department_id'],
                    semester=student_data['semester'],
                    gender=student_data['gender'],
                    date_of_birth=student_data['date_of_birth'],
                    email=student_data.get('email'),
                    phone=student_data.get('phone'),
                    address=student_data.get('address'),
                    registration_no=student_data.get('registration_no'),
                    cnic=student_data.get('cnic'),
                    father_name=student_data.get('father_name'),
                    father_cnic=student_data.get('father_cnic'),
                    guardian_phone=student_data.get('guardian_phone')
                )
                if success:
                    QMessageBox.information(self, "Success", msg)
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


