"""
Report Builder UI
Customizable report generator
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.report_controller import report_controller
from controllers.department_controller import department_controller
import os

class ReportBuilderPage(QWidget):
    """Page for generating custom reports"""
    
    def __init__(self, user_data=None, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.user_role = user_data.get('role', 'Viewer') if user_data else 'Viewer'
        self.department_id = user_data.get('department_id') if user_data else None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📑 Report Builder")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        layout.addLayout(header_layout)
        
        # Configuration Area
        config_group = QGroupBox("Report Configuration")
        config_layout = QGridLayout(config_group)
        config_layout.setSpacing(15)
        
        # Report Type
        config_layout.addWidget(QLabel("Report Type:"), 0, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Student Performance Report", "Attendance Report"])
        self.type_combo.currentIndexChanged.connect(self.load_preview)
        config_layout.addWidget(self.type_combo, 0, 1)
        
        # Department Filter
        config_layout.addWidget(QLabel("Department:"), 0, 2)
        self.dept_combo = QComboBox()
        
        # Only show "All Departments" for Admin
        if self.user_role not in ['Teacher']:
            self.dept_combo.addItem("All Departments", None)
            
        self.load_departments()
        self.dept_combo.currentIndexChanged.connect(self.load_preview)
        config_layout.addWidget(self.dept_combo, 0, 3)
        
        # Lock for Teacher
        if self.user_role == 'Teacher' and self.department_id:
            self.dept_combo.setEnabled(False)
        
        # Format
        config_layout.addWidget(QLabel("Format:"), 1, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Excel (.xlsx)", "PDF (.pdf)"])
        config_layout.addWidget(self.format_combo, 1, 1)
        
        # Generate Button
        gen_btn = QPushButton("📥 Generate Report")
        gen_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px 15px; font-weight: bold;")
        gen_btn.clicked.connect(self.generate_report)
        config_layout.addWidget(gen_btn, 1, 3)
        
        layout.addWidget(config_group)
        
        # Preview Area
        layout.addWidget(QLabel("Data Preview (First 50 records):"))
        self.preview_table = QTableWidget()
        layout.addWidget(self.preview_table)
        
        # Initial Load
        self.load_preview()
        
    def load_departments(self):
        """Load departments"""
        depts = department_controller.get_all_departments()
        for d in depts:
            # Filter for Teacher
            if self.user_role == 'Teacher' and self.department_id:
                if d['department_id'] == self.department_id:
                    self.dept_combo.addItem(d['department_name'], d['department_id'])
            else:
                self.dept_combo.addItem(d['department_name'], d['department_id'])

    def load_preview(self):
        """Load data preview"""
        report_type = self.type_combo.currentText()
        dept_id = self.dept_combo.currentData()
        
        if report_type == "Student Performance Report":
            headers, data = report_controller.get_student_performance_data(dept_id)
        else:
            headers, data = report_controller.get_attendance_data(dept_id)
            
        self.preview_table.setColumnCount(len(headers))
        self.preview_table.setHorizontalHeaderLabels(headers)
        self.preview_table.setRowCount(min(len(data), 50))
        
        for row, row_data in enumerate(data[:50]):
            for col, val in enumerate(row_data):
                self.preview_table.setItem(row, col, QTableWidgetItem(str(val)))
                
        self.current_headers = headers
        self.current_data = data

    def generate_report(self):
        """Generate and save report"""
        report_type = self.type_combo.currentText()
        fmt = self.format_combo.currentText()
        dept_name = self.dept_combo.currentText()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type.replace(' ', '_')}_{timestamp}"
        
        if "Excel" in fmt:
            filename += ".xlsx"
            success, path = report_controller.generate_excel_report(
                f"{report_type} - {dept_name}",
                self.current_headers,
                self.current_data,
                filename
            )
        else:
            filename += ".pdf"
            html = self.generate_html_content(report_type, dept_name)
            success, path = report_controller.generate_pdf_report(html, filename)
            
        if success:
            QMessageBox.information(self, "Success", f"Report generated successfully:\n{path}")
            os.startfile(path) # Open the file
        else:
            QMessageBox.warning(self, "Error", path)

    def generate_html_content(self, title, subtitle):
        """Generate HTML for PDF report"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                h3 {{ color: #7f8c8d; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <h3>{subtitle}</h3>
            <table>
                <thead>
                    <tr>
        """
        
        for h in self.current_headers:
            html += f"<th>{h}</th>"
            
        html += """
                    </tr>
                </thead>
                <tbody>
        """
        
        for row in self.current_data:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell}</td>"
            html += "</tr>"
            
        html += """
                </tbody>
            </table>
            <p style="text-align: right; margin-top: 20px; color: #95a5a6;">Generated by University Exam System</p>
        </body>
        </html>
        """
        return html

from datetime import datetime
