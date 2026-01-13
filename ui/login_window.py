"""
Login Window - Clean Desktop-Style Authentication Interface
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QCheckBox, QMessageBox, QFrame,
                             QGraphicsDropShadowEffect, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap
from controllers.auth_controller import auth
from utils.resource_helper import resource_path
import config


class SpinnerWidget(QLabel):
    """Animated loading spinner widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.setFixedSize(24, 24)
        self.setAlignment(Qt.AlignCenter)
        
    def start(self):
        """Start spinner animation"""
        self.timer.start(50)
        self.show()
        
    def stop(self):
        """Stop spinner animation"""
        self.timer.stop()
        self.hide()
        
    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 30) % 360
        self.update()
        
    def paintEvent(self, event):
        """Draw animated spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Translate to center and rotate
        painter.translate(12, 12)
        painter.rotate(self.angle)
        
        # Draw spinner segments
        colors = ['#6366F1', '#818CF8', '#A5B4FC', '#C7D2FE', '#E0E7FF', '#EEF2FF']
        for i, color in enumerate(colors):
            painter.setBrush(QColor(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(-10 + i * 0, -10, 4, 4)
            painter.rotate(60)


class LoginWindow(QWidget):
    """Clean desktop-style login window"""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def paintEvent(self, event):
        """Custom paint event for soft gradient background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Gradient background
        from PyQt5.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(1, QColor("#764ba2"))
        painter.fillRect(self.rect(), gradient)
    
    def init_ui(self):
        """Initialize clean desktop UI"""
        self.setWindowTitle(f"{config.APP_NAME} - Login")
        self.setFixedSize(750, 850)  # Larger window size
        
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
                border-radius: 16px;
            }
        """)
        panel.setFixedWidth(520)
        panel.setGraphicsEffect(self.create_shadow())
        
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(60, 50, 60, 50)
        panel_layout.setSpacing(0)
        
        # TOP SECTION - Logo and Title
        # Logo/Icon
        logo = QLabel()
        logo_path = resource_path("resources/images/uob_logo.png")
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            # Scale logo to 100x100 while maintaining aspect ratio
            scaled_pixmap = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(scaled_pixmap)
        else:
            # Fallback to emoji if image not found
            logo.setText("🎓")
            logo.setFont(QFont("Segoe UI Emoji", 56))
        logo.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(logo)
        panel_layout.addSpacing(16)
        
        # Application Name
        app_name = QLabel("UOB Subcampus Kharan\nExamination System")
        app_name.setFont(QFont("Segoe UI", 22, QFont.DemiBold))
        app_name.setStyleSheet("color: #1F2937; line-height: 1.4;")
        app_name.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(app_name)
        panel_layout.addSpacing(8)
        
        # Subtitle
        subtitle = QLabel("Sign in to continue")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #6B7280;")
        subtitle.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(subtitle)
        panel_layout.addSpacing(40)
        
        # INPUT SECTION
        # Username
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 14, QFont.DemiBold))
        username_label.setStyleSheet("color: #374151;")
        panel_layout.addWidget(username_label)
        panel_layout.addSpacing(10)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(50)
        self.username_input.setFont(QFont("Segoe UI", 14))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                padding: 0 16px;
                color: #1F2937;
            }
            QLineEdit:focus {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
            }
        """)
        panel_layout.addWidget(self.username_input)
        panel_layout.addSpacing(20)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 14, QFont.DemiBold))
        password_label.setStyleSheet("color: #374151;")
        panel_layout.addWidget(password_label)
        panel_layout.addSpacing(10)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(50)
        self.password_input.setFont(QFont("Segoe UI", 14))
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                padding: 0 16px;
                color: #1F2937;
            }
            QLineEdit:focus {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        panel_layout.addWidget(self.password_input)
        panel_layout.addSpacing(24)
        
        # OPTIONS SECTION
        options_layout = QHBoxLayout()
        options_layout.setContentsMargins(0, 0, 0, 0)
        
        # Remember Me
        self.remember_checkbox = QCheckBox("Remember Me")
        self.remember_checkbox.setFont(QFont("Segoe UI", 13))
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #374151;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #D1D5DB;
                background-color: #F9FAFB;
            }
            QCheckBox::indicator:checked {
                background-color: #6366F1;
                border-color: #6366F1;
            }
            QCheckBox::indicator:hover {
                border-color: #6366F1;
            }
        """)
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        
        # Forgot Password
        forgot_password = QLabel('<a href="#" style="color: #6366F1; text-decoration: none; font-weight: 500;">Forgot Password?</a>')
        forgot_password.setFont(QFont("Segoe UI", 13))
        forgot_password.setOpenExternalLinks(False)
        forgot_password.setCursor(Qt.PointingHandCursor)
        options_layout.addWidget(forgot_password)
        
        panel_layout.addLayout(options_layout)
        panel_layout.addSpacing(32)
        
        # BUTTON SECTION with spinner
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.login_button = QPushButton("SIGN IN")
        self.login_button.setFixedHeight(54)
        self.login_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5558E3, stop:1 #7C4DE8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A4AD5, stop:1 #6D3EDA);
            }
            QPushButton:disabled {
                background: #C7D2FE;
                color: #FFFFFF;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)
        
        panel_layout.addLayout(button_layout)
        
        # Loading indicator (hidden by default)
        self.loading_container = QWidget()
        loading_layout = QHBoxLayout(self.loading_container)
        loading_layout.setContentsMargins(0, 16, 0, 0)
        loading_layout.setAlignment(Qt.AlignCenter)
        
        self.spinner = SpinnerWidget()
        loading_layout.addWidget(self.spinner)
        
        self.loading_label = QLabel("Signing in...")
        self.loading_label.setFont(QFont("Segoe UI", 13))
        self.loading_label.setStyleSheet("color: #6366F1; margin-left: 8px;")
        loading_layout.addWidget(self.loading_label)
        
        self.loading_container.hide()
        panel_layout.addWidget(self.loading_container)
        
        panel_layout.addSpacing(40)
        
        # FOOTER
        footer = QLabel("Developed by Shayak Siraj & Ahmed Ali")
        footer.setFont(QFont("Segoe UI", 12))
        footer.setStyleSheet("color: #9CA3AF;")
        footer.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(footer)
        
        version = QLabel(f"v{config.APP_VERSION}")
        version.setFont(QFont("Segoe UI", 11))
        version.setStyleSheet("color: #D1D5DB;")
        version.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(version)
        
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
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        return shadow
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        # Show loading state
        self.login_button.setEnabled(False)
        self.login_button.setText("⏳ SIGNING IN...")
        self.loading_container.show()
        self.spinner.start()
        
        # Process events to show loading state
        QApplication.processEvents()
        
        # Use QTimer to simulate async and show spinner
        QTimer.singleShot(100, lambda: self.perform_login(username, password))
    
    def perform_login(self, username, password):
        """Actually perform the login"""
        # Attempt login
        success, message, user_data = auth.login(username, password)
        
        # Stop spinner
        self.spinner.stop()
        self.loading_container.hide()
        
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

