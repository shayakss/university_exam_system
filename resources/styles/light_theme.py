"""
Light Theme Stylesheet
"""

class LightTheme:
    @staticmethod
    def get_stylesheet():
        return """
        /* Main Window */
        QMainWindow {
            background-color: #F5F7FA;
        }

        /* Menu Bar */
        QMenuBar {
            background-color: #FFFFFF;
            color: #2C3E50;
            border-bottom: 1px solid #E0E0E0;
        }
        QMenuBar::item:selected {
            background-color: #F0F2F5;
        }
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
        }
        QMenu::item:selected {
            background-color: #F0F2F5;
            color: #2C3E50;
        }

        /* Buttons */
        QPushButton {
            background-color: #FFFFFF;
            color: #2C3E50;
            border: 1px solid #D1D5DB;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #F9FAFB;
            border-color: #9CA3AF;
        }
        QPushButton:pressed {
            background-color: #F3F4F6;
        }
        QPushButton:disabled {
            background-color: #F3F4F6;
            color: #9CA3AF;
        }

        /* Primary Button */
        QPushButton[class="primary"] {
            background-color: #3498DB;
            color: white;
            border: none;
        }
        QPushButton[class="primary"]:hover {
            background-color: #2980B9;
        }

        /* Input Fields */
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {
            background-color: #FFFFFF;
            border: 1px solid #D1D5DB;
            border-radius: 6px;
            padding: 8px;
            color: #2C3E50;
            selection-background-color: #3498DB;
        }
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {
            border: 1px solid #3498DB;
        }

        /* Tables */
        QTableWidget {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            gridline-color: #F0F2F5;
            selection-background-color: #EBF5FB;
            selection-color: #2C3E50;
        }
        QHeaderView::section {
            background-color: #F8FAFC;
            color: #64748B;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #E0E0E0;
            font-weight: 600;
        }

        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #E0E0E0;
            background-color: #FFFFFF;
            border-radius: 6px;
        }
        QTabBar::tab {
            background-color: #F1F5F9;
            color: #64748B;
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #FFFFFF;
            color: #3498DB;
            font-weight: 600;
        }

        /* Group Box */
        QGroupBox {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 1.5em;
            padding-top: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            color: #2C3E50;
            font-weight: 600;
        }

        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background: #F1F5F9;
            width: 10px;
            margin: 0;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #CBD5E1;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: #94A3B8;
        }
        
        /* Labels */
        QLabel {
            color: #2C3E50;
        }
        """
