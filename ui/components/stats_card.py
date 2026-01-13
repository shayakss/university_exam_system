"""
Stats Card Component
Display statistics with icon, number, and label
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from ui.styles import COLORS


class StatsCard(QFrame):
    """Statistics card for dashboard"""
    
    def __init__(self, title, value, icon="📊", color=None, parent=None):
        super().__init__(parent)
        
        # Use provided color or default to primary
        bg_color = color or COLORS['primary']
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: {bg_color};
            }}
        """)
        self.setFrameShape(QFrame.NoFrame)
        self.setMinimumHeight(120)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Top row: Icon and title
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {bg_color};
        """)
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 500;
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Value
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        layout.addWidget(value_label)
        
        layout.addStretch()
    
    def update_value(self, new_value):
        """Update the displayed value"""
        # Find the value label and update it
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.styleSheet().find('font-size: 32px') != -1:
                widget.setText(str(new_value))
                break
