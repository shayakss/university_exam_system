"""
Audit Viewer UI
Handles viewing and filtering of system audit logs
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from controllers.audit_controller import audit_controller
from controllers.user_controller import user_controller
import json

class AuditViewerPage(QWidget):
    """Page for viewing system audit logs"""
    
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
        title = QLabel("📜 Audit Logs")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        if self.user_role == 'Admin':
            cleanup_btn = QPushButton("🗑️ Cleanup Old Logs")
            cleanup_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 15px;")
            cleanup_btn.clicked.connect(self.show_cleanup_dialog)
            header_layout.addWidget(cleanup_btn)
            
        layout.addLayout(header_layout)
        
        # Filter Area
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        filter_layout = QGridLayout(filter_frame)
        
        # Row 1
        filter_layout.addWidget(QLabel("User:"), 0, 0)
        self.user_combo = QComboBox()
        self.user_combo.addItem("All Users", None)
        self.load_users()
        filter_layout.addWidget(self.user_combo, 0, 1)
        
        filter_layout.addWidget(QLabel("Action Type:"), 0, 2)
        self.action_combo = QComboBox()
        self.action_combo.addItems(["All Actions", "LOGIN", "LOGOUT", "CREATE", "UPDATE", "DELETE"])
        filter_layout.addWidget(self.action_combo, 0, 3)
        
        filter_layout.addWidget(QLabel("Table:"), 0, 4)
        self.table_combo = QComboBox()
        self.table_combo.addItems(["All Tables", "students", "users", "courses", "departments", "marks", "results"])
        filter_layout.addWidget(self.table_combo, 0, 5)
        
        # Row 2
        filter_layout.addWidget(QLabel("Start Date:"), 1, 0)
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        filter_layout.addWidget(self.start_date, 1, 1)
        
        filter_layout.addWidget(QLabel("End Date:"), 1, 2)
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date, 1, 3)
        
        search_btn = QPushButton("Search Logs")
        search_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        search_btn.clicked.connect(self.load_logs)
        filter_layout.addWidget(search_btn, 1, 4, 1, 2)
        
        layout.addWidget(filter_frame)
        
        # Logs Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Time", "User", "Action", "Table", "Description", "IP Address", "Details"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        self.load_logs()
        
    def load_users(self):
        """Load users into combo box"""
        try:
            users = user_controller.get_all_users()
            for user in users:
                self.user_combo.addItem(user['username'], user['user_id'])
        except Exception as e:
            print(f"Error loading users: {e}")

    def load_logs(self):
        """Load logs based on filters"""
        try:
            user_id = self.user_combo.currentData()
            action = self.action_combo.currentText()
            if action == "All Actions":
                action = None
            
            table_name = self.table_combo.currentText()
            if table_name == "All Tables":
                table_name = None
                
            start = self.start_date.date().toPyDate()
            end = self.end_date.date().toPyDate()
            
            logs = audit_controller.get_audit_logs(user_id, action, table_name, start, end)
            self.table.setRowCount(len(logs))
            
            for row, log in enumerate(logs):
                self.table.setItem(row, 0, QTableWidgetItem(str(log['timestamp'])))
                self.table.setItem(row, 1, QTableWidgetItem(log['username']))
                
                action_item = QTableWidgetItem(log['action_type'])
                if log['action_type'] == 'DELETE':
                    action_item.setForeground(Qt.red)
                elif log['action_type'] == 'CREATE':
                    action_item.setForeground(Qt.green)
                elif log['action_type'] == 'UPDATE':
                    action_item.setForeground(Qt.blue)
                self.table.setItem(row, 2, action_item)
                
                self.table.setItem(row, 3, QTableWidgetItem(log['table_name'] or "-"))
                self.table.setItem(row, 4, QTableWidgetItem(log['action_description']))
                self.table.setItem(row, 5, QTableWidgetItem(log['ip_address'] or "-"))
                
                btn = QPushButton("View Details")
                btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 5px;")
                btn.clicked.connect(lambda checked, l=log: self.show_log_details(l))
                self.table.setCellWidget(row, 6, btn)
                
        except Exception as e:
            print(f"Error loading logs: {e}")

    def show_log_details(self, log):
        """Show full details of a log entry"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Log Details - {log['timestamp']}")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Basic Info
        info_text = f"""
        <b>Timestamp:</b> {log['timestamp']}<br>
        <b>User:</b> {log['username']} (ID: {log['user_id']})<br>
        <b>Action:</b> {log['action_type']}<br>
        <b>Table:</b> {log['table_name'] or 'N/A'}<br>
        <b>Record ID:</b> {log['record_id'] or 'N/A'}<br>
        <b>IP Address:</b> {log['ip_address'] or 'N/A'}<br>
        <b>Description:</b> {log['action_description']}
        """
        info_label = QLabel(info_text)
        info_label.setTextFormat(Qt.RichText)
        layout.addWidget(info_label)
        
        # Changes
        if log['old_value'] or log['new_value']:
            layout.addWidget(QLabel("<b>Changes:</b>"))
            
            changes_layout = QHBoxLayout()
            
            if log['old_value']:
                old_group = QGroupBox("Old Value")
                old_layout = QVBoxLayout(old_group)
                old_text = QTextEdit()
                old_text.setReadOnly(True)
                try:
                    formatted = json.dumps(json.loads(log['old_value']), indent=2)
                    old_text.setText(formatted)
                except:
                    old_text.setText(log['old_value'])
                old_layout.addWidget(old_text)
                changes_layout.addWidget(old_group)
                
            if log['new_value']:
                new_group = QGroupBox("New Value")
                new_layout = QVBoxLayout(new_group)
                new_text = QTextEdit()
                new_text.setReadOnly(True)
                try:
                    formatted = json.dumps(json.loads(log['new_value']), indent=2)
                    new_text.setText(formatted)
                except:
                    new_text.setText(log['new_value'])
                new_layout.addWidget(new_text)
                changes_layout.addWidget(new_group)
                
            layout.addLayout(changes_layout)
            
        btn = QPushButton("Close")
        btn.clicked.connect(dialog.accept)
        layout.addWidget(btn)
        
        dialog.exec_()

    def show_cleanup_dialog(self):
        """Show dialog to cleanup old logs"""
        days, ok = QInputDialog.getInt(self, "Cleanup Logs", 
                                     "Delete logs older than (days):", 
                                     365, 30, 3650)
        if ok:
            confirm = QMessageBox.question(self, "Confirm Cleanup", 
                                         f"Are you sure you want to delete all logs older than {days} days?\nThis action cannot be undone.",
                                         QMessageBox.Yes | QMessageBox.No)
            
            if confirm == QMessageBox.Yes:
                success, msg = audit_controller.cleanup_old_logs(days)
                if success:
                    QMessageBox.information(self, "Success", msg)
                    self.load_logs()
                else:
                    QMessageBox.warning(self, "Error", msg)
