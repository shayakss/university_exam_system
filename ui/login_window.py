"""
Login Window - Clean Desktop-Style Authentication Interface
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QCheckBox, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap
from controllers.auth_controller import auth
from utils.resource_helper import resource_path
import config


class LoginWindow(QWidget):
    """Clean desktop-style login window"""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def paintEvent(self, event):
        """Custom paint event for soft background"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#F2F4F7"))
    
    def init_ui(self):
        """Initialize clean desktop UI"""
        self.setWindowTitle(f"{config.APP_NAME} - Login")
        self.setFixedSize(600, 700)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Center vertically
        main_layout.addStretch(1)
        
        # Login panel (card)
        panel = QFrame()
        panel.setObjectName("loginPanel")
        panel.setStyleSheet("""
            QFrame#loginPanel {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
        """)
        panel.setFixedWidth(480)
        panel.setGraphicsEffect(self.create_shadow())
        
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(50, 40, 50, 40)
        panel_layout.setSpacing(0)
        
        # TOP SECTION - Logo and Title
        # Logo/Icon
        logo = QLabel()
        logo_path = resource_path("resources/images/uob_logo.png")
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            # Scale logo to 80x80 while maintaining aspect ratio
            scaled_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(scaled_pixmap)
        else:
            # Fallback to emoji if image not found
            logo.setText("🎓")
            logo.setFont(QFont("Segoe UI Emoji", 48))
        logo.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(logo)
        panel_layout.addSpacing(10)
        
        # Application Name
        app_name = QLabel("UOB Subcampus Kharan\nExamination System")
        app_name.setFont(QFont("Segoe UI", 18, QFont.DemiBold))
        app_name.setStyleSheet("color: #2C3E50; line-height: 1.3;")
        app_name.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(app_name)
        panel_layout.addSpacing(8)
        
        # Subtitle
        subtitle = QLabel("Sign in to continue")
        subtitle.setFont(QFont("Segoe UI", 13, QFont.Medium))
        subtitle.setStyleSheet("color: #6c6c6c;")
        subtitle.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(subtitle)
        panel_layout.addSpacing(32)
        
        # INPUT SECTION
        # Username
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 13, QFont.DemiBold))
        username_label.setStyleSheet("color: #2C3E50;")
        panel_layout.addWidget(username_label)
        panel_layout.addSpacing(8)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(42)
        self.username_input.setFont(QFont("Segoe UI", 13))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FAFAFA;
                border: 1px solid #D5D8DC;
                border-radius: 6px;
                padding: 0 12px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border: 1px solid #6A5ACD;
                background-color: #FFFFFF;
            }
            QLineEdit::placeholder {
                color: #A0A0A0;
            }
        """)
        panel_layout.addWidget(self.username_input)
        panel_layout.addSpacing(16)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 13, QFont.DemiBold))
        password_label.setStyleSheet("color: #2C3E50;")
        panel_layout.addWidget(password_label)
        panel_layout.addSpacing(8)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(42)
        self.password_input.setFont(QFont("Segoe UI", 13))
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #FAFAFA;
                border: 1px solid #D5D8DC;
                border-radius: 6px;
                padding: 0 12px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border: 1px solid #6A5ACD;
                background-color: #FFFFFF;
            }
            QLineEdit::placeholder {
                color: #A0A0A0;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        panel_layout.addWidget(self.password_input)
        panel_layout.addSpacing(20)
        
        # OPTIONS SECTION
        options_layout = QHBoxLayout()
        options_layout.setContentsMargins(0, 0, 0, 0)
        
        # Remember Me
        self.remember_checkbox = QCheckBox("Remember Me")
        self.remember_checkbox.setFont(QFont("Segoe UI", 12))
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2C3E50;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid #D5D8DC;
                background-color: #FAFAFA;
            }
            QCheckBox::indicator:checked {
                background-color: #6366F1;
                border-color: #6366F1;
                image: url(none);
            }
            QCheckBox::indicator:hover {
                border-color: #6A5ACD;
            }
        """)
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        
        # Forgot Password
        forgot_password = QLabel('<a href="#" style="color: #6366F1; text-decoration: none;">Forgot Password?</a>')
        forgot_password.setFont(QFont("Segoe UI", 12))
        forgot_password.setOpenExternalLinks(False)
        forgot_password.setCursor(Qt.PointingHandCursor)
        options_layout.addWidget(forgot_password)
        
        panel_layout.addLayout(options_layout)
        panel_layout.addSpacing(24)
        
        # BUTTON SECTION
        self.login_button = QPushButton("SIGN IN")
        self.login_button.setFixedHeight(46)
        self.login_button.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5558E3, stop:1 #7C4DE8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A4AD5, stop:1 #6D3EDA);
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        panel_layout.addWidget(self.login_button)
        panel_layout.addSpacing(32)
        
        # FOOTER
        footer = QLabel("Developed by Shayak Siraj & Ahmed Ali")
        footer.setFont(QFont("Segoe UI", 11))
        footer.setStyleSheet("color: #A0A0A0;")
        footer.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(footer)
        
        # Center the panel horizontally
        panel_container = QHBoxLayout()
        panel_container.addStretch()
        panel_container.addWidget(panel)
        panel_container.addStretch()
        
        main_layout.addLayout(panel_container)
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)
        
        # Set focus to username
        self.username_input.setFocus()
    
    def create_shadow(self):
        """Create shadow effect for the panel"""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(32)
        shadow.setXOffset(0)
        shadow.setYOffset(12)
        shadow.setColor(QColor(0, 0, 0, 25))  # rgba(0,0,0,0.10)
        return shadow
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        # Disable button during login
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        
        # Attempt login
        success, message, user_data = auth.login(username, password)
        
        if success:
            # Close login window and open main window
            from ui.main_window import MainWindow
            self.main_window = MainWindow(user_data)
            self.main_window.show()
            self.close()
        else:
            # Re-enable button
            self.login_button.setEnabled(True)
            self.login_button.setText("SIGN IN")
            
            QMessageBox.critical(self, "Login Failed", message)
            self.password_input.clear()
            self.password_input.setFocus()
