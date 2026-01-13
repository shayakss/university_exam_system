"""
ID Card Generator UI
Handles ID card generation and preview
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from controllers.id_card_controller import id_card_controller
from controllers.student_controller import student_controller
from controllers.user_controller import user_controller
import qrcode
from io import BytesIO

class IDCardGeneratorPage(QWidget):
    """Page for generating and managing ID cards"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.user_id = user_data.get('user_id')
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🪪 ID Card Generator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_generator_tab(), "Generate Card")
        self.tabs.addTab(self.create_history_tab(), "Card History")
        layout.addWidget(self.tabs)
        
    def create_generator_tab(self):
        """Create the generator tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left Panel: Controls
        left_panel = QFrame()
        left_panel.setFixedWidth(350)
        left_panel.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("<b>Select Type:</b>"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Student", "Staff/Teacher"])
        self.type_combo.currentIndexChanged.connect(self.load_entities)
        left_layout.addWidget(self.type_combo)
        
        left_layout.addWidget(QLabel("<b>Select Person:</b>"))
        self.person_combo = QComboBox()
        self.person_combo.setEditable(True) # Allow searching
        self.person_combo.currentIndexChanged.connect(self.update_preview)
        left_layout.addWidget(self.person_combo)
        
        left_layout.addStretch()
        
        self.generate_btn = QPushButton("Generate ID Card")
        self.generate_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 10px;")
        self.generate_btn.clicked.connect(self.generate_card)
        left_layout.addWidget(self.generate_btn)
        
        layout.addWidget(left_panel)
        
        # Right Panel: Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        preview_label = QLabel("Card Preview")
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #7f8c8d;")
        right_layout.addWidget(preview_label)
        
        self.card_preview = QLabel()
        self.card_preview.setAlignment(Qt.AlignCenter)
        self.card_preview.setStyleSheet("border: 2px dashed #bdc3c7; border-radius: 10px; background-color: #ecf0f1;")
        self.card_preview.setMinimumSize(400, 250)
        right_layout.addWidget(self.card_preview)
        
        layout.addWidget(right_panel)
        
        self.load_entities()
        
        return widget

    def create_history_tab(self):
        """Create the history tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(["Card No", "Type", "Name", "Issue Date", "Expiry Date", "Status", "Action"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        return widget

    def load_entities(self):
        """Load students or staff based on selection"""
        self.person_combo.clear()
        card_type = self.type_combo.currentText()
        
        try:
            if card_type == "Student":
                students = student_controller.get_all_students()
                for s in students:
                    self.person_combo.addItem(f"{s['roll_number']} - {s['name']}", s)
            else:
                users = user_controller.get_all_users()
                for u in users:
                    if u['role'] in ['Teacher', 'Admin', 'DataEntry']:
                        self.person_combo.addItem(f"{u['username']} - {u['full_name']}", u)
        except Exception as e:
            print(f"Error loading entities: {e}")

    def update_preview(self):
        """Update the ID card preview"""
        data = self.person_combo.currentData()
        if not data:
            self.card_preview.clear()
            self.card_preview.setText("Select a person to preview")
            return
            
        # Create a pixmap for the card
        width, height = 400, 250
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.setBrush(QColor("#f8f9fa"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, width, height, 15, 15)
        
        # Header
        header_color = QColor("#3498db") if self.type_combo.currentText() == "Student" else QColor("#e74c3c")
        painter.setBrush(header_color)
        painter.drawRoundedRect(0, 0, width, 60, 15, 15)
        painter.drawRect(0, 30, width, 30) # Fix bottom corners
        
        # Header Text
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(0, 0, width, 60, Qt.AlignCenter, "University ID Card")
        
        # Content
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        
        name = data.get('name') or data.get('full_name')
        role = "Student" if self.type_combo.currentText() == "Student" else data.get('role')
        
        painter.drawText(20, 90, f"Name: {name}")
        painter.drawText(20, 120, f"Role: {role}")
        
        if role == "Student":
            painter.drawText(20, 150, f"Roll No: {data.get('roll_number')}")
            # Need to fetch department name if not in data, but let's assume it is or skip
        
        # QR Code
        qr_content = f"{name}-{role}" # Simple content for preview
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(qr_content)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert PIL image to QImage
        qr_img_qt = QImage(qr_img.tobytes(), qr_img.size[0], qr_img.size[1], QImage.Format_Grayscale8)
        painter.drawImage(width - 110, 80, qr_img_qt.scaled(90, 90, Qt.KeepAspectRatio))
        
        painter.end()
        
        self.card_preview.setPixmap(QPixmap.fromImage(image))

    def generate_card(self):
        """Generate the ID card"""
        data = self.person_combo.currentData()
        if not data:
            return
            
        card_type = self.type_combo.currentText()
        
        try:
            if card_type == "Student":
                success, msg, details = id_card_controller.generate_student_id_card(
                    data['student_id'], self.user_id
                )
            else:
                success, msg, details = id_card_controller.generate_staff_id_card(
                    data['user_id'], self.user_id
                )
                
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_history()
            else:
                QMessageBox.warning(self, "Error", msg)
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate card: {str(e)}")

    def load_history(self):
        """Load card history"""
        try:
            cards = id_card_controller.get_id_cards()
            self.history_table.setRowCount(len(cards))
            
            for row, card in enumerate(cards):
                self.history_table.setItem(row, 0, QTableWidgetItem(card['card_number']))
                self.history_table.setItem(row, 1, QTableWidgetItem(card['card_type']))
                
                name = card['student_name'] if card['card_type'] == 'Student' else card['staff_name']
                self.history_table.setItem(row, 2, QTableWidgetItem(name))
                self.history_table.setItem(row, 3, QTableWidgetItem(card['issue_date']))
                self.history_table.setItem(row, 4, QTableWidgetItem(card['expiry_date']))
                
                status_item = QTableWidgetItem("Active" if card['is_active'] else "Inactive")
                status_item.setForeground(Qt.green if card['is_active'] else Qt.red)
                self.history_table.setItem(row, 5, status_item)
                
                if card['is_active']:
                    btn = QPushButton("Deactivate")
                    btn.setStyleSheet("background-color: #e74c3c; color: white;")
                    btn.clicked.connect(lambda checked, cid=card['card_id']: self.deactivate_card(cid))
                    self.history_table.setCellWidget(row, 6, btn)
                else:
                    self.history_table.setItem(row, 6, QTableWidgetItem("-"))
                    
        except Exception as e:
            print(f"Error loading history: {e}")

    def deactivate_card(self, card_id):
        """Deactivate a card"""
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to deactivate this card?",
                                     QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success, msg = id_card_controller.deactivate_id_card(card_id)
            if success:
                self.load_history()
            else:
                QMessageBox.warning(self, "Error", msg)
