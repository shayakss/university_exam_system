"""
Dark Theme Stylesheet
"""

class DarkTheme:
    @staticmethod
    def get_stylesheet():
        return """
        /* Main Window */
        QMainWindow {
            background-color: #1E1E1E;
        }

        /* Menu Bar */
        QMenuBar {
            background-color: #252526;
            color: #CCCCCC;
            border-bottom: 1px solid #333333;
        }
        QMenuBar::item:selected {
            background-color: #37373D;
        }
        QMenu {
            background-color: #252526;
            color: #CCCCCC;
            border: 1px solid #333333;
        }
        QMenu::item:selected {
            background-color: #094771;
            color: white;
        }

        /* Buttons */
        QPushButton {
            background-color: #3C3C3C;
            color: #CCCCCC;
            border: 1px solid #333333;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #444444;
            border-color: #555555;
        }
        QPushButton:pressed {
            background-color: #2D2D2D;
        }
        QPushButton:disabled {
            background-color: #2D2D2D;
            color: #666666;
            border-color: #333333;
        }

        /* Primary Button */
        QPushButton[class="primary"] {
            background-color: #0E639C;
            color: white;
            border: none;
        }
        QPushButton[class="primary"]:hover {
            background-color: #1177BB;
        }

        /* Input Fields */
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {
            background-color: #3C3C3C;
            border: 1px solid #333333;
            border-radius: 6px;
            padding: 8px;
            color: #CCCCCC;
            selection-background-color: #264F78;
        }
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {
            border: 1px solid #007ACC;
        }

        /* Tables */
        QTableWidget {
            background-color: #1E1E1E;
            border: 1px solid #333333;
            gridline-color: #333333;
            selection-background-color: #37373D;
            selection-color: white;
            color: #CCCCCC;
        }
        QHeaderView::section {
            background-color: #252526;
            color: #CCCCCC;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #333333;
            font-weight: 600;
        }

        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #333333;
            background-color: #1E1E1E;
            border-radius: 6px;
        }
        QTabBar::tab {
            background-color: #2D2D2D;
            color: #999999;
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #1E1E1E;
            color: #007ACC;
            font-weight: 600;
        }

        /* Group Box */
        QGroupBox {
            background-color: #1E1E1E;
            border: 1px solid #333333;
            border-radius: 8px;
            margin-top: 1.5em;
            padding-top: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            color: #CCCCCC;
            font-weight: 600;
        }

        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background: #1E1E1E;
            width: 10px;
            margin: 0;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #424242;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: #4F4F4F;
        }
        
        /* Labels */
        QLabel {
            color: #CCCCCC;
        }
        """
