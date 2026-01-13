"""
Enhanced Dashboard with Visual Charts and Analytics
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from controllers.student_controller import student_controller
from controllers.department_controller import department_controller
from controllers.result_controller import result_controller
from utils.chart_generator import ChartWidget, chart_generator


class DashboardEnhanced(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        # Delay loading to ensure widget has valid dimensions
        QTimer.singleShot(1500, self.load_dashboard_data)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Dashboard & Analytics")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        refresh_btn = QPushButton("🔄 Refresh Data")
        refresh_btn.clicked.connect(self.load_dashboard_data)
        refresh_layout.addWidget(refresh_btn)
        layout.addLayout(refresh_layout)
        
        # Statistics cards
        stats_layout = QHBoxLayout()
        
        self.total_students_card = self.create_stat_card("Total Students", "0", "#3498DB")
        self.total_depts_card = self.create_stat_card("Departments", "0", "#9B59B6")
        self.pass_rate_card = self.create_stat_card("Pass Rate", "0%", "#27AE60")
        self.avg_cgpa_card = self.create_stat_card("Avg CGPA", "0.00", "#F39C12")
        
        stats_layout.addWidget(self.total_students_card)
        stats_layout.addWidget(self.total_depts_card)
        stats_layout.addWidget(self.pass_rate_card)
        stats_layout.addWidget(self.avg_cgpa_card)
        
        layout.addLayout(stats_layout)
        
        # Chart tabs
        self.chart_tabs = QTabWidget()
        
        # Tab 1: Pass/Fail Analysis
        self.pass_fail_chart = ChartWidget()
        self.chart_tabs.addTab(self.pass_fail_chart, "📊 Pass/Fail Analysis")
        
        # Tab 2: Department Performance
        self.dept_chart = ChartWidget()
        self.chart_tabs.addTab(self.dept_chart, "📈 Department Performance")
        
        # Tab 3: Grade Distribution
        self.grade_chart = ChartWidget()
        self.chart_tabs.addTab(self.grade_chart, "🎯 Grade Distribution")
        
        # Tab 4: Top Students
        self.top_students_chart = ChartWidget()
        self.chart_tabs.addTab(self.top_students_chart, "🏆 Top 10 Students")
        
        layout.addWidget(self.chart_tabs)
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card widget"""
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                background-color: {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 12px;")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def load_dashboard_data(self):
        """Load all dashboard data and charts"""
        # Update statistics cards
        self.update_statistics()
        
        # Update charts
        self.update_pass_fail_chart()
        self.update_department_chart()
        self.update_grade_distribution_chart()
        self.update_top_students_chart()
    
    def update_statistics(self):
        """Update statistics cards"""
        # Total students
        students = student_controller.get_all_students()
        self.total_students_card.value_label.setText(str(len(students)))
        
        # Total departments
        departments = department_controller.get_all_departments()
        self.total_depts_card.value_label.setText(str(len(departments)))
        
        # Calculate overall pass rate and average CGPA
        if departments:
            total_passed = 0
            total_students = 0
            total_cgpa = 0
            cgpa_count = 0
            
            for dept in departments:
                for semester in range(1, 9):
                    stats = result_controller.get_pass_fail_statistics(
                        dept['department_id'], semester
                    )
                    if stats['total'] > 0:
                        total_passed += stats['passed']
                        total_students += stats['total']
                    
                    # Get toppers for CGPA calculation
                    toppers = result_controller.get_topper_list(
                        dept['department_id'], semester, 100
                    )
                    for topper in toppers:
                        if topper.get('cgpa'):
                            total_cgpa += topper['cgpa']
                            cgpa_count += 1
            
            # Update pass rate
            if total_students > 0:
                pass_rate = (total_passed / total_students) * 100
                self.pass_rate_card.value_label.setText(f"{pass_rate:.1f}%")
            else:
                self.pass_rate_card.value_label.setText("N/A")
            
            # Update average CGPA
            if cgpa_count > 0:
                avg_cgpa = total_cgpa / cgpa_count
                self.avg_cgpa_card.value_label.setText(f"{avg_cgpa:.2f}")
            else:
                self.avg_cgpa_card.value_label.setText("N/A")
        else:
            self.pass_rate_card.value_label.setText("N/A")
            self.avg_cgpa_card.value_label.setText("N/A")
    
    def update_pass_fail_chart(self):
        """Update pass/fail pie chart"""
        self.pass_fail_chart.clear()
        
        departments = department_controller.get_all_departments()
        total_passed = 0
        total_failed = 0
        
        for dept in departments:
            for semester in range(1, 9):
                stats = result_controller.get_pass_fail_statistics(
                    dept['department_id'], semester
                )
                total_passed += stats['passed']
                total_failed += stats['failed']
        
        if total_passed > 0 or total_failed > 0:
            data = [total_passed, total_failed]
            labels = ['Passed', 'Failed']
            colors = ['#27AE60', '#E74C3C']
            
            chart_generator.create_pie_chart(
                self.pass_fail_chart.figure,
                data, labels,
                "Overall Pass/Fail Distribution",
                colors
            )
        else:
            ax = self.pass_fail_chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=14)
        
        self.pass_fail_chart.draw()
    
    def update_department_chart(self):
        """Update department performance bar chart"""
        self.dept_chart.clear()
        
        departments = department_controller.get_all_departments()
        dept_names = []
        pass_rates = []
        
        for dept in departments:
            total_passed = 0
            total_students = 0
            
            for semester in range(1, 9):
                stats = result_controller.get_pass_fail_statistics(
                    dept['department_id'], semester
                )
                total_passed += stats['passed']
                total_students += stats['total']
            
            if total_students > 0:
                dept_names.append(dept['department_code'])
                pass_rate = (total_passed / total_students) * 100
                pass_rates.append(pass_rate)
        
        if dept_names:
            chart_generator.create_bar_chart(
                self.dept_chart.figure,
                dept_names, pass_rates,
                "Department-wise Pass Rate",
                "Department", "Pass Rate (%)",
                '#3498DB'
            )
        else:
            ax = self.dept_chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=14)
        
        self.dept_chart.draw()
    
    def update_grade_distribution_chart(self):
        """Update grade distribution pie chart"""
        self.grade_chart.clear()
        
        grade_counts = {'A+': 0, 'A': 0, 'B+': 0, 'B': 0, 'C+': 0, 'C': 0, 'F': 0}
        
        departments = department_controller.get_all_departments()
        for dept in departments:
            for semester in range(1, 9):
                toppers = result_controller.get_topper_list(
                    dept['department_id'], semester, 1000
                )
                for student in toppers:
                    grade = student.get('overall_grade', 'F')
                    if grade in grade_counts:
                        grade_counts[grade] += 1
        
        # Filter out grades with 0 count
        labels = [grade for grade, count in grade_counts.items() if count > 0]
        data = [count for count in grade_counts.values() if count > 0]
        
        if data:
            colors = ['#27AE60', '#2ECC71', '#3498DB', '#5DADE2', '#F39C12', '#E67E22', '#E74C3C']
            chart_generator.create_pie_chart(
                self.grade_chart.figure,
                data, labels,
                "Grade Distribution",
                colors[:len(labels)]
            )
        else:
            ax = self.grade_chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=14)
        
        self.grade_chart.draw()
    
    def update_top_students_chart(self):
        """Update top 10 students bar chart"""
        self.top_students_chart.clear()
        
        # Get all students with results
        all_toppers = []
        departments = department_controller.get_all_departments()
        
        for dept in departments:
            for semester in range(1, 9):
                toppers = result_controller.get_topper_list(
                    dept['department_id'], semester, 100
                )
                all_toppers.extend(toppers)
        
        # Sort by CGPA and get top 10
        all_toppers.sort(key=lambda x: x.get('cgpa', 0), reverse=True)
        top_10 = all_toppers[:10]
        
        if top_10:
            names = [f"{s['roll_number']}" for s in top_10]
            cgpas = [s['cgpa'] for s in top_10]
            
            chart_generator.create_horizontal_bar_chart(
                self.top_students_chart.figure,
                names, cgpas,
                "Top 10 Students by CGPA",
                "CGPA", "Roll Number"
            )
        else:
            ax = self.top_students_chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=14)
        
        self.top_students_chart.draw()
