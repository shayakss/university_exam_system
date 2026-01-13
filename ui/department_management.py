"""
Department Management Page
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.department_controller import department_controller


class DepartmentManagementPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.departments_data = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Department Management")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()
        
        add_btn = QPushButton("➕ Add Department")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_department)
        header.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_departments)
        header.addWidget(refresh_btn)
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Code", "Department Name", "Head of Department", "Male", "Female"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_department_from_selection)
        action_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_department_from_selection)
        action_layout.addWidget(delete_btn)
        
        layout.addLayout(action_layout)
        
        self.load_departments()
    
    def load_departments(self):
        """Load all departments into table"""
        from controllers.student_controller import student_controller
        
        departments = department_controller.get_all_departments()
        self.departments_data = departments
        
        # CRITICAL: Clear table first
        self.table.clearContents()
        self.table.setRowCount(0)
        
        # Set new row count
        self.table.setRowCount(len(departments))
        
        for row, dept in enumerate(departments):
            self.table.setItem(row, 0, QTableWidgetItem(dept['department_code']))
            self.table.setItem(row, 1, QTableWidgetItem(dept['department_name']))
            self.table.setItem(row, 2, QTableWidgetItem(dept.get('head_of_department', '')))
            
            # Calculate male/female counts
            all_students = student_controller.get_students_by_department(dept['department_id'])
            male_count = len([s for s in all_students if s.get('gender') == 'Male'])
            female_count = len([s for s in all_students if s.get('gender') == 'Female'])
            
            self.table.setItem(row, 3, QTableWidgetItem(str(male_count)))
            self.table.setItem(row, 4, QTableWidgetItem(str(female_count)))
        
        self.table.resizeColumnsToContents()
    
    def add_department(self):
        dialog = DepartmentDialog(self)
        if dialog.exec_():
            self.load_departments()
    
    def edit_department_from_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a department to edit")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.departments_data):
            return
        
        dept = self.departments_data[row]
        dialog = DepartmentDialog(self, dept)
        if dialog.exec_():
            self.load_departments()
    
    def delete_department_from_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a department to delete")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.departments_data):
            return
        
        dept = self.departments_data[row]
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Are you sure you want to delete {dept['department_name']}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, msg = department_controller.delete_department(dept['department_id'])
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_departments()
            else:
                QMessageBox.warning(self, "Error", msg)


class DepartmentDialog(QDialog):
    def __init__(self, parent=None, department=None):
        super().__init__(parent)
        self.department = department
        self.setWindowTitle("Add Department" if not department else "Edit Department")
        self.setFixedSize(400, 200)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        layout.addRow("Department Name:", self.name_input)
        
        self.code_input = QLineEdit()
        layout.addRow("Department Code:", self.code_input)
        
        self.hod_input = QLineEdit()
        layout.addRow("Head of Department:", self.hod_input)
        
        if department:
            self.name_input.setText(department['department_name'])
            self.code_input.setText(department['department_code'])
            self.hod_input.setText(department.get('head_of_department', ''))
        
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
        name = self.name_input.text().strip()
        code = self.code_input.text().strip()
        hod = self.hod_input.text().strip()
        
        if not name or not code:
            QMessageBox.warning(self, "Error", "Please fill all required fields")
            return
        
        if self.department:
            success, msg = department_controller.update_department(
                self.department['department_id'], name, code, hod
            )
        else:
            success, msg, _ = department_controller.create_department(name, code, hod)
        
        if success:
            QMessageBox.information(self, "Success", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", msg)
