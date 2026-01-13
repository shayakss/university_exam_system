"""
My Results Page - Student's own results only
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.result_controller import result_controller


class MyResultsPage(QWidget):
    """Display student's own results"""
    
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_id = student_id
        self.init_ui()
        self.load_results()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📋 My Results")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Course Code", "Course Name", "Marks Obtained", "Max Marks", "Grade", "Status"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Summary
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        
        export_transcript_btn = QPushButton("📜 Export Transcript")
        export_transcript_btn.setObjectName("primaryButton")
        export_transcript_btn.setToolTip("Export complete academic transcript as PDF")
        export_transcript_btn.clicked.connect(self.export_transcript)
        btn_layout.addWidget(export_transcript_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_results)
        btn_layout.addWidget(refresh_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
    
    def load_results(self):
        """Load student's results"""
        if not self.student_id:
            QMessageBox.warning(self, "Error", "No student ID found")
            return
        
        try:
            results = result_controller.get_student_results(self.student_id)
            
            # Clear table
            self.table.clearContents()
            self.table.setRowCount(0)
            self.table.setRowCount(len(results))
            
            total_marks = 0
            max_marks = 0
            
            for row, result in enumerate(results):
                self.table.setItem(row, 0, QTableWidgetItem(result.get('course_code', '')))
                self.table.setItem(row, 1, QTableWidgetItem(result.get('course_name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(str(result.get('marks_obtained', 0))))
                self.table.setItem(row, 3, QTableWidgetItem(str(result.get('max_marks', 100))))
                self.table.setItem(row, 4, QTableWidgetItem(result.get('grade', 'N/A')))
                self.table.setItem(row, 5, QTableWidgetItem(result.get('status', 'N/A')))
                
                total_marks += result.get('marks_obtained', 0)
                max_marks += result.get('max_marks', 100)
            
            self.table.resizeColumnsToContents()
            
            # Calculate percentage
            if max_marks > 0:
                percentage = (total_marks / max_marks) * 100
                self.summary_label.setText(
                    f"<b>Total:</b> {total_marks}/{max_marks} | <b>Percentage:</b> {percentage:.2f}%"
                )
            else:
                self.summary_label.setText("No results available")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load results: {str(e)}")
    
    def export_transcript(self):
        """Export student's complete academic transcript"""
        if not self.student_id:
            QMessageBox.warning(self, "Error", "No student ID found")
            return
        
        try:
            # Get student info for the dialog
            from controllers.student_controller import student_controller
            students = student_controller.get_all_students()
            student = next((s for s in students if s['student_id'] == self.student_id), None)
            
            if not student:
                QMessageBox.warning(self, "Error", "Student information not found")
                return
            
            student_name = student.get('name', 'Student')
            
            # Open transcript export dialog
            from ui.transcript_export import TranscriptExportDialog
            dialog = TranscriptExportDialog(self.student_id, student_name, self)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export transcript: {str(e)}")
            print(f"Error in export_transcript: {e}")
            import traceback
            traceback.print_exc()
