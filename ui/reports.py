"""
Reports Page
"""
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.result_controller import result_controller
from controllers.department_controller import department_controller
from utils.excel_exporter import excel_exporter


class ReportsPage(QWidget):
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.teacher_department_id = department_id  # For teacher filtering
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Reports & Analytics")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Department:"))
        self.dept_combo = QComboBox()
        
        if self.teacher_department_id:
            # Teacher - only their department
            departments = department_controller.get_all_departments()
            for dept in departments:
                if dept['department_id'] == self.teacher_department_id:
                    self.dept_combo.addItem(dept['department_name'], dept['department_id'])
                    break
            self.dept_combo.setEnabled(False)  # Can't change department
        else:
            # Admin - all departments
            self.dept_combo.addItem("All Departments", None)
            departments = department_controller.get_all_departments()
            for dept in departments:
                self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        filter_layout.addWidget(self.dept_combo)
        
        filter_layout.addWidget(QLabel("Semester:"))
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("All Semesters", None)
        for i in range(1, 9):
            self.semester_combo.addItem(f"Semester {i}", i)
        filter_layout.addWidget(self.semester_combo)
        
        generate_btn = QPushButton("📊 Generate Report")
        generate_btn.setObjectName("primaryButton")
        generate_btn.clicked.connect(self.generate_report)
        filter_layout.addWidget(generate_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Statistics
        stats_group = QGroupBox("Pass/Fail Statistics")
        stats_layout = QFormLayout(stats_group)
        
        self.total_label = QLabel("0")
        stats_layout.addRow("Total Students:", self.total_label)
        
        self.passed_label = QLabel("0")
        stats_layout.addRow("Passed:", self.passed_label)
        
        self.failed_label = QLabel("0")
        stats_layout.addRow("Failed:", self.failed_label)
        
        self.pass_rate_label = QLabel("0%")
        stats_layout.addRow("Pass Rate:", self.pass_rate_label)
        
        layout.addWidget(stats_group)
        
        # Topper list
        topper_label = QLabel("Top 10 Students")
        topper_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(topper_label)
        
        self.topper_table = QTableWidget()
        self.topper_table.setColumnCount(6)
        self.topper_table.setHorizontalHeaderLabels([
            "Rank", "Roll Number", "Name", "CGPA", "Percentage", "Grade"
        ])
        layout.addWidget(self.topper_table)
        
        # Export
        export_layout = QHBoxLayout()
        
        export_excel_btn = QPushButton("📊 Export to Excel")
        export_excel_btn.clicked.connect(self.export_report)
        export_layout.addWidget(export_excel_btn)
        
        export_pdf_btn = QPushButton("📄 Export to PDF")
        export_pdf_btn.clicked.connect(self.export_pdf_report)
        export_layout.addWidget(export_pdf_btn)
        
        export_layout.addStretch()
        layout.addLayout(export_layout)
    
    def generate_report(self):
        dept_id = self.dept_combo.currentData()
        semester = self.semester_combo.currentData()
        
        # Get statistics
        stats = result_controller.get_pass_fail_statistics(dept_id, semester)
        
        self.total_label.setText(str(stats['total']))
        self.passed_label.setText(str(stats['passed']))
        self.failed_label.setText(str(stats['failed']))
        self.pass_rate_label.setText(f"{stats['pass_percentage']}%")
        
        # Get topper list
        if dept_id and semester:
            toppers = result_controller.get_topper_list(dept_id, semester, 10)
            self.display_toppers(toppers)
        else:
            self.topper_table.setRowCount(0)
    
    def display_toppers(self, toppers):
        self.topper_table.setRowCount(len(toppers))
        
        for row, topper in enumerate(toppers):
            self.topper_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.topper_table.setItem(row, 1, QTableWidgetItem(topper['roll_number']))
            self.topper_table.setItem(row, 2, QTableWidgetItem(topper['student_name']))
            self.topper_table.setItem(row, 3, QTableWidgetItem(str(topper['cgpa'])))
            self.topper_table.setItem(row, 4, QTableWidgetItem(f"{topper['percentage']}%"))
            self.topper_table.setItem(row, 5, QTableWidgetItem(topper['overall_grade']))
    
    def export_report(self):
        dept_id = self.dept_combo.currentData()
        semester = self.semester_combo.currentData()
        
        if not dept_id or not semester:
            QMessageBox.warning(self, "Error", "Please select department and semester")
            return
        
        toppers = result_controller.get_topper_list(dept_id, semester, 100)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "report.xlsx", "Excel Files (*.xlsx)"
        )
        
        if file_path:
            success = excel_exporter.export_results_report(toppers, file_path)
            if success:
                QMessageBox.information(self, "Success", f"Report saved to {file_path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export report")
    
    def export_pdf_report(self):
        """Export report to PDF"""
        dept_id = self.dept_combo.currentData()
        semester = self.semester_combo.currentData()
        
        if not dept_id or not semester:
            QMessageBox.warning(self, "Error", "Please select department and semester")
            return
        
        # Show university details dialog
        from ui.university_details_dialog import UniversityDetailsDialog
        dialog = UniversityDetailsDialog(self)
        
        if dialog.exec_() != QDialog.Accepted:
            return  # User cancelled
        
        university_data = dialog.get_university_data()
        
        toppers = result_controller.get_topper_list(dept_id, semester, 100)
        stats = result_controller.get_pass_fail_statistics(dept_id, semester)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", "report.pdf", "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.units import inch
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums import TA_CENTER
                from datetime import datetime
                import config
                
                # Create PDF
                doc = SimpleDocTemplate(file_path, pagesize=A4,
                                       rightMargin=0.75*inch, leftMargin=0.75*inch,
                                       topMargin=0.75*inch, bottomMargin=0.75*inch)
                
                elements = []
                styles = getSampleStyleSheet()
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=20,
                    textColor=colors.HexColor('#2C3E50'),
                    spaceAfter=12,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold'
                )
                
                # Use custom university name
                title = Paragraph(f"{university_data['name']}<br/>Results Report", title_style)
                elements.append(title)
                
                # Add university contact info
                contact_parts = []
                if university_data.get('address'):
                    contact_parts.append(university_data['address'])
                if university_data.get('phone'):
                    contact_parts.append(f"Phone: {university_data['phone']}")
                if university_data.get('email'):
                    contact_parts.append(f"Email: {university_data['email']}")
                
                if contact_parts:
                    contact_style = ParagraphStyle(
                        'Contact',
                        parent=styles['Normal'],
                        fontSize=9,
                        textColor=colors.HexColor('#7F8C8D'),
                        alignment=TA_CENTER,
                        spaceAfter=12
                    )
                    contact_text = " | ".join(contact_parts)
                    contact = Paragraph(contact_text, contact_style)
                    elements.append(contact)
                
                elements.append(Spacer(1, 0.3*inch))
                
                # Statistics
                stats_data = [
                    ['Total Students', str(stats['total'])],
                    ['Passed', str(stats['passed'])],
                    ['Failed', str(stats['failed'])],
                    ['Pass Rate', f"{stats['pass_percentage']}%"]
                ]
                
                stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                
                elements.append(stats_table)
                elements.append(Spacer(1, 0.4*inch))
                
                # Topper list
                subtitle = Paragraph("Top Students", styles['Heading2'])
                elements.append(subtitle)
                elements.append(Spacer(1, 0.2*inch))
                
                topper_data = [['Rank', 'Roll No', 'Name', 'CGPA', 'Percentage', 'Grade']]
                
                for topper in toppers[:20]:  # Top 20
                    topper_data.append([
                        str(topper.get('rank', '')),
                        topper['roll_number'],
                        topper['student_name'],
                        str(topper['cgpa']),
                        f"{topper['percentage']}%",
                        topper['overall_grade']
                    ])
                
                topper_table = Table(topper_data, colWidths=[0.6*inch, 1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 0.8*inch])
                topper_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                    ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                
                elements.append(topper_table)
                
                # Footer
                elements.append(Spacer(1, 0.3*inch))
                footer_text = f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
                footer = Paragraph(footer_text, styles['Normal'])
                elements.append(footer)
                
                doc.build(elements)
                
                QMessageBox.information(self, "Success", f"PDF report saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export PDF: {str(e)}")
