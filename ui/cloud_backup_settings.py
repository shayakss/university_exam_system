"""
Cloud Backup Settings UI
Handles configuration for cloud backups
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.cloud_backup_controller import cloud_backup_controller

class CloudBackupSettingsPage(QWidget):
    """Page for configuring cloud backups"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("☁️ Cloud Backup Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        layout.addLayout(header_layout)
        
        # Provider Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_provider_tab("Google Drive"), "Google Drive")
        self.tabs.addTab(self.create_provider_tab("Dropbox"), "Dropbox")
        layout.addWidget(self.tabs)
        
        # Manual Backup Section
        backup_group = QGroupBox("Manual Backup")
        backup_layout = QHBoxLayout(backup_group)
        
        backup_btn = QPushButton("🚀 Backup Now")
        backup_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px 20px; font-weight: bold;")
        backup_btn.clicked.connect(self.trigger_backup)
        backup_layout.addWidget(backup_btn)
        
        self.status_label = QLabel("Ready")
        backup_layout.addWidget(self.status_label)
        
        layout.addWidget(backup_group)
        layout.addStretch()
        
    def create_provider_tab(self, provider_name):
        """Create configuration tab for a provider"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Access Token
        token_edit = QLineEdit()
        token_edit.setPlaceholderText(f"Enter {provider_name} Access Token")
        token_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Access Token:", token_edit)
        
        # Folder Path
        folder_edit = QLineEdit()
        folder_edit.setPlaceholderText("/backups/university_exam_system")
        form_layout.addRow("Remote Folder:", folder_edit)
        
        # Auto Backup
        auto_chk = QCheckBox("Enable Automatic Backup")
        form_layout.addRow("", auto_chk)
        
        # Frequency
        freq_spin = QSpinBox()
        freq_spin.setRange(1, 365)
        freq_spin.setValue(7)
        freq_spin.setSuffix(" days")
        form_layout.addRow("Frequency:", freq_spin)
        
        layout.addLayout(form_layout)
        
        # Save Button
        save_btn = QPushButton("Save Configuration")
        save_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        save_btn.clicked.connect(lambda: self.save_config(provider_name, token_edit, folder_edit, auto_chk, freq_spin))
        layout.addWidget(save_btn)
        
        # Load existing config
        self.load_config(provider_name, token_edit, folder_edit, auto_chk, freq_spin)
        
        return widget

    def load_config(self, provider, token_edit, folder_edit, auto_chk, freq_spin):
        """Load existing configuration"""
        configs = cloud_backup_controller.get_backup_config(provider)
        if configs:
            config = configs[0]
            token_edit.setText(config['access_token'])
            folder_edit.setText(config['folder_path'])
            auto_chk.setChecked(bool(config['auto_backup_enabled']))
            freq_spin.setValue(config['backup_frequency_days'])

    def save_config(self, provider, token_edit, folder_edit, auto_chk, freq_spin):
        """Save configuration"""
        success, msg = cloud_backup_controller.save_backup_config(
            provider,
            access_token=token_edit.text(),
            folder_path=folder_edit.text(),
            auto_backup_enabled=auto_chk.isChecked(),
            backup_frequency_days=freq_spin.value()
        )
        
        if success:
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.warning(self, "Error", msg)

    def trigger_backup(self):
        """Trigger manual backup"""
        provider = self.tabs.tabText(self.tabs.currentIndex())
        self.status_label.setText(f"Backing up to {provider}...")
        QApplication.processEvents()
        
        success, msg = cloud_backup_controller.backup_to_cloud(provider)
        
        if success:
            self.status_label.setText("Backup completed successfully!")
            QMessageBox.information(self, "Success", msg)
        else:
            self.status_label.setText("Backup failed.")
            QMessageBox.warning(self, "Error", msg)
