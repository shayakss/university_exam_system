"""
Student Management Page - Enhanced CRUD with Pagination, Filters, and Stats
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QDialog,
                             QFormLayout, QComboBox, QDateEdit, QMessageBox, QFileDialog,
                             QApplication, QProgressBar, QFrame, QHeaderView, QSpinBox,
                             QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, QDate, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QBrush
from controllers.student_controller import student_controller
from controllers.department_controller import department_controller


class StudentLoaderThread(QThread):
    """Background thread for loading students without blocking UI"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, department_id=None, semester=None, gender=None, search_term=None):
        super().__init__()
        self.department_id = department_id
        self.semester = semester
        self.gender = gender
        self.search_term = search_term
    
    def run(self):
        try:
            if self.search_term:
                students = student_controller.search_students(self.search_term)
            elif self.department_id:
                students = student_controller.get_students_by_department(self.department_id)
            else:
                students = student_controller.get_all_students()
            
            # Apply additional filters in memory
            students = students or []
            if self.semester and self.semester > 0:
                students = [s for s in students if s.get('semester') == self.semester]
            if self.gender and self.gender != 'All':
                students = [s for s in students if s.get('gender') == self.gender]
            
            self.finished.emit(students)
        except Exception as e:
            self.error.emit(str(e))


class StudentManagementPage(QWidget):
    """Enhanced student management with pagination, filters, stats"""
    
    # Constants
    ROWS_PER_PAGE = 25
    
    def __init__(self, parent=None, department_id=None):
        super().__init__(parent)
        self.all_students = []  # All loaded students
        self.filtered_students = []  # After filters applied
        self.students_data = []  # Current page data
        self.department_id = department_id
        self.loader_thread = None
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._do_search)
        
        # Pagination state
        self.current_page = 1
        self.total_pages = 1
        
        # Sorting state
        self.sort_column = 1  # Name column
        self.sort_order = Qt.AscendingOrder
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("👥 Student Management")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #1F2937; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Stats section removed as per user request
        
        # ========== FILTERS SECTION ==========
        self.create_filters_section(layout)
        
        # ========== ACTION BUTTONS ==========
        self.create_actions_section(layout)
        
        # ========== TABLE ==========
        self.create_table(layout)
        
        # ========== PAGINATION ==========
        self.create_pagination_section(layout)
        
        # Load students asynchronously
        QTimer.singleShot(100, self.load_students)
    
    # stats cards removed as per request
    
    def create_stat_card(self, title, value, color, icon):
        """Create a single stat card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 4px solid {color};
                padding: 12px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 8, 12, 8)
        card_layout.setSpacing(4)
        
        # Title row with icon
        title_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px;")
        title_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6B7280; font-size: 12px; font-weight: 500;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        card_layout.addLayout(title_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        value_label.setObjectName("valueLabel")
        card_layout.addWidget(value_label)
        
        return card
    
    def create_filters_section(self, layout):
        """Create advanced filters"""
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E5E7EB;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(16)
        
        # Search
        search_icon = QLabel("🔍")
        filter_layout.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, roll number, email...")
        self.search_input.setMinimumWidth(250)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
            }
        """)
        self.search_input.textChanged.connect(self.search_students)
        filter_layout.addWidget(self.search_input)
        
        # Department filter
        filter_layout.addWidget(QLabel("Department:"))
        self.dept_filter = QComboBox()
        self.dept_filter.setMinimumWidth(150)
        self.dept_filter.addItem("All Departments", None)
        departments = department_controller.get_all_departments() or []
        for dept in departments:
            self.dept_filter.addItem(dept['department_name'], dept['department_id'])
        self.dept_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.dept_filter)
        
        # Semester filter
        filter_layout.addWidget(QLabel("Semester:"))
        self.sem_filter = QComboBox()
        self.sem_filter.addItem("All", 0)
        for i in range(1, 9):
            self.sem_filter.addItem(f"Semester {i}", i)
        self.sem_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.sem_filter)
        
        # Gender filter
        filter_layout.addWidget(QLabel("Gender:"))
        self.gender_filter = QComboBox()
        self.gender_filter.addItems(["All", "Male", "Female"])
        self.gender_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.gender_filter)
        
        # Loading indicator
        self.loading_label = QLabel("")
        self.loading_label.setStyleSheet("color: #3B82F6; font-weight: bold;")
        filter_layout.addWidget(self.loading_label)
        
        filter_layout.addStretch()
        
        # Clear filters button
        clear_btn = QPushButton("✕ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        clear_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(clear_btn)
        
        layout.addWidget(filter_frame)
    
    def create_actions_section(self, layout):
        """Create action buttons"""
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # Add Student
        add_btn = QPushButton("➕ Add Student")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        add_btn.clicked.connect(self.add_student)
        actions_layout.addWidget(add_btn)
        
        # Edit
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        edit_btn.clicked.connect(self.edit_student_from_selection)
        actions_layout.addWidget(edit_btn)
        
        # Delete
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        delete_btn.clicked.connect(self.delete_student_from_selection)
        actions_layout.addWidget(delete_btn)
        
        actions_layout.addStretch()
        
        # Export buttons
        export_excel_btn = QPushButton("📊 Export Excel")
        export_excel_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        export_excel_btn.clicked.connect(self.export_to_excel)
        actions_layout.addWidget(export_excel_btn)
        
        export_pdf_btn = QPushButton("📄 Export PDF")
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        actions_layout.addWidget(export_pdf_btn)
        
        # Transcript
        transcript_btn = QPushButton("📜 Transcript")
        transcript_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        transcript_btn.clicked.connect(self.export_transcript)
        actions_layout.addWidget(transcript_btn)
        
        # Import
        import_btn = QPushButton("📁 Import")
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        import_btn.clicked.connect(self.import_students)
        actions_layout.addWidget(import_btn)
        
        # Refresh
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #64748B;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        refresh_btn.clicked.connect(self.load_students)
        actions_layout.addWidget(refresh_btn)
        
        layout.addLayout(actions_layout)
    
    def create_table(self, layout):
        """Create the student table with sortable headers"""
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Roll Number", "Name", "Department", "Semester", "Gender",
            "DOB", "Phone", "Email", "Father Name", "CNIC"
        ])
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        
        # Styling
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                gridline-color: #F3F4F6;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F3F4F6;
            }
            QTableWidget::item:selected {
                background-color: #DBEAFE;
                color: #1E40AF;
            }
            QTableWidget::item:hover {
                background-color: #F0F9FF;
            }
            QHeaderView::section {
                background-color: #F8FAFC;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                font-weight: bold;
                color: #374151;
            }
            QHeaderView::section:hover {
                background-color: #E5E7EB;
            }
        """)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Roll
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Dept
        
        layout.addWidget(self.table)
    
    def create_pagination_section(self, layout):
        """Create pagination controls"""
        pagination_frame = QFrame()
        pagination_frame.setStyleSheet("""
            QFrame {
                background-color: #F8FAFC;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        pagination_layout = QHBoxLayout(pagination_frame)
        pagination_layout.setContentsMargins(16, 8, 16, 8)
        
        # Rows per page
        pagination_layout.addWidget(QLabel("Rows per page:"))
        self.rows_per_page_combo = QComboBox()
        self.rows_per_page_combo.addItems(["25", "50", "100", "200"])
        self.rows_per_page_combo.currentTextChanged.connect(self.on_rows_per_page_changed)
        pagination_layout.addWidget(self.rows_per_page_combo)
        
        pagination_layout.addStretch()
        
        # Page info
        self.page_info_label = QLabel("Page 1 of 1")
        self.page_info_label.setStyleSheet("font-weight: bold; color: #374151;")
        pagination_layout.addWidget(self.page_info_label)
        
        pagination_layout.addStretch()
        
        # Navigation buttons
        self.first_page_btn = QPushButton("⏮️ First")
        self.first_page_btn.setStyleSheet(self.get_pagination_btn_style())
        self.first_page_btn.clicked.connect(lambda: self.go_to_page(1))
        pagination_layout.addWidget(self.first_page_btn)
        
        self.prev_page_btn = QPushButton("◀️ Prev")
        self.prev_page_btn.setStyleSheet(self.get_pagination_btn_style())
        self.prev_page_btn.clicked.connect(lambda: self.go_to_page(self.current_page - 1))
        pagination_layout.addWidget(self.prev_page_btn)
        
        # Page input
        self.page_input = QSpinBox()
        self.page_input.setMinimum(1)
        self.page_input.setMaximum(1)
        self.page_input.setStyleSheet("padding: 4px 8px; min-width: 60px;")
        self.page_input.valueChanged.connect(self.on_page_input_changed)
        pagination_layout.addWidget(self.page_input)
        
        self.next_page_btn = QPushButton("Next ▶️")
        self.next_page_btn.setStyleSheet(self.get_pagination_btn_style())
        self.next_page_btn.clicked.connect(lambda: self.go_to_page(self.current_page + 1))
        pagination_layout.addWidget(self.next_page_btn)
        
        self.last_page_btn = QPushButton("Last ⏭️")
        self.last_page_btn.setStyleSheet(self.get_pagination_btn_style())
        self.last_page_btn.clicked.connect(lambda: self.go_to_page(self.total_pages))
        pagination_layout.addWidget(self.last_page_btn)
        
        layout.addWidget(pagination_frame)
    
    def get_pagination_btn_style(self):
        return """
            QPushButton {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 6px 12px;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
                border-color: #9CA3AF;
            }
            QPushButton:disabled {
                background-color: #F9FAFB;
                color: #D1D5DB;
            }
        """
    
    # ========== DATA LOADING ==========
    
    def load_students(self):
        """Load all students (async)"""
        self.loading_label.setText("⏳ Loading...")
        
        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.terminate()
            self.loader_thread.wait()
        
        dept_id = self.dept_filter.currentData() if hasattr(self, 'dept_filter') else self.department_id
        
        self.loader_thread = StudentLoaderThread(dept_id)
        self.loader_thread.finished.connect(self._on_students_loaded)
        self.loader_thread.error.connect(self._on_load_error)
        self.loader_thread.start()
    
    def _on_students_loaded(self, students):
        """Handle async load completion"""
        self.loading_label.setText("")
        self.all_students = students
        self.all_students = students
        self.apply_filters()
    
    def _on_load_error(self, error):
        """Handle async load error"""
        self.loading_label.setText("❌ Error")
        print(f"Load error: {error}")
    
    def apply_filters(self):
        """Apply all filters and refresh display"""
        students = self.all_students.copy()
        
        # Department filter
        dept_id = self.dept_filter.currentData()
        if dept_id:
            students = [s for s in students if s.get('department_id') == dept_id]
        
        # Semester filter
        semester = self.sem_filter.currentData()
        if semester and semester > 0:
            students = [s for s in students if s.get('semester') == semester]
        
        # Gender filter
        gender = self.gender_filter.currentText()
        if gender != "All":
            students = [s for s in students if s.get('gender') == gender]
        
        # Search filter
        search_term = self.search_input.text().strip().lower()
        if search_term:
            students = [s for s in students if 
                        search_term in s.get('name', '').lower() or
                        search_term in s.get('roll_number', '').lower() or
                        search_term in (s.get('email', '') or '').lower()]
        
        self.filtered_students = students
        self.current_page = 1
        self.update_pagination()
        self.display_current_page()
    
    def search_students(self):
        """Debounced search"""
        self.search_timer.stop()
        self.search_timer.start(300)
    
    def _do_search(self):
        """Execute search after debounce"""
        self.apply_filters()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_input.clear()
        self.dept_filter.setCurrentIndex(0)
        self.sem_filter.setCurrentIndex(0)
        self.gender_filter.setCurrentIndex(0)
        self.apply_filters()
    
    # ========== PAGINATION ==========
    
    def update_pagination(self):
        """Update pagination state"""
        rows_per_page = int(self.rows_per_page_combo.currentText())
        total_students = len(self.filtered_students)
        self.total_pages = max(1, (total_students + rows_per_page - 1) // rows_per_page)
        
        self.page_input.setMaximum(self.total_pages)
        self.page_input.setValue(self.current_page)
        
        self.page_info_label.setText(f"Page {self.current_page} of {self.total_pages} ({total_students} students)")
        
        # Update button states
        self.first_page_btn.setEnabled(self.current_page > 1)
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
        self.last_page_btn.setEnabled(self.current_page < self.total_pages)
    
    def go_to_page(self, page):
        """Go to a specific page"""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.update_pagination()
            self.display_current_page()
    
    def on_page_input_changed(self, value):
        """Handle page input change"""
        self.go_to_page(value)
    
    def on_rows_per_page_changed(self):
        """Handle rows per page change"""
        self.current_page = 1
        self.update_pagination()
        self.display_current_page()
    
    def on_header_clicked(self, logical_index):
        """Handle column header click for sorting"""
        if self.sort_column == logical_index:
            self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        else:
            self.sort_column = logical_index
            self.sort_order = Qt.AscendingOrder
        
        self.sort_students()
        self.display_current_page()
    
    def sort_students(self):
        """Sort filtered students by current column"""
        column_keys = ['roll_number', 'name', 'department_name', 'semester', 'gender',
                       'date_of_birth', 'phone', 'email', 'father_name', 'cnic']
        
        if 0 <= self.sort_column < len(column_keys):
            key = column_keys[self.sort_column]
            reverse = self.sort_order == Qt.DescendingOrder
            self.filtered_students.sort(key=lambda x: str(x.get(key, '') or '').lower(), reverse=reverse)
    
    # ========== DISPLAY ==========
    
    def display_current_page(self):
        """Display current page of students"""
        rows_per_page = int(self.rows_per_page_combo.currentText())
        start_idx = (self.current_page - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        
        self.students_data = self.filtered_students[start_idx:end_idx]
        
        self.table.setUpdatesEnabled(False)
        self.table.setSortingEnabled(False)
        self.table.clearContents()
        self.table.setRowCount(len(self.students_data))
        
        for row, student in enumerate(self.students_data):
            self.table.setItem(row, 0, QTableWidgetItem(student.get('roll_number', '')))
            self.table.setItem(row, 1, QTableWidgetItem(student.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(student.get('department_name', '') or ''))
            self.table.setItem(row, 3, QTableWidgetItem(str(student.get('semester', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(student.get('gender', '') or ''))
            
            dob = student.get('date_of_birth', '')
            self.table.setItem(row, 5, QTableWidgetItem(str(dob) if dob else ''))
            
            self.table.setItem(row, 6, QTableWidgetItem(student.get('phone', '') or ''))
            self.table.setItem(row, 7, QTableWidgetItem(student.get('email', '') or ''))
            self.table.setItem(row, 8, QTableWidgetItem(student.get('father_name', '') or ''))
            self.table.setItem(row, 9, QTableWidgetItem(student.get('cnic', '') or ''))
            
            # Row highlighting based on gender
            if student.get('gender') == 'Male':
                for col in range(10):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QBrush(QColor("#F0F9FF")))
            elif student.get('gender') == 'Female':
                for col in range(10):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QBrush(QColor("#FDF2F8")))
        
        self.table.setSortingEnabled(True)
        self.table.setUpdatesEnabled(True)
    
    # stats update logic removed
    
    # ========== ACTIONS ==========
    
    def add_student(self):
        """Open add student dialog"""
        dialog = StudentDialog(self)
        if dialog.exec_():
            self.load_students()
    
    def edit_student_from_selection(self):
        """Edit selected student"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a student to edit")
            return
        
        if len(selected_rows) > 1:
            QMessageBox.warning(self, "Multiple Selection", "Please select only one student to edit")
            return
        
        row = selected_rows[0].row()
        if row < 0 or row >= len(self.students_data):
            return
        
        student = self.students_data[row]
        dialog = StudentDialog(self, student)
        if dialog.exec_():
            self.load_students()
    
    def delete_student_from_selection(self):
        """Delete selected student(s)"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select student(s) to delete")
            return
        
        count = len(selected_rows)
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Delete {count} student(s)?\n\nThis will also delete all related marks and results.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success_count = 0
            for index in selected_rows:
                row = index.row()
                if 0 <= row < len(self.students_data):
                    student = self.students_data[row]
                    success, _ = student_controller.delete_student(student['student_id'])
                    if success:
                        success_count += 1
            
            QMessageBox.information(self, "Success", f"Deleted {success_count} student(s)")
            self.load_students()
    
    def export_to_excel(self):
        """Export filtered students to Excel"""
        if not self.filtered_students:
            QMessageBox.warning(self, "No Data", "No students to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "students.xlsx", "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                import pandas as pd
                df = pd.DataFrame(self.filtered_students)
                columns_to_export = ['roll_number', 'name', 'department_name', 'semester',
                                      'gender', 'date_of_birth', 'phone', 'email', 'father_name', 'cnic']
                df = df[[c for c in columns_to_export if c in df.columns]]
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"Exported {len(self.filtered_students)} students to Excel")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def export_to_pdf(self):
        """Export filtered students to PDF"""
        if not self.filtered_students:
            QMessageBox.warning(self, "No Data", "No students to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF File", "students.pdf", "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import A4, landscape
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
                from reportlab.lib.styles import getSampleStyleSheet
                
                doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
                elements = []
                
                styles = getSampleStyleSheet()
                elements.append(Paragraph("Student List", styles['Title']))
                
                # Table data
                data = [['Roll No', 'Name', 'Department', 'Semester', 'Gender', 'Phone']]
                for s in self.filtered_students[:200]:  # Limit to 200 for PDF
                    data.append([
                        s.get('roll_number', ''),
                        s.get('name', ''),
                        s.get('department_name', '') or '',
                        str(s.get('semester', '')),
                        s.get('gender', '') or '',
                        s.get('phone', '') or ''
                    ])
                
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
                ]))
                elements.append(table)
                
                doc.build(elements)
                QMessageBox.information(self, "Success", f"Exported to PDF (max 200 rows)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def export_transcript(self):
        """Export transcript for selected student"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a student")
            return
        
        row = selected_rows[0].row()
        if 0 <= row < len(self.students_data):
            student = self.students_data[row]
            from ui.transcript_export import TranscriptExportDialog
            dialog = TranscriptExportDialog(student['student_id'], student['name'], self)
            dialog.exec_()
    
    def import_students(self):
        """Import students from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            success, msg, count = student_controller.bulk_import_students(file_path)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.load_students()
            else:
                QMessageBox.warning(self, "Error", msg)


class StudentDialog(QDialog):
    """Dialog for adding/editing students"""
    
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()
        if student:
            self.load_student_data()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Edit Student" if self.student else "Add Student")
        self.setFixedSize(600, 650)
        
        layout = QFormLayout(self)
        
        self.roll_input = QLineEdit()
        layout.addRow("Roll Number:*", self.roll_input)
        
        self.name_input = QLineEdit()
        layout.addRow("Name:*", self.name_input)
        
        self.registration_input = QLineEdit()
        layout.addRow("Registration No:", self.registration_input)
        
        self.dept_combo = QComboBox()
        departments = department_controller.get_all_departments() or []
        for dept in departments:
            self.dept_combo.addItem(dept['department_name'], dept['department_id'])
        layout.addRow("Department:*", self.dept_combo)
        
        self.semester_combo = QComboBox()
        for i in range(1, 9):
            self.semester_combo.addItem(f"Semester {i}", i)
        layout.addRow("Semester:*", self.semester_combo)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        layout.addRow("Gender:*", self.gender_combo)
        
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate().addYears(-18))
        layout.addRow("Date of Birth:*", self.dob_input)
        
        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("03XX-XXXXXXX")
        layout.addRow("Phone:", self.phone_input)
        
        self.guardian_phone_input = QLineEdit()
        layout.addRow("Guardian Phone:", self.guardian_phone_input)
        
        self.cnic_input = QLineEdit()
        self.cnic_input.setPlaceholderText("XXXXX-XXXXXXX-X")
        layout.addRow("CNIC:", self.cnic_input)
        
        self.father_name_input = QLineEdit()
        layout.addRow("Father Name:", self.father_name_input)
        
        self.father_cnic_input = QLineEdit()
        layout.addRow("Father CNIC:", self.father_cnic_input)
        
        self.address_input = QLineEdit()
        layout.addRow("Address:", self.address_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; padding: 8px 24px;")
        save_btn.clicked.connect(self.save_student)
        btn_layout.addWidget(save_btn)
        
        layout.addRow("", btn_layout)
    
    def load_student_data(self):
        """Load student data into form"""
        self.roll_input.setText(self.student.get('roll_number', ''))
        self.name_input.setText(self.student.get('name', ''))
        
        for i in range(self.dept_combo.count()):
            if self.dept_combo.itemData(i) == self.student.get('department_id'):
                self.dept_combo.setCurrentIndex(i)
                break
        
        semester = self.student.get('semester', 1)
        if semester:
            self.semester_combo.setCurrentIndex(semester - 1)
        
        gender = self.student.get('gender', 'Male')
        index = self.gender_combo.findText(gender)
        if index >= 0:
            self.gender_combo.setCurrentIndex(index)
        
        dob = self.student.get('date_of_birth')
        if dob:
            date = QDate.fromString(str(dob), "yyyy-MM-dd")
            if date.isValid():
                self.dob_input.setDate(date)
        
        self.father_name_input.setText(self.student.get('father_name', '') or '')
        self.cnic_input.setText(self.student.get('cnic', '') or '')
        self.phone_input.setText(self.student.get('phone', '') or '')
        self.email_input.setText(self.student.get('email', '') or '')
        self.address_input.setText(self.student.get('address', '') or '')
        self.father_cnic_input.setText(self.student.get('father_cnic', '') or '')
        self.guardian_phone_input.setText(self.student.get('guardian_phone', '') or '')
        self.registration_input.setText(self.student.get('registration_no', '') or '')
    
    def save_student(self):
        """Save student data"""
        roll_number = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        department_id = self.dept_combo.currentData()
        semester = self.semester_combo.currentIndex() + 1
        
        if not roll_number or not name:
            QMessageBox.warning(self, "Validation Error", "Roll number and name are required!")
            return
        
        if not department_id:
            QMessageBox.warning(self, "Validation Error", "Please select a department!")
            return
        
        student_data = {
            'roll_number': roll_number,
            'name': name,
            'father_name': self.father_name_input.text().strip(),
            'department_id': department_id,
            'semester': semester,
            'gender': self.gender_combo.currentText(),
            'date_of_birth': self.dob_input.date().toString("yyyy-MM-dd"),
            'cnic': self.cnic_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip(),
            'address': self.address_input.text().strip(),
            'father_cnic': self.father_cnic_input.text().strip(),
            'guardian_phone': self.guardian_phone_input.text().strip(),
            'registration_no': self.registration_input.text().strip()
        }
        
        try:
            if self.student:
                success, msg = student_controller.update_student(
                    student_id=self.student['student_id'],
                    **student_data
                )
            else:
                success, msg, _ = student_controller.create_student(**student_data)
            
            if success:
                QMessageBox.information(self, "Success", msg)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
