"""
Modern Card Component
Reusable card widget with title and content area
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from ui.styles import get_card_style, COLORS


class ModernCard(QFrame):
    """Modern card component with optional title"""
    
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_card_style())
        self.setFrameShape(QFrame.NoFrame)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)
        
        # Title if provided
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("subtitleLabel")
            title_label.setStyleSheet(f"""
                font-size: 16px;
                font-weight: 600;
                color: {COLORS['text_primary']};
                margin-bottom: 8px;
            """)
            self.main_layout.addWidget(title_label)
        
        # Content layout (for child widgets)
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(12)
        self.main_layout.addLayout(self.content_layout)
    
    def add_widget(self, widget):
        """Add a widget to the card content"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add a layout to the card content"""
        self.content_layout.addLayout(layout)
