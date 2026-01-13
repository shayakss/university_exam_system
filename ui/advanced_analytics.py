"""
Advanced Analytics UI
Interactive charts and reports using Matplotlib
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from controllers.analytics_controller import analytics_controller
from controllers.department_controller import department_controller

class AdvancedAnalyticsPage(QWidget):
    """Page for advanced analytics and visualization"""
    
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
        title = QLabel("\U0001F4CA Advanced Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        
        # Department Filter
        self.dept_combo = QComboBox()
        
        # Only show "All Departments" for Admin
        if self.user_role not in ['Teacher']:
            self.dept_combo.addItem("All Departments", None)
            
        self.load_departments()
        self.dept_combo.currentIndexChanged.connect(self.refresh_charts)
        header_layout.addWidget(QLabel("Filter by Department:"))
        header_layout.addWidget(self.dept_combo)
        
        # Lock for Teacher
        if self.user_role == 'Teacher' and self.department_id:
            self.dept_combo.setEnabled(False)
        
        refresh_btn = QPushButton("\U0001F504 Refresh")
        refresh_btn.clicked.connect(self.refresh_charts)
        header_layout.addWidget(refresh_btn)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_overview_tab(), "Overview")
        self.tabs.addTab(self.create_performance_tab(), "Performance Analysis")
        self.tabs.addTab(self.create_attendance_tab(), "Attendance Stats")
        layout.addWidget(self.tabs)
        
        # Initial Load
        self.refresh_charts()
        
    def load_departments(self):
        """Load departments into combo box"""
        depts = department_controller.get_all_departments()
        for d in depts:
            # Filter for Teacher
            if self.user_role == 'Teacher' and self.department_id:
                if d['department_id'] == self.department_id:
                    self.dept_combo.addItem(d['department_name'], d['department_id'])
            else:
                self.dept_combo.addItem(d['department_name'], d['department_id'])

    def create_overview_tab(self):
        """Create overview tab with summary and basic charts"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary Cards
        cards_layout = QHBoxLayout()
        self.total_students_card = self.create_stat_card("Total Students", "0", "#3498db")
        self.avg_cgpa_card = self.create_stat_card("Avg CGPA", "0.00", "#2ecc71")
        self.pass_rate_card = self.create_stat_card("Pass Rate", "0%", "#9b59b6")
        
        cards_layout.addWidget(self.total_students_card)
        cards_layout.addWidget(self.avg_cgpa_card)
        cards_layout.addWidget(self.pass_rate_card)
        layout.addLayout(cards_layout)
        
        # Charts Row
        charts_layout = QHBoxLayout()
        
        # Gender Distribution (Pie)
        self.gender_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.gender_canvas)
        
        # Pass/Fail (Pie)
        self.pass_fail_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.pass_fail_canvas)
        
        layout.addLayout(charts_layout)
        
        return widget

    def create_performance_tab(self):
        """Create performance analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Grade Distribution (Bar)
        self.grade_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.grade_canvas)
        
        # Performance Trends (Line)
        self.trend_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.trend_canvas)
        
        return widget

    def create_attendance_tab(self):
        """Create attendance statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Attendance by Dept (Bar)
        self.attendance_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.attendance_canvas)
        
        return widget

    def create_stat_card(self, title, value, color):
        """Create a simple stat card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 5px solid {color};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        l = QVBoxLayout(card)
        t = QLabel(title)
        t.setStyleSheet("color: #7f8c8d;")
        v = QLabel(value)
        v.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        l.addWidget(t)
        l.addWidget(v)
        card.value_label = v
        return card

    def refresh_charts(self):
        """Refresh all charts with current filter"""
        dept_id = self.dept_combo.currentData()
        
        # Update Summary Cards
        summary = analytics_controller.get_dashboard_summary()
        if summary:
            self.total_students_card.value_label.setText(str(summary.get('students', {}).get('total', 0)))
            avg_cgpa = summary.get('performance', {}).get('avg_cgpa')
            self.avg_cgpa_card.value_label.setText(f"{avg_cgpa:.2f}" if avg_cgpa else "0.00")
            
            pf_rates = analytics_controller.get_pass_fail_rates(dept_id)
            pass_rate = pf_rates.get('pass_rate', 0) if pf_rates else 0
            self.pass_rate_card.value_label.setText(f"{pass_rate}%")

        # 1. Gender Distribution
        dist = analytics_controller.get_student_distribution_by_department() or []
        male = sum(d.get('male_count', 0) or 0 for d in dist)
        female = sum(d.get('female_count', 0) or 0 for d in dist)
        
        self.gender_canvas.axes.clear()
        if male + female > 0:
            self.gender_canvas.axes.pie([male, female], labels=['Male', 'Female'], autopct='%1.1f%%', colors=['#3498db', '#e91e63'])
        else:
            self.gender_canvas.axes.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.gender_canvas.axes.set_title("Gender Distribution")
        self.gender_canvas.draw()
        
        # 2. Pass/Fail Rates
        pf = analytics_controller.get_pass_fail_rates(dept_id) or {}
        passed = pf.get('passed', 0) or 0
        failed = pf.get('failed', 0) or 0
        
        self.pass_fail_canvas.axes.clear()
        if passed + failed > 0:
            self.pass_fail_canvas.axes.pie([passed, failed], labels=['Pass', 'Fail'], autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
        else:
            self.pass_fail_canvas.axes.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.pass_fail_canvas.axes.set_title("Pass/Fail Ratio")
        self.pass_fail_canvas.draw()
        
        # 3. Grade Distribution
        grades = analytics_controller.get_grade_distribution(dept_id) or []
        labels = [g['grade'] for g in grades] if grades else []
        counts = [g['count'] for g in grades] if grades else []
        
        self.grade_canvas.axes.clear()
        if labels and counts:
            self.grade_canvas.axes.bar(labels, counts, color='#9b59b6')
        else:
            self.grade_canvas.axes.text(0.5, 0.5, "No Data", ha='center', va='center', transform=self.grade_canvas.axes.transAxes)
        self.grade_canvas.axes.set_title("Grade Distribution")
        self.grade_canvas.axes.set_xlabel("Grade")
        self.grade_canvas.axes.set_ylabel("Count")
        self.grade_canvas.draw()
        
        # 4. Trends
        trends = analytics_controller.get_performance_trends(dept_id) or []
        
        self.trend_canvas.axes.clear()
        if trends:
            months = [t['month'] for t in trends]
            cgpas = [t['avg_cgpa'] or 0 for t in trends]
            self.trend_canvas.axes.plot(months, cgpas, marker='o', color='#e67e22')
        else:
            self.trend_canvas.axes.text(0.5, 0.5, "No Data", ha='center', va='center', transform=self.trend_canvas.axes.transAxes)
        self.trend_canvas.axes.set_title("Average CGPA Trend")
        self.trend_canvas.axes.set_xlabel("Month")
        self.trend_canvas.axes.set_ylabel("CGPA")
        self.trend_canvas.axes.grid(True)
        self.trend_canvas.draw()
        
        # 5. Attendance
        att = analytics_controller.get_attendance_statistics(dept_id) or []
        
        self.attendance_canvas.axes.clear()
        if att:
            depts = [a['department_name'] for a in att]
            rates = [a.get('avg_attendance_rate', 0) or 0 for a in att]
            self.attendance_canvas.axes.barh(depts, rates, color='#1abc9c')
        else:
            self.attendance_canvas.axes.text(0.5, 0.5, "No Data", ha='center', va='center', transform=self.attendance_canvas.axes.transAxes)
        self.attendance_canvas.axes.set_title("Average Attendance by Department")
        self.attendance_canvas.axes.set_xlabel("Attendance %")
        self.attendance_canvas.draw()

class MplCanvas(FigureCanvas):
    """Matplotlib Canvas for PyQt"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
