"""
Result Generation Page
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QComboBox, QTableWidget, QTableWidgetItem, QMessageBox,
                             QFileDialog, QDialog, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.result_controller import result_controller
from controllers.student_controller import student_controller
from utils.pdf_generator import pdf_generator
from utils.excel_exporter import excel_exporter


class ResultGenerationPage(QWidget):
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.teacher_department_id = department_id  # For teacher filtering
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Result Generation")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Selection
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Select Student:"))
        self.student_combo = QComboBox()
        self.load_students()  # Load students initially
        select_layout.addWidget(self.student_combo)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self.load_students)
        select_layout.addWidget(refresh_btn)
        
        generate_btn = QPushButton("📊 Generate Result")
        generate_btn.setObjectName("primaryButton")
        generate_btn.clicked.connect(self.generate_result)
        select_layout.addWidget(generate_btn)
        select_layout.addStretch()
        
        layout.addLayout(select_layout)
        
        # Result display
        self.result_group = QGroupBox("Result Details")
        result_layout = QFormLayout(self.result_group)
        
        self.student_name_label = QLabel("--")
        result_layout.addRow("Student:", self.student_name_label)
        
        self.roll_label = QLabel("--")
        result_layout.addRow("Roll Number:", self.roll_label)
        
        self.semester_label = QLabel("--")
        result_layout.addRow("Semester:", self.semester_label)
        
        self.total_marks_label = QLabel("--")
        result_layout.addRow("Total Marks:", self.total_marks_label)
        
        self.obtained_marks_label = QLabel("--")
        result_layout.addRow("Marks Obtained:", self.obtained_marks_label)
        
        self.percentage_label = QLabel("--")
        result_layout.addRow("Percentage:", self.percentage_label)
        
        self.sgpa_label = QLabel("--")
        result_layout.addRow("SGPA:", self.sgpa_label)
        
        self.cgpa_label = QLabel("--")
        result_layout.addRow("CGPA:", self.cgpa_label)
        
        self.grade_label = QLabel("--")
        result_layout.addRow("Overall Grade:", self.grade_label)
        
        self.status_label = QLabel("--")
        result_layout.addRow("Status:", self.status_label)
        
        layout.addWidget(self.result_group)
        
        # Marks table
        self.marks_table = QTableWidget()
        self.marks_table.setColumnCount(6)
        self.marks_table.setHorizontalHeaderLabels([
            "Course Code", "Course Name", "Max Marks", "Marks Obtained", "Grade", "Status"
        ])
        layout.addWidget(self.marks_table)
        
        # Actions
        action_layout = QHBoxLayout()
        
        pdf_btn = QPushButton("📄 Export to PDF")
        pdf_btn.clicked.connect(self.export_pdf)
        action_layout.addWidget(pdf_btn)
        
        transcript_btn = QPushButton("📜 Export Transcript")
        transcript_btn.setToolTip("Export complete academic transcript")
        transcript_btn.clicked.connect(self.export_transcript)
        action_layout.addWidget(transcript_btn)
        
        excel_btn = QPushButton("📊 Export to Excel")
        excel_btn.clicked.connect(self.export_excel)
        action_layout.addWidget(excel_btn)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        self.current_result = None
    
    def load_students(self):
        """Load/Reload students into dropdown"""
        self.student_combo.clear()
        if self.teacher_department_id:
            # Teacher - only their department students
            students = student_controller.get_students_by_department(self.teacher_department_id)
        else:
            # Admin - all students
            students = student_controller.get_all_students()
        for student in students:
            self.student_combo.addItem(
                f"{student['roll_number']} - {student['name']} (Sem {student['semester']})",
                (student['student_id'], student['semester'])
            )
    
    def generate_result(self):
        data = self.student_combo.currentData()
        if not data:
            return
        
        student_id, semester = data
        success, result_data, msg = result_controller.generate_result(student_id, semester)
        
        if success:
            self.current_result = result_data
            self.display_result(result_data)
        else:
            QMessageBox.warning(self, "Error", msg)
    
    def display_result(self, result_data):
        student = result_data['student']
        
        self.student_name_label.setText(student['name'])
        self.roll_label.setText(student['roll_number'])
        self.semester_label.setText(str(result_data['semester']))
        self.total_marks_label.setText(str(result_data['total_marks']))
        self.obtained_marks_label.setText(str(result_data['marks_obtained']))
        self.percentage_label.setText(f"{result_data['percentage']}%")
        self.sgpa_label.setText(str(result_data['sgpa']))
        self.cgpa_label.setText(str(result_data['cgpa']))
        self.grade_label.setText(result_data['overall_grade'])
        
        status = result_data['status']
        self.status_label.setText(status)
        self.status_label.setStyleSheet(
            f"color: {'green' if status == 'Pass' else 'red'}; font-weight: bold;"
        )
        
        # Display marks
        marks = result_data['marks']
        self.marks_table.setRowCount(len(marks))
        
        for row, mark in enumerate(marks):
            self.marks_table.setItem(row, 0, QTableWidgetItem(mark['course_code']))
            self.marks_table.setItem(row, 1, QTableWidgetItem(mark['course_name']))
            self.marks_table.setItem(row, 2, QTableWidgetItem(str(mark['max_marks'])))
            self.marks_table.setItem(row, 3, QTableWidgetItem(str(mark['marks_obtained'])))
            self.marks_table.setItem(row, 4, QTableWidgetItem(mark['grade']))
            self.marks_table.setItem(row, 5, QTableWidgetItem(mark['status']))
    
    def export_pdf(self):
        """Export result to PDF"""
        if not self.current_result:
            QMessageBox.warning(self, "Error", "Please calculate result first")
            return
        
        # Show university details dialog
        from ui.university_details_dialog import UniversityDetailsDialog
        dialog = UniversityDetailsDialog(self)
        
        if dialog.exec_() != QDialog.Accepted:
            return  # User cancelled
        
        university_data = dialog.get_university_data()
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Marksheet", f"marksheet_{self.current_result['student']['roll_number']}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            success = pdf_generator.generate_marksheet(self.current_result, file_path, university_data)
            if success:
                QMessageBox.information(self, "Success", f"Marksheet saved to {file_path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to generate PDF")
    
    def export_transcript(self):
        """Export complete academic transcript"""
        try:
            data = self.student_combo.currentData()
            if not data:
                QMessageBox.warning(self, "No Selection", "Please select a student first")
                return
            
            # Handle tuple data (student_id, semester) or single student_id
            if isinstance(data, tuple):
                student_id = data[0]
            else:
                student_id = data
            
            # Safely get student name from combo box text
            combo_text = self.student_combo.currentText()
            if " - " in combo_text:
                parts = combo_text.split(" - ", 1)  # Split only on first occurrence
                student_name = parts[1].split(" (")[0] if len(parts) > 1 else "Student"
            else:
                student_name = "Student"
            
            # Open transcript export dialog
            from ui.transcript_export import TranscriptExportDialog
            dialog = TranscriptExportDialog(student_id, student_name, self)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export transcript: {str(e)}")
            print(f"Error in export_transcript: {e}")
            import traceback
            traceback.print_exc()
    
    def export_excel(self):
        """Export result to Excel"""
        if not self.current_result:
            QMessageBox.warning(self, "Error", "Please calculate result first")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel", f"marksheet_{self.current_result['student']['roll_number']}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            success = excel_exporter.export_detailed_marksheet(self.current_result, file_path)
            if success:
                QMessageBox.information(self, "Success", f"Excel saved to {file_path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to generate Excel")
