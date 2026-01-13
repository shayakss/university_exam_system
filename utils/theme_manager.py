"""
Theme Manager
Manages application themes (Light/Dark mode)
"""
from typing import Dict

class ThemeManager:
    """Manages application themes"""
    
    def __init__(self):
        self.current_theme = 'Light'
        self.themes = {
            'Light': self.get_light_theme(),
            'Dark': self.get_dark_theme()
        }
    
    def get_light_theme(self) -> str:
        """Get light theme stylesheet"""
        return """
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                gridline-color: #e0e0e0;
                border: 1px solid #ddd;
            }
            
            QTableWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #2C3E50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                color: #333;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
            }
            
            QLabel {
                color: #333333;
            }
            
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333;
                padding: 10px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                color: #2196F3;
                font-weight: bold;
            }
            
            QMenuBar {
                background-color: #2C3E50;
                color: white;
            }
            
            QMenuBar::item:selected {
                background-color: #34495E;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
            }
            
            QMenu::item:selected {
                background-color: #2196F3;
                color: white;
            }
        """
    
    def get_dark_theme(self) -> str:
        """Get dark theme stylesheet"""
        return """
            QMainWindow, QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QPushButton {
                background-color: #0D47A1;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1565C0;
            }
            
            QPushButton:pressed {
                background-color: #0A3D91;
            }
            
            QTableWidget {
                background-color: #2D2D2D;
                alternate-background-color: #252525;
                gridline-color: #404040;
                border: 1px solid #404040;
                color: #E0E0E0;
            }
            
            QTableWidget::item:selected {
                background-color: #0D47A1;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #1565C0;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {
                background-color: #2D2D2D;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 6px;
                color: #E0E0E0;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #0D47A1;
            }
            
            QLabel {
                color: #E0E0E0;
            }
            
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #2D2D2D;
            }
            
            QTabBar::tab {
                background-color: #252525;
                color: #E0E0E0;
                padding: 10px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #2D2D2D;
                color: #2196F3;
                font-weight: bold;
            }
            
            QMenuBar {
                background-color: #1565C0;
                color: white;
            }
            
            QMenuBar::item:selected {
                background-color: #0D47A1;
            }
            
            QMenu {
                background-color: #2D2D2D;
                border: 1px solid #404040;
                color: #E0E0E0;
            }
            
            QMenu::item:selected {
                background-color: #0D47A1;
                color: white;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2D2D2D;
                color: #E0E0E0;
                selection-background-color: #0D47A1;
            }
        """
    
    def get_theme(self, theme_name: str) -> str:
        """Get theme stylesheet by name"""
        return self.themes.get(theme_name, self.themes['Light'])
    
    def set_theme(self, theme_name: str):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def get_current_theme(self) -> str:
        """Get current theme name"""
        return self.current_theme
    
    def save_user_preference(self, user_id: int, theme: str):
        """Save user's theme preference to database"""
        try:
            from database.db_manager import db
            
            # Check if preference exists
            check_query = "SELECT preference_id FROM user_preferences WHERE user_id = ?"
            existing = db.execute_query(check_query, (user_id,))
            
            if existing:
                query = "UPDATE user_preferences SET theme = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?"
                db.execute_update(query, (theme, user_id))
            else:
                query = "INSERT INTO user_preferences (user_id, theme) VALUES (?, ?)"
                db.execute_update(query, (user_id, theme))
                
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    def load_user_preference(self, user_id: int) -> str:
        """Load user's theme preference from database"""
        try:
            from database.db_manager import db
            
            query = "SELECT theme FROM user_preferences WHERE user_id = ?"
            result = db.execute_query(query, (user_id,))
            
            if result and result[0]['theme']:
                return result[0]['theme']
            
            return 'Light'  # Default
            
        except Exception as e:
            print(f"Error loading theme preference: {e}")
            return 'Light'

# Global instance
theme_manager = ThemeManager()
