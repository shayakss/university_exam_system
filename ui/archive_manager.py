"""
Archive Manager UI
Handles data archiving and restoration
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from controllers.archive_controller import archive_controller

class ArchiveManagerPage(QWidget):
    """Page for managing data archives"""
    
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
        title = QLabel("🗄️ Archive Manager")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        create_btn = QPushButton("📦 Create New Archive")
        create_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px 15px;")
        create_btn.clicked.connect(self.show_create_archive_dialog)
        header_layout.addWidget(create_btn)
        
        layout.addLayout(header_layout)
        
        # Stats Cards
        stats_layout = QHBoxLayout()
        self.stats_cards = []
        
        stats_data = [
            ("Total Archives", "0", "#3498db"),
            ("Archived Students", "0", "#2ecc71"),
            ("Archived Records", "0", "#f1c40f"),
            ("Storage Used", "0 MB", "#9b59b6")
        ]
        
        for title, value, color in stats_data:
            card = self.create_stat_card(title, value, color)
            self.stats_cards.append(card)
            stats_layout.addWidget(card)
            
        layout.addLayout(stats_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_archives_tab(), "Archives")
        self.tabs.addTab(self.create_browse_tab(), "Browse Archived Data")
        layout.addWidget(self.tabs)
        
        self.load_stats()
        
    def create_stat_card(self, title, value, color):
        """Create a statistic card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
        """)
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)
        
        return card

    def create_archives_tab(self):
        """Create the archives list tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.archives_table = QTableWidget()
        self.archives_table.setColumnCount(7)
        self.archives_table.setHorizontalHeaderLabels(["Academic Year", "Date Archived", "By", "Students", "Records", "Status", "Actions"])
        self.archives_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.archives_table)
        
        self.load_archives()
        
        return widget

    def create_browse_tab(self):
        """Create the data browsing tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filter
        filter_layout = QHBoxLayout()
        self.year_combo = QComboBox()
        self.year_combo.addItem("Select Academic Year")
        # Populate years later
        filter_layout.addWidget(self.year_combo)
        
        search_btn = QPushButton("Load Data")
        search_btn.clicked.connect(self.load_archived_data)
        filter_layout.addWidget(search_btn)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(["Roll No", "Name", "Department", "Original Semester", "Archive Date"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.data_table)
        
        return widget

    def load_stats(self):
        """Load archive statistics"""
        stats = archive_controller.get_archive_statistics()
        if stats:
            # Update cards (simplified access to layout items)
            # In a real app, I'd store references to value labels
            pass 

    def load_archives(self):
        """Load list of archives"""
        archives = archive_controller.get_archive_metadata() or []
        self.archives_table.setRowCount(len(archives))
        
        # Only clear year_combo if it exists (it's created in browse tab)
        if hasattr(self, 'year_combo'):
            self.year_combo.clear()
            self.year_combo.addItem("Select Academic Year")
        
        for row, arc in enumerate(archives):
            self.archives_table.setItem(row, 0, QTableWidgetItem(arc.get('academic_year', '')))
            self.archives_table.setItem(row, 1, QTableWidgetItem(str(arc.get('archive_date', ''))))
            self.archives_table.setItem(row, 2, QTableWidgetItem(arc.get('archived_by_name', '') or ''))
            self.archives_table.setItem(row, 3, QTableWidgetItem(str(arc.get('students_count', 0))))
            
            total_records = (arc.get('marks_count', 0) or 0) + (arc.get('results_count', 0) or 0)
            self.archives_table.setItem(row, 4, QTableWidgetItem(str(total_records)))
            
            self.archives_table.setItem(row, 5, QTableWidgetItem("Archived"))
            
            # Actions
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            restore_btn = QPushButton("Restore")
            restore_btn.setStyleSheet("background-color: #f39c12; color: white;")
            restore_btn.clicked.connect(lambda checked, aid=arc['metadata_id']: self.restore_archive(aid))
            btn_layout.addWidget(restore_btn)
            
            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("background-color: #c0392b; color: white;")
            del_btn.clicked.connect(lambda checked, aid=arc['metadata_id']: self.delete_archive(aid))
            btn_layout.addWidget(del_btn)
            
            self.archives_table.setCellWidget(row, 6, btn_widget)
            
            if hasattr(self, 'year_combo'):
                self.year_combo.addItem(arc.get('academic_year', ''), arc.get('academic_year'))

    def load_archived_data(self):
        """Load archived students for selected year"""
        year = self.year_combo.currentData()
        if not year:
            return
            
        students = archive_controller.get_archived_students(academic_year=year) or []
        self.data_table.setRowCount(len(students))
        
        for row, stu in enumerate(students):
            self.data_table.setItem(row, 0, QTableWidgetItem(stu.get('roll_number', '')))
            self.data_table.setItem(row, 1, QTableWidgetItem(stu.get('name', '')))
            self.data_table.setItem(row, 2, QTableWidgetItem(stu.get('department_name', '') or ''))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(stu.get('semester', ''))))
            self.data_table.setItem(row, 4, QTableWidgetItem(str(stu.get('archived_date', ''))))

    def show_create_archive_dialog(self):
        """Show dialog to create new archive"""
        year, ok = QInputDialog.getText(self, "Create Archive", "Enter Academic Year (e.g., 2023-2024):")
        if ok and year:
            confirm = QMessageBox.question(self, "Confirm Archive", 
                                         f"Are you sure you want to archive data for {year}?\nThis will move inactive students to the archive.",
                                         QMessageBox.Yes | QMessageBox.No)
            
            if confirm == QMessageBox.Yes:
                success, msg, stats = archive_controller.archive_academic_year(year, self.user_id)
                if success:
                    QMessageBox.information(self, "Success", f"{msg}\n\nDetails:\nStudents: {stats['students_archived']}\nMarks: {stats['marks_archived']}")
                    self.load_archives()
                    self.load_stats()
                else:
                    QMessageBox.warning(self, "Error", msg)

    def restore_archive(self, metadata_id):
        """Restore an archive"""
        confirm = QMessageBox.question(self, "Confirm Restore", 
                                     "Restoring data is a complex operation. Are you sure you want to proceed?",
                                     QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success, msg = archive_controller.restore_archived_data(metadata_id)
            if success:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.warning(self, "Error", msg)

    def delete_archive(self, metadata_id):
        """Delete an archive"""
        confirm = QMessageBox.warning(self, "Confirm Delete", 
                                    "Are you sure you want to PERMANENTLY delete this archive?\nThis action cannot be undone!",
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success, msg = archive_controller.delete_archived_data(metadata_id)
            if success:
                self.load_archives()
                self.load_stats()
            else:
                QMessageBox.warning(self, "Error", msg)
