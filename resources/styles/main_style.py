"""
QSS Stylesheet for the application - Minimalist Design
"""

MAIN_STYLESHEET = """
/* Main Window */
QMainWindow {
    background-color: #F5F5F5;
}

/* Menu Bar */
QMenuBar {
    background-color: white;
    color: #333333;
    border-bottom: 1px solid #CCCCCC;
    padding: 5px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background-color: #E0E0E0;
}

QMenu {
    background-color: white;
    color: #333333;
    border: 1px solid #CCCCCC;
}

QMenu::item:selected {
    background-color: #E0E0E0;
}

/* Buttons */
QPushButton {
    background-color: white;
    color: #333333;
    border: 1px solid #CCCCCC;
    padding: 6px 16px;
    border-radius: 3px;
    font-size: 11px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #F0F0F0;
    border-color: #999999;
}

QPushButton:pressed {
    background-color: #E0E0E0;
}

QPushButton:disabled {
    background-color: #F5F5F5;
    color: #AAAAAA;
    border-color: #DDDDDD;
}

QPushButton#primaryButton {
    background-color: white;
    border: 1px solid #CCCCCC;
}

QPushButton#primaryButton:hover {
    background-color: #F0F0F0;
}

QPushButton#dangerButton {
    background-color: white;
    color: #D32F2F;
    border: 1px solid #CCCCCC;
}

QPushButton#dangerButton:hover {
    background-color: #FFEBEE;
}

QPushButton#secondaryButton {
    background-color: white;
    border: 1px solid #CCCCCC;
}

/* Line Edit */
QLineEdit {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    background-color: white;
    font-size: 11px;
}

QLineEdit:focus {
    border: 1px solid #666666;
}

QLineEdit:disabled {
    background-color: #F5F5F5;
    color: #AAAAAA;
}

/* Text Edit */
QTextEdit, QPlainTextEdit {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    background-color: white;
    font-size: 11px;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #666666;
}

/* Combo Box */
QComboBox {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    background-color: white;
    font-size: 11px;
}

QComboBox:focus {
    border: 1px solid #666666;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    border: 1px solid #CCCCCC;
    selection-background-color: #E0E0E0;
    background-color: white;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    background-color: white;
    font-size: 11px;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #666666;
}

/* Date Edit */
QDateEdit {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    background-color: white;
    font-size: 11px;
}

QDateEdit:focus {
    border: 1px solid #666666;
}

/* Table Widget */
QTableWidget {
    border: 1px solid #CCCCCC;
    background-color: white;
    gridline-color: #E0E0E0;
    font-size: 10px;
}

QTableWidget::item {
    padding: 5px;
    border-bottom: 1px solid #E0E0E0;
}

QTableWidget::item:selected {
    background-color: #E8F4F8;
    color: #333333;
}

QHeaderView::section {
    background-color: #F5F5F5;
    color: #333333;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #CCCCCC;
    border-right: 1px solid #E0E0E0;
    font-weight: bold;
    font-size: 10px;
}

QHeaderView::section:hover {
    background-color: #EEEEEE;
}

/* Scroll Bar */
QScrollBar:vertical {
    border: none;
    background-color: #F5F5F5;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #CCCCCC;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #AAAAAA;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #F5F5F5;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #CCCCCC;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #AAAAAA;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #CCCCCC;
    background-color: white;
    top: -1px;
}

QTabBar::tab {
    background-color: #F5F5F5;
    color: #333333;
    padding: 8px 20px;
    margin-right: 2px;
    border: 1px solid #CCCCCC;
    border-bottom: none;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
}

QTabBar::tab:selected {
    background-color: white;
    color: #333333;
    font-weight: bold;
    border-bottom: 1px solid white;
}

QTabBar::tab:hover {
    background-color: #EEEEEE;
}

/* Group Box */
QGroupBox {
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    margin-top: 10px;
    font-weight: bold;
    padding-top: 10px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #333333;
}

/* Label */
QLabel {
    color: #333333;
    font-size: 11px;
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: bold;
    color: #333333;
}

QLabel#subtitleLabel {
    font-size: 12px;
    font-weight: bold;
    color: #666666;
}

QLabel#errorLabel {
    color: #D32F2F;
    font-weight: bold;
}

QLabel#successLabel {
    color: #388E3C;
    font-weight: bold;
}

/* Status Bar */
QStatusBar {
    background-color: #F5F5F5;
    color: #666666;
    border-top: 1px solid #CCCCCC;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #CCCCCC;
    border-radius: 3px;
    text-align: center;
    background-color: white;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 2px;
}

/* Check Box */
QCheckBox {
    spacing: 5px;
    color: #333333;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #CCCCCC;
    border-radius: 2px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

/* Radio Button */
QRadioButton {
    spacing: 5px;
    color: #333333;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #CCCCCC;
    border-radius: 8px;
    background-color: white;
}

QRadioButton::indicator:checked {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

/* Tool Tip */
QToolTip {
    background-color: #333333;
    color: white;
    border: 1px solid #666666;
    padding: 5px;
    border-radius: 3px;
}

/* Card Style Widget */
QFrame#card {
    background-color: white;
    border-radius: 3px;
    border: 1px solid #CCCCCC;
}

/* Dialog */
QDialog {
    background-color: white;
}

/* List Widget */
QListWidget {
    border: 1px solid #CCCCCC;
    background-color: white;
}

QListWidget::item {
    padding: 5px;
    border-bottom: 1px solid #E0E0E0;
}

QListWidget::item:selected {
    background-color: #E8F4F8;
    color: #333333;
}

QListWidget::item:hover {
    background-color: #F5F5F5;
}
"""
