"""
Transcript Export Dialog - UI for exporting student transcripts
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.transcript_controller import transcript_controller
import os


class TranscriptExportDialog(QDialog):
    """Dialog for exporting student transcript"""
    
    def __init__(self, student_id, student_name, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.student_name = student_name
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Export Transcript")
        self.setFixedSize(500, 250)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel(f"📄 Export Transcript for {self.student_name}")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Info
        info_label = QLabel("Generate a professional academic transcript PDF with all semester marks and grades.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666;")
        layout.addWidget(info_label)
        
        # File selection
        file_group = QGroupBox("Output Location")
        file_layout = QHBoxLayout()
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Select where to save the transcript...")
        self.file_path_input.setReadOnly(True)
        file_layout.addWidget(self.file_path_input)
        
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # University details (optional)
        uni_group = QGroupBox("University Details (Optional)")
        uni_layout = QFormLayout()
        
        self.uni_name_input = QLineEdit()
        self.uni_name_input.setPlaceholderText("e.g., University of Balochistan, Quetta")
        uni_layout.addRow("University Name:", self.uni_name_input)
        
        self.sub_campus_input = QLineEdit()
        self.sub_campus_input.setPlaceholderText("e.g., Kharan")
        uni_layout.addRow("Sub-Campus:", self.sub_campus_input)
        
        uni_group.setLayout(uni_layout)
        layout.addWidget(uni_group)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        export_btn = QPushButton("📥 Export Transcript")
        export_btn.setObjectName("primaryButton")
        export_btn.setStyleSheet("background-color: #2563eb; color: white; padding: 10px 20px; font-weight: bold;")
        export_btn.clicked.connect(self.export_transcript)
        btn_layout.addWidget(export_btn)
        
        layout.addLayout(btn_layout)
    
    def browse_file(self):
        """Browse for save location"""
        default_filename = f"Transcript_{self.student_name.replace(' ', '_')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Transcript As",
            default_filename,
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'
            self.file_path_input.setText(file_path)
    
    def export_transcript(self):
        """Export the transcript"""
        file_path = self.file_path_input.text().strip()
        
        if not file_path:
            QMessageBox.warning(self, "No File Selected", "Please select where to save the transcript.")
            return
        
        # Prepare university data
        university_data = {}
        if self.uni_name_input.text().strip():
            university_data['name'] = self.uni_name_input.text().strip()
        if self.sub_campus_input.text().strip():
            university_data['sub_campus'] = self.sub_campus_input.text().strip()
        
        # Generate transcript
        try:
            success, message = transcript_controller.generate_transcript_pdf(
                self.student_id,
                file_path,
                university_data if university_data else None
            )
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export transcript: {str(e)}")
