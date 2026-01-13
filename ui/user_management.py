"""
User Management Page - CRUD operations for users
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
                             QLineEdit, QComboBox, QCheckBox, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.user_controller import user_controller


class UserManagementPage(QWidget):
    """User management interface (Admin only)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("User Management")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Header with buttons
        header_layout = QHBoxLayout()
        
        # Role Filter
        filter_label = QLabel("Filter by Role:")
        header_layout.addWidget(filter_label)
        
        self.role_filter = QComboBox()
        self.role_filter.addItems(["All Roles", "Admin", "Teacher", "Student", "DataEntry"])
        self.role_filter.currentTextChanged.connect(self.load_users)
        header_layout.addWidget(self.role_filter)
        
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add User")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_user)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Users table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Username", "Full Name", "Email", "Role", "Status", "Created"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.doubleClicked.connect(self.edit_user_from_selection)
        layout.addWidget(self.table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_user_from_selection)
        action_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_user_from_selection)
        action_layout.addWidget(delete_btn)
        
        change_pwd_btn = QPushButton("Change Password")
        change_pwd_btn.clicked.connect(self.change_password_from_selection)
        action_layout.addWidget(change_pwd_btn)
        
        layout.addLayout(action_layout)
    
    def load_users(self):
        """Load users into table with filtering"""
        selected_role = self.role_filter.currentText()
        
        if selected_role == "All Roles":
            users = user_controller.get_all_users()
        else:
            users = user_controller.get_users_by_role(selected_role)
            
        self.users_data = users
        
        # CRITICAL: Clear table first to prevent invisible rows
        self.table.clearContents()
        self.table.setRowCount(0)
        
        # Set new row count
        self.table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user['username']))
            self.table.setItem(row, 1, QTableWidgetItem(user['full_name']))
            self.table.setItem(row, 2, QTableWidgetItem(user.get('email', '')))
            self.table.setItem(row, 3, QTableWidgetItem(user['role']))
            
            status = "Active" if user['is_active'] else "Inactive"
            self.table.setItem(row, 4, QTableWidgetItem(status))
            
            # Convert datetime to string
            created_at = user['created_at']
            if created_at:
                created_at_str = str(created_at)[:10] if not isinstance(created_at, str) else created_at[:10]
            else:
                created_at_str = "N/A"
            self.table.setItem(row, 5, QTableWidgetItem(created_at_str))
        
        self.table.resizeColumnsToContents()
    
    def add_user(self):
        """Open add user dialog"""
        try:
            dialog = UserDialog(self)
            if dialog.exec_():
                self.load_users()
        except Exception as e:
            print(f"Error in add_user: {e}")
            import traceback
            traceback.print_exc()
            # Try to reload users anyway
            try:
                self.load_users()
            except:
                pass
    
    def edit_user_from_selection(self):
        """Edit selected user"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a user to edit")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.users_data):
            return
        
        user = self.users_data[row]
        dialog = UserDialog(self, user)
        if dialog.exec_():
            self.load_users()
    
    def delete_user_from_selection(self):
        """Delete selected user"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a user to delete")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.users_data):
            return
        
        user = self.users_data[row]
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Are you sure you want to delete user '{user['username']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, msg = user_controller.delete_user(user['user_id'])
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", msg)
    
    def change_password_from_selection(self):
        """Change password for selected user"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a user")
            return
        
        row = self.table.currentRow()
        if row < 0 or row >= len(self.users_data):
            return
        
        user = self.users_data[row]
        
        password, ok = QInputDialog.getText(
            self, "Change Password",
            f"Enter new password for {user['username']}:",
            QLineEdit.Password
        )
        
        if ok and password:
            from utils.validators import validate_password_strength
            is_valid, msg = validate_password_strength(password)
            if not is_valid:
                QMessageBox.warning(self, "Error", msg)
                return
            
            success, msg = user_controller.update_user_password(user['user_id'], password)
            if success:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.warning(self, "Error", msg)


class UserDialog(QDialog):
    """Dialog for adding/editing users"""
    
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        if user:
            self.load_user_data()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Edit User" if self.user else "Add User")
        self.setMinimumSize(450, 600)
        
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        self.username_input = QLineEdit()
        layout.addRow("Username:*", self.username_input)
        
        self.full_name_input = QLineEdit()
        layout.addRow("Full Name:*", self.full_name_input)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Teacher", "Student", "DataEntry"])
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        layout.addRow("Role:*", self.role_combo)
        
        # Email field (required for Teacher/Student)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        self.email_label = QLabel("Email:")
        layout.addRow(self.email_label, self.email_input)
        
        # Department field (required for Teacher)
        self.dept_combo = QComboBox()
        self.dept_combo.addItem("-- Select Department --", None)
        
        try:
            from controllers.department_controller import department_controller
            departments = department_controller.get_all_departments()
            for dept in departments:
                self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        except Exception as e:
            print(f"Warning: Could not load departments: {e}")
        
        self.dept_label = QLabel("Department:")
        layout.addRow(self.dept_label, self.dept_combo)
        
        # Subject field (optional/required for Teacher)
        self.subject_combo = QComboBox()
        self.subject_combo.addItem("-- Select Subject (Optional) --", None)
        self.subject_label = QLabel("Assigned Subject:")
        layout.addRow(self.subject_label, self.subject_combo)
        
        # Connect department change to load subjects
        self.dept_combo.currentIndexChanged.connect(self.load_department_courses)
        
        # Roll Number field (required for Student)
        self.roll_number_input = QLineEdit()
        self.roll_number_input.setPlaceholderText("Enter student's roll number")
        self.roll_number_label = QLabel("Roll Number:")
        layout.addRow(self.roll_number_label, self.roll_number_input)
        
        # Password fields
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Min 8 chars, uppercase, lowercase, number")
        layout.addRow("Password:*", self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Confirm Password:*", self.confirm_password_input)
        
        self.active_checkbox = QCheckBox("Active")
        self.active_checkbox.setChecked(True)
        layout.addRow("Status:", self.active_checkbox)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_user)
        btn_layout.addWidget(save_btn)
        
        layout.addRow("", btn_layout)
        
        # Initially hide email, department, and subject fields
        self.on_role_changed(self.role_combo.currentText())
        
    def load_department_courses(self):
        """Load courses for selected department"""
        self.subject_combo.clear()
        self.subject_combo.addItem("-- Select Subject (Optional) --", None)
        
        dept_id = self.dept_combo.currentData()
        if dept_id:
            try:
                from controllers.course_controller import course_controller
                courses = course_controller.get_courses_by_department(dept_id)
                for course in courses:
                    self.subject_combo.addItem(f"{course['course_code']} - {course['course_name']}", course['course_id'])
            except Exception as e:
                print(f"Error loading courses: {e}")
    
    def on_role_changed(self, role):
        """Show/hide fields based on selected role"""
        # Email required for Teacher and Student
        show_email = role in ['Teacher', 'Student']
        self.email_label.setVisible(show_email)
        self.email_input.setVisible(show_email)
        
        # Department required for Teacher only
        show_dept = role == 'Teacher'
        self.dept_label.setVisible(show_dept)
        self.dept_combo.setVisible(show_dept)
        self.subject_label.setVisible(show_dept)
        self.subject_combo.setVisible(show_dept)
        
        # Roll number required for Student only
        show_roll = role == 'Student'
        self.roll_number_label.setVisible(show_roll)
        self.roll_number_input.setVisible(show_roll)
        
        # Update labels
        if show_email:
            self.email_label.setText("Email:*")
        else:
            self.email_label.setText("Email:")
        
        if show_dept:
            self.dept_label.setText("Department:*")
        else:
            self.dept_label.setText("Department:")
        
        if show_roll:
            self.roll_number_label.setText("Roll Number:*")
        else:
            self.roll_number_label.setText("Roll Number:")
    
    def load_user_data(self):
        """Load user data into form"""
        self.username_input.setText(self.user['username'])
        self.full_name_input.setText(self.user['full_name'])
        
        # Set role
        index = self.role_combo.findText(self.user['role'])
        if index >= 0:
            self.role_combo.setCurrentIndex(index)
        
        # Set email if exists
        if self.user.get('email'):
            self.email_input.setText(self.user['email'])
        
        # Set department if exists
        if self.user.get('department_id'):
            for i in range(self.dept_combo.count()):
                if self.dept_combo.itemData(i) == self.user['department_id']:
                    self.dept_combo.setCurrentIndex(i)
                    break
            
            # Load courses for this department
            self.load_department_courses()
            
            # Set assigned subject if exists
            if self.user.get('assigned_subject_id'):
                for i in range(self.subject_combo.count()):
                    if self.subject_combo.itemData(i) == self.user['assigned_subject_id']:
                        self.subject_combo.setCurrentIndex(i)
                        break
        
        self.active_checkbox.setChecked(bool(self.user['is_active']))
        
        # Password not required for edit
        self.password_input.setPlaceholderText("Leave blank to keep current password")
        self.confirm_password_input.setPlaceholderText("Leave blank to keep current password")
    
    def save_user(self):
        """Save user"""
        try:
            username = self.username_input.text().strip()
            full_name = self.full_name_input.text().strip()
            role = self.role_combo.currentText()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()
            is_active = 1 if self.active_checkbox.isChecked() else 0
            
            # Get email, department, roll number, and assigned subject
            email = self.email_input.text().strip() if self.email_input.isVisible() else None
            department_id = self.dept_combo.currentData() if self.dept_combo.isVisible() else None
            assigned_subject_id = self.subject_combo.currentData() if self.subject_combo.isVisible() else None
            roll_number = self.roll_number_input.text().strip() if self.roll_number_input.isVisible() else None
            
            # Validation
            if not all([username, full_name, role]):
                QMessageBox.warning(self, "Error", "Please fill in all required fields")
                return
            
            # Email required for Teacher/Student
            if role in ['Teacher', 'Student'] and not email:
                QMessageBox.warning(self, "Error", f"Email is required for {role} role")
                return
            
            # Department required for Teacher
            if role == 'Teacher' and not department_id:
                QMessageBox.warning(self, "Error", "Department is required for Teacher role")
                return
            
            # Roll number required for Student
            if role == 'Student' and not roll_number:
                QMessageBox.warning(self, "Error", "Roll number is required for Student role")
                return
            
            # Password validation for new users
            if not self.user:
                if not password:
                    QMessageBox.warning(self, "Error", "Password is required")
                    return
                
                if password != confirm_password:
                    QMessageBox.warning(self, "Error", "Passwords do not match")
                    return
            else:
                # For existing users, only validate if password is provided
                if password and password != confirm_password:
                    QMessageBox.warning(self, "Error", "Passwords do not match")
                    return
            
            if self.user:
                # Update existing user
                success, msg = user_controller.update_user(
                    self.user['user_id'], username, full_name, role, is_active, assigned_subject_id
                )
                
                # Update password if provided
                if success and password:
                    success, msg = user_controller.update_user_password(self.user['user_id'], password)
            else:
                # Create new user
                success, msg, _ = user_controller.create_user(
                    username, password, full_name, role, email, department_id, roll_number, assigned_subject_id
                )
            
            if success:
                QMessageBox.information(self, "Success", msg)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", msg)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            print(f"Error in save_user: {e}")
            import traceback
            traceback.print_exc()
