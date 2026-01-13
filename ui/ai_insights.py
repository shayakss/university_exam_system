"""
AI Performance Insights UI
Shows at-risk students and intervention recommendations
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.ai_insights_controller import ai_insights_controller
from controllers.department_controller import department_controller

class AIInsightsPage(QWidget):
    """AI Insights Interface"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🤖 AI Performance Insights")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Department:"))
        self.department_combo = QComboBox()
        self.department_combo.addItem("All Departments", None)
        filter_layout.addWidget(self.department_combo)
        
        filter_layout.addWidget(QLabel("Risk Threshold:"))
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 100)
        self.threshold_spin.setValue(40)
        self.threshold_spin.setSuffix("%")
        filter_layout.addWidget(self.threshold_spin)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)
        filter_layout.addWidget(refresh_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Summary Cards
        cards_layout = QHBoxLayout()
        
        self.critical_card = self.create_stat_card("Critical Risk", "0", "#e74c3c")
        self.high_card = self.create_stat_card("High Risk", "0", "#e67e22")
        self.medium_card = self.create_stat_card("Medium Risk", "0", "#f39c12")
        self.total_card = self.create_stat_card("Total At-Risk", "0", "#3498db")
        
        cards_layout.addWidget(self.critical_card)
        cards_layout.addWidget(self.high_card)
        cards_layout.addWidget(self.medium_card)
        cards_layout.addWidget(self.total_card)
        
        layout.addLayout(cards_layout)
        
        # At-Risk Students Table
        table_label = QLabel("At-Risk Students")
        table_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Roll Number", "Name", "Department", "Risk Score", "Risk Level", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Load departments
        self.load_departments()
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        value_label.setObjectName("value_label")
        card_layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def load_departments(self):
        """Load departments"""
        departments = department_controller.get_all_departments()
        for dept in departments:
            self.department_combo.addItem(dept['department_name'], dept['department_id'])
    
    def load_data(self):
        """Load at-risk students"""
        dept_id = self.department_combo.currentData()
        threshold = self.threshold_spin.value()
        
        # Get at-risk students
        at_risk = ai_insights_controller.get_at_risk_students(
            department_id=dept_id,
            risk_threshold=threshold
        )
        
        # Update summary cards
        critical = len([s for s in at_risk if s['risk_level'] == 'Critical'])
        high = len([s for s in at_risk if s['risk_level'] == 'High'])
        medium = len([s for s in at_risk if s['risk_level'] == 'Medium'])
        
        self.critical_card.value_label.setText(str(critical))
        self.high_card.value_label.setText(str(high))
        self.medium_card.value_label.setText(str(medium))
        self.total_card.value_label.setText(str(len(at_risk)))
        
        # Populate table
        self.table.setRowCount(len(at_risk))
        
        for row, student in enumerate(at_risk):
            self.table.setItem(row, 0, QTableWidgetItem(student['roll_number']))
            self.table.setItem(row, 1, QTableWidgetItem(student['name']))
            self.table.setItem(row, 2, QTableWidgetItem(student['department']))
            
            # Risk score with color
            score_item = QTableWidgetItem(f"{student['risk_score']:.1f}%")
            if student['risk_score'] >= 70:
                score_item.setBackground(QColor("#e74c3c"))
                score_item.setForeground(QColor("white"))
            elif student['risk_score'] >= 50:
                score_item.setBackground(QColor("#e67e22"))
                score_item.setForeground(QColor("white"))
            else:
                score_item.setBackground(QColor("#f39c12"))
            self.table.setItem(row, 3, score_item)
            
            # Risk level
            level_item = QTableWidgetItem(student['risk_level'])
            self.table.setItem(row, 4, level_item)
            
            # Actions button
            actions_btn = QPushButton("View Details")
            actions_btn.clicked.connect(lambda checked, sid=student['student_id']: self.show_details(sid))
            self.table.setCellWidget(row, 5, actions_btn)
            
            # Store student_id
            self.table.item(row, 0).setData(Qt.UserRole, student['student_id'])
    
    def show_details(self, student_id):
        """Show detailed analysis for a student"""
        # Calculate risk score and get factors
        risk_score, factors = ai_insights_controller.calculate_risk_score(student_id)
        
        # Get recommendations
        recommendations = ai_insights_controller.get_intervention_recommendations(student_id)
        
        # Get prediction
        prediction = ai_insights_controller.get_performance_prediction(student_id)
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Student Risk Analysis")
        dialog.resize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Risk Score
        score_label = QLabel(f"<h2>Risk Score: {risk_score:.1f}%</h2>")
        layout.addWidget(score_label)
        
        # Risk Factors
        factors_group = QGroupBox("Risk Factors")
        factors_layout = QVBoxLayout()
        
        for factor_name, factor_data in factors.items():
            factor_text = f"<b>{factor_name.replace('_', ' ').title()}:</b> "
            factor_text += f"{factor_data.get('value', 0):.1f} "
            factor_text += f"(Risk: {factor_data.get('risk', 0):.1f}%, Weight: {factor_data.get('weight', 0)}%)"
            factors_layout.addWidget(QLabel(factor_text))
        
        factors_group.setLayout(factors_layout)
        layout.addWidget(factors_group)
        
        # Performance Prediction
        pred_group = QGroupBox("Performance Prediction")
        pred_layout = QVBoxLayout()
        pred_layout.addWidget(QLabel(f"<b>Current CGPA:</b> {prediction.get('current_cgpa', 0):.2f}"))
        pred_layout.addWidget(QLabel(f"<b>Predicted CGPA:</b> {prediction.get('predicted_cgpa', 0):.2f}"))
        pred_layout.addWidget(QLabel(f"<b>Prediction:</b> {prediction.get('prediction', 'N/A')}"))
        pred_group.setLayout(pred_layout)
        layout.addWidget(pred_group)
        
        # Recommendations
        rec_group = QGroupBox("Intervention Recommendations")
        rec_layout = QVBoxLayout()
        
        for i, rec in enumerate(recommendations, 1):
            rec_layout.addWidget(QLabel(f"{i}. {rec}"))
        
        rec_group.setLayout(rec_layout)
        layout.addWidget(rec_group)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
