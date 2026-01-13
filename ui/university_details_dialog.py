"""
University Details Dialog - Collect university information for exports
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config


class UniversityDetailsDialog(QDialog):
    """Dialog to collect university details for PDF/Excel exports"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.university_data = {}
        self.init_ui()
        self.load_default_values()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("University Details")
        self.setFixedSize(500, 400)
        self.setStyleSheet("QDialog { background-color: white; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Enter University Details")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(title)
        
        subtitle = QLabel("This information will be included in the exported document")
        subtitle.setStyleSheet("color: #7F8C8D; font-size: 10px;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # University Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., ABC University")
        self.name_input.setFixedHeight(35)
        form_layout.addRow("University Name:*", self.name_input)
        
        # Address
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("e.g., 123 University Street, City")
        self.address_input.setFixedHeight(35)
        form_layout.addRow("Address:", self.address_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g., +1 (555) 123-4567")
        self.phone_input.setFixedHeight(35)
        form_layout.addRow("Phone:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g., info@university.edu")
        self.email_input.setFixedHeight(35)
        form_layout.addRow("Email:", self.email_input)
        
        # Website
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("e.g., www.university.edu")
        self.website_input.setFixedHeight(35)
        form_layout.addRow("Website:", self.website_input)
        
        layout.addLayout(form_layout)
        
        # Note
        note = QLabel("* Required field")
        note.setStyleSheet("color: #E74C3C; font-size: 9px; font-style: italic;")
        layout.addWidget(note)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(100, 35)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        export_btn = QPushButton("Export")
        export_btn.setObjectName("primaryButton")
        export_btn.setFixedSize(100, 35)
        export_btn.clicked.connect(self.accept_data)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
    
    def load_default_values(self):
        """Load default values from config"""
        self.name_input.setText(config.UNIVERSITY_NAME)
        self.address_input.setText(getattr(config, 'UNIVERSITY_ADDRESS', ''))
        self.phone_input.setText(getattr(config, 'UNIVERSITY_PHONE', ''))
        self.email_input.setText(getattr(config, 'UNIVERSITY_EMAIL', ''))
        self.website_input.setText(getattr(config, 'UNIVERSITY_WEBSITE', ''))
    
    def accept_data(self):
        """Validate and accept data"""
        university_name = self.name_input.text().strip()
        
        if not university_name:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Required Field", "University Name is required!")
            self.name_input.setFocus()
            return
        
        # Store data
        self.university_data = {
            'name': university_name,
            'address': self.address_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip(),
            'website': self.website_input.text().strip()
        }
        
        self.accept()
    
    def get_university_data(self):
        """Get the collected university data"""
        return self.university_data
