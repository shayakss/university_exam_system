"""
Backup and Restore Page
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.db_manager import db
from datetime import datetime
import os


class BackupRestorePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Backup & Restore")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Backup section
        backup_group = QGroupBox("Create Backup")
        backup_layout = QVBoxLayout(backup_group)
        
        info_label = QLabel("Create a backup of the database to protect your data.")
        backup_layout.addWidget(info_label)
        
        backup_btn_layout = QHBoxLayout()
        backup_btn = QPushButton("💾 Create Backup")
        backup_btn.setObjectName("primaryButton")
        backup_btn.clicked.connect(self.create_backup)
        backup_btn_layout.addWidget(backup_btn)
        backup_btn_layout.addStretch()
        backup_layout.addLayout(backup_btn_layout)
        
        layout.addWidget(backup_group)
        
        # Restore section
        restore_group = QGroupBox("Restore from Backup")
        restore_layout = QVBoxLayout(restore_group)
        
        warning_label = QLabel("⚠️ Warning: Restoring will replace all current data!")
        warning_label.setStyleSheet("color: #E74C3C; font-weight: bold;")
        restore_layout.addWidget(warning_label)
        
        restore_btn_layout = QHBoxLayout()
        restore_btn = QPushButton("📁 Restore from File")
        restore_btn.setObjectName("dangerButton")
        restore_btn.clicked.connect(self.restore_backup)
        restore_btn_layout.addWidget(restore_btn)
        restore_btn_layout.addStretch()
        restore_layout.addLayout(restore_btn_layout)
        
        layout.addWidget(restore_group)
        
        # Backup history
        history_label = QLabel("Backup History")
        history_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(history_label)
        
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        
        refresh_btn = QPushButton("🔄 Refresh List")
        refresh_btn.clicked.connect(self.load_backup_history)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        self.load_backup_history()
    
    def create_backup(self):
        reply = QMessageBox.question(
            self, 'Confirm Backup',
            'Create a backup of the database?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, backup_path = db.backup_database()
            
            if success:
                QMessageBox.information(
                    self, "Success",
                    f"Backup created successfully!\n\nLocation: {backup_path}"
                )
                self.load_backup_history()
            else:
                QMessageBox.critical(
                    self, "Error",
                    f"Failed to create backup:\n{backup_path}"
                )
    
    def restore_backup(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Backup File", "",
            "Database Files (*.db);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        reply = QMessageBox.warning(
            self, 'Confirm Restore',
            '⚠️ WARNING: This will replace all current data!\n\n'
            'Are you absolutely sure you want to restore from this backup?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = db.restore_database(file_path)
            
            if success:
                QMessageBox.information(
                    self, "Success",
                    "Database restored successfully!\n\n"
                    "Please restart the application for changes to take effect."
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Failed to restore database from backup."
                )
    
    def load_backup_history(self):
        """Load list of backup files"""
        self.history_list.clear()
        
        import config
        backup_dir = config.BACKUP_DIR
        
        if not os.path.exists(backup_dir):
            return
        
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
        backup_files.sort(reverse=True)  # Most recent first
        
        for backup_file in backup_files:
            file_path = os.path.join(backup_dir, backup_file)
            file_size = os.path.getsize(file_path) / 1024  # KB
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            item_text = f"{backup_file} - {file_size:.2f} KB - {mod_time.strftime('%Y-%m-%d %H:%M:%S')}"
            self.history_list.addItem(item_text)
