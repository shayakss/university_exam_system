"""
Modern Theme Stylesheet for PyQt5 Application
Professional SaaS-grade design
"""

# Color Palette
COLORS = {
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'primary_pressed': '#1e40af',
    'dark': '#1e293b',
    'dark_hover': '#334155',
    'light': '#f1f5f9',
    'white': '#ffffff',
    'border': '#e2e8f0',
    'border_dark': '#cbd5e1',
    'text_primary': '#0f172a',
    'text_secondary': '#64748b',
    'text_light': '#94a3b8',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'danger_hover': '#dc2626',
    'bg_hover': '#f8fafc',
}

def get_modern_stylesheet():
    """Returns the complete modern stylesheet"""
    return f"""
    /* Global Styles */
    QWidget {{
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: 13px;
        color: {COLORS['text_primary']};
    }}
    
    /* Main Window */
    QMainWindow {{
        background-color: {COLORS['light']};
    }}
    
    /* Sidebar Styles */
    QWidget#sidebar {{
        background-color: {COLORS['dark']};
        border-right: 1px solid {COLORS['border_dark']};
    }}
    
    /* Tab Widget - Modern Sidebar Style */
    QTabWidget::pane {{
        border: none;
        background-color: {COLORS['white']};
        border-radius: 8px;
        margin: 0px;
    }}
    
    QTabBar::tab {{
        background-color: transparent;
        color: {COLORS['text_light']};
        padding: 12px 20px;
        margin: 2px 8px;
        border: none;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        text-align: left;
        min-width: 180px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {COLORS['dark_hover']};
        color: {COLORS['white']};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {COLORS['white']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
        min-height: 36px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['bg_hover']};
        border-color: {COLORS['border_dark']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['light']};
    }}
    
    QPushButton#primaryButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
    }}
    
    QPushButton#primaryButton:hover {{
        background-color: {COLORS['primary_hover']};
    }}
    
    QPushButton#primaryButton:pressed {{
        background-color: {COLORS['primary_pressed']};
    }}
    
    QPushButton#dangerButton {{
        background-color: {COLORS['danger']};
        color: {COLORS['white']};
        border: none;
    }}
    
    QPushButton#dangerButton:hover {{
        background-color: {COLORS['danger_hover']};
    }}
    
    QPushButton#secondaryButton {{
        background-color: transparent;
        color: {COLORS['text_secondary']};
        border: 1px solid {COLORS['border']};
    }}
    
    QPushButton#secondaryButton:hover {{
        background-color: {COLORS['bg_hover']};
        color: {COLORS['text_primary']};
    }}
    
    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['primary']};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {COLORS['primary']};
        outline: none;
    }}
    
    QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{
        border-color: {COLORS['border_dark']};
    }}
    
    /* ComboBox */
    QComboBox {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        min-height: 36px;
    }}
    
    QComboBox:hover {{
        border-color: {COLORS['border_dark']};
    }}
    
    QComboBox:focus {{
        border-color: {COLORS['primary']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid {COLORS['text_secondary']};
        margin-right: 8px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        selection-background-color: {COLORS['primary']};
        selection-color: {COLORS['white']};
        padding: 4px;
    }}
    
    /* SpinBox */
    QSpinBox, QDoubleSpinBox {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        min-height: 36px;
    }}
    
    QSpinBox:hover, QDoubleSpinBox:hover {{
        border-color: {COLORS['border_dark']};
    }}
    
    QSpinBox:focus, QDoubleSpinBox:focus {{
        border-color: {COLORS['primary']};
    }}
    
    /* Tables */
    QTableWidget {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        gridline-color: {COLORS['border']};
        selection-background-color: {COLORS['primary']};
        selection-color: {COLORS['white']};
    }}
    
    QTableWidget::item {{
        padding: 8px;
        border: none;
    }}
    
    QTableWidget::item:hover {{
        background-color: {COLORS['bg_hover']};
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['light']};
        color: {COLORS['text_secondary']};
        padding: 12px 8px;
        border: none;
        border-bottom: 2px solid {COLORS['border']};
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    QHeaderView::section:hover {{
        background-color: {COLORS['border']};
    }}
    
    /* Scrollbars */
    QScrollBar:vertical {{
        background-color: {COLORS['light']};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {COLORS['border_dark']};
        border-radius: 6px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['text_secondary']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background-color: {COLORS['light']};
        height: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {COLORS['border_dark']};
        border-radius: 6px;
        min-width: 30px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {COLORS['text_secondary']};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* Labels */
    QLabel#titleLabel {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['text_primary']};
        padding: 0px;
        margin-bottom: 8px;
    }}
    
    QLabel#subtitleLabel {{
        font-size: 15px;
        font-weight: 600;
        color: {COLORS['text_primary']};
    }}
    
    QLabel#sectionLabel {{
        font-size: 13px;
        font-weight: 600;
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* GroupBox */
    QGroupBox {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        margin-top: 16px;
        padding: 16px;
        font-weight: 600;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        color: {COLORS['text_primary']};
        background-color: {COLORS['white']};
    }}
    
    /* Dialog */
    QDialog {{
        background-color: {COLORS['white']};
    }}
    
    /* Menu */
    QMenu {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 8px 16px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {COLORS['white']};
        border-top: 1px solid {COLORS['border']};
        color: {COLORS['text_secondary']};
    }}
    
    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        background-color: {COLORS['light']};
        text-align: center;
        height: 24px;
    }}
    
    QProgressBar::chunk {{
        background-color: {COLORS['primary']};
        border-radius: 5px;
    }}
    
    /* CheckBox */
    QCheckBox {{
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {COLORS['border_dark']};
        border-radius: 4px;
        background-color: {COLORS['white']};
    }}
    
    QCheckBox::indicator:hover {{
        border-color: {COLORS['primary']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEgNEw0LjUgNy41TDExIDEiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+);
    }}
    
    /* Radio Button */
    QRadioButton {{
        spacing: 8px;
    }}
    
    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {COLORS['border_dark']};
        border-radius: 9px;
        background-color: {COLORS['white']};
    }}
    
    QRadioButton::indicator:hover {{
        border-color: {COLORS['primary']};
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
    }}
    
    QRadioButton::indicator:checked::after {{
        content: "";
        width: 8px;
        height: 8px;
        border-radius: 4px;
        background-color: {COLORS['white']};
    }}
    """

def get_card_style():
    """Returns stylesheet for card-like containers"""
    return f"""
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 16px;
    """

def get_stats_card_style():
    """Returns stylesheet for statistics cards"""
    return f"""
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 20px;
        min-height: 100px;
    """
