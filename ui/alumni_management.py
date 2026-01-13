"""
Alumni Management UI
Handles alumni database and employment tracking
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from controllers.alumni_controller import alumni_controller
from controllers.department_controller import department_controller

class AlumniManagementPage(QWidget):
    """Page for managing alumni"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.user_role = user_data.get('role', 'Student')
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🎓 Alumni Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        if self.user_role == 'Admin':
            grad_btn = QPushButton("🎓 Graduate Students")
            grad_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px 15px;")
            grad_btn.clicked.connect(self.show_graduation_dialog)
            header_layout.addWidget(grad_btn)
            
        layout.addLayout(header_layout)
        
        # Search & Filter
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        filter_layout = QHBoxLayout(filter_frame)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name or Roll No...")
        self.search_input.textChanged.connect(self.load_data)
        filter_layout.addWidget(self.search_input)
        
        self.year_combo = QComboBox()
        self.year_combo.addItem("All Years", None)
        current_year = QDate.currentDate().year()
        for year in range(current_year, current_year - 10, -1):
            self.year_combo.addItem(str(year), year)
        self.year_combo.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Year:"))
        filter_layout.addWidget(self.year_combo)
        
        self.dept_combo = QComboBox()
        self.dept_combo.addItem("All Departments", None)
        self.load_departments()
        self.dept_combo.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Dept:"))
        filter_layout.addWidget(self.dept_combo)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["All Status", "Employed", "Unemployed", "Higher Studies", "Self-Employed"])
        self.status_combo.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(self.status_combo)
        
        layout.addWidget(filter_frame)
        
        # Alumni Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Roll No", "Name", "Department", "Grad Year", "CGPA", "Status", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.load_data()
        
    def load_departments(self):
        """Load departments into combo box"""
        try:
            departments = department_controller.get_all_departments()
            for dept in departments:
                self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        except Exception as e:
            print(f"Error loading departments: {e}")

    def load_data(self):
        """Load alumni data based on filters"""
        try:
            search = self.search_input.text()
            year = self.year_combo.currentData()
            dept_id = self.dept_combo.currentData()
            status = self.status_combo.currentText()
            if status == "All Status":
                status = None
                
            alumni = alumni_controller.search_alumni(year, dept_id, status, search)
            self.table.setRowCount(len(alumni))
            
            for row, data in enumerate(alumni):
                self.table.setItem(row, 0, QTableWidgetItem(data['roll_number']))
                self.table.setItem(row, 1, QTableWidgetItem(data['name']))
                self.table.setItem(row, 2, QTableWidgetItem(data['department_code']))
                self.table.setItem(row, 3, QTableWidgetItem(str(data['graduation_year'])))
                self.table.setItem(row, 4, QTableWidgetItem(f"{data['final_cgpa']:.2f}"))
                
                status_item = QTableWidgetItem(data['current_status'])
                if data['current_status'] == 'Employed':
                    status_item.setForeground(Qt.green)
                elif data['current_status'] == 'Unemployed':
                    status_item.setForeground(Qt.red)
                self.table.setItem(row, 5, status_item)
                
                btn = QPushButton("View Profile")
                btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 5px;")
                btn.clicked.connect(lambda checked, d=data: self.show_profile(d))
                self.table.setCellWidget(row, 6, btn)
                
        except Exception as e:
            print(f"Error loading alumni: {e}")

    def show_profile(self, data):
        """Show alumni profile and employment history"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Alumni Profile - {data['name']}")
        dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Info Group
        info_group = QGroupBox("Personal Information")
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel(f"<b>Name:</b> {data['name']}"), 0, 0)
        info_layout.addWidget(QLabel(f"<b>Roll No:</b> {data['roll_number']}"), 0, 1)
        info_layout.addWidget(QLabel(f"<b>Department:</b> {data['department_name']}"), 1, 0)
        info_layout.addWidget(QLabel(f"<b>Grad Year:</b> {data['graduation_year']}"), 1, 1)
        info_layout.addWidget(QLabel(f"<b>Final CGPA:</b> {data['final_cgpa']:.2f}"), 2, 0)
        info_layout.addWidget(QLabel(f"<b>Status:</b> {data['current_status']}"), 2, 1)
        info_layout.addWidget(QLabel(f"<b>Email:</b> {data['contact_email'] or '-'}"), 3, 0)
        info_layout.addWidget(QLabel(f"<b>Phone:</b> {data['contact_phone'] or '-'}"), 3, 1)
        
        layout.addWidget(info_group)
        
        # Employment History
        emp_group = QGroupBox("Employment History")
        emp_layout = QVBoxLayout(emp_group)
        
        emp_table = QTableWidget()
        emp_table.setColumnCount(4)
        emp_table.setHorizontalHeaderLabels(["Company", "Role", "Duration", "Location"])
        emp_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        history = alumni_controller.get_alumni_employment_history(data['alumni_id'])
        emp_table.setRowCount(len(history))
        
        for row, emp in enumerate(history):
            emp_table.setItem(row, 0, QTableWidgetItem(emp['company_name']))
            emp_table.setItem(row, 1, QTableWidgetItem(emp['job_title']))
            
            start = emp['start_date']
            end = emp['end_date'] or "Present"
            emp_table.setItem(row, 2, QTableWidgetItem(f"{start} to {end}"))
            emp_table.setItem(row, 3, QTableWidgetItem(emp['location'] or "-"))
            
        emp_layout.addWidget(emp_table)
        
        add_emp_btn = QPushButton("➕ Add Employment Record")
        add_emp_btn.clicked.connect(lambda: self.show_add_employment_dialog(data['alumni_id'], dialog))
        emp_layout.addWidget(add_emp_btn)
        
        layout.addWidget(emp_group)
        
        dialog.exec_()

    def show_add_employment_dialog(self, alumni_id, parent_dialog):
        """Show dialog to add employment record"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Employment Record")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Company Name:"))
        company_edit = QLineEdit()
        layout.addWidget(company_edit)
        
        layout.addWidget(QLabel("Job Title:"))
        role_edit = QLineEdit()
        layout.addWidget(role_edit)
        
        layout.addWidget(QLabel("Start Date:"))
        start_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDate(QDate.currentDate())
        layout.addWidget(start_date)
        
        layout.addWidget(QLabel("Location:"))
        loc_edit = QLineEdit()
        layout.addWidget(loc_edit)
        
        current_chk = QCheckBox("Currently Working Here")
        current_chk.setChecked(True)
        layout.addWidget(current_chk)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            if not company_edit.text() or not role_edit.text():
                QMessageBox.warning(self, "Error", "Company and Role are required")
                return
                
            success, msg = alumni_controller.add_employment_record(
                alumni_id, company_edit.text(), role_edit.text(),
                start_date.date().toPyDate(), is_current=current_chk.isChecked(),
                location=loc_edit.text()
            )
            
            if success:
                QMessageBox.information(self, "Success", msg)
                parent_dialog.accept() # Close profile to refresh
                # Ideally we should just refresh the table inside profile, but this is simpler
            else:
                QMessageBox.warning(self, "Error", msg)

    def show_graduation_dialog(self):
        """Show dialog to move students to alumni (Mockup for now)"""
        QMessageBox.information(self, "Info", "This feature would allow bulk moving of final year students to the alumni database upon graduation.")
