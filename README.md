- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [User Roles](#-user-roles)
- [Core Modules](#-core-modules)
- [Database](#-database)
- [Backup & Recovery](#-backup--recovery)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Support](#-support)

---

## ✨ Features

### 🎓 Student Management
- **Complete Student Profiles** - Roll number, name, father's name, CNIC, contact details
- **Department Assignment** - Link students to departments and semesters
- **Advanced Search & Filtering** - Search by name, roll number, department, semester
- **Bulk Import** - Import students from CSV/Excel files
- **Student Records** - Track gender, date of birth, address, guardian information

### 📚 Course Management
- **Course Creation** - Define courses with codes, names, credits
- **Department-wise Organization** - Assign courses to departments and semesters
- **Marks Configuration** - Set maximum marks and pass marks per course
- **Course Filtering** - Filter by department, semester, status

### 📊 Department Management
- **Department Setup** - Create departments with unique codes
- **Student Statistics** - View student count per department
- **Gender Distribution** - Track male/female student ratios
- **Department Reports** - Generate department-wise analytics

### 📝 Marks Entry
- **Intuitive Interface** - Easy marks entry with validation
- **Real-time Grade Calculation** - Automatic grade assignment based on marks
- **Pass/Fail Status** - Automatic status determination
- **Bulk Entry** - Enter marks for multiple students efficiently
- **Edit & Update** - Modify marks with full audit trail

### 📈 Result Generation
- **Semester Results** - Generate results for individual semesters
- **CGPA Calculation** - Cumulative GPA across all semesters
- **SGPA Calculation** - Semester-wise GPA
- **Overall Grading** - A+, A, B+, B, C+, C, F grades
- **Percentage Calculation** - Total percentage and marks obtained
- **Class Ranking** - Automatic rank assignment based on CGPA

### 📄 Transcript Export
- **Professional PDF Transcripts** - University-branded transcripts
- **Complete Academic Record** - All semesters with grades and GPA
- **Custom Watermark** - University logo watermark (15% opacity, 140% scale)
- **Digital Signature** - Assistant Director Examination signature
- **Custom Fonts** - Bookman Old Style, Goudy Old Style, Times New Roman

### 👥 User Management
- **Role-based Access** - Admin, Teacher, Student roles
- **User Authentication** - Secure login with password hashing (bcrypt)
- **Permission Control** - Different features for different roles
- **User Profiles** - Manage user information and credentials

### 📊 Dashboard & Reports
- **Visual Analytics** - Charts for student distribution, performance trends
- **Department Statistics** - Student counts, gender ratios
- **Performance Metrics** - Pass/fail rates, average GPA
- **Quick Actions** - Fast access to common tasks
- **OS:** Windows 7/8/10/11, macOS 10.12+, Linux (Ubuntu 18.04+)
- **Python:** 3.8 or higher
- **RAM:** 2 GB
- **Storage:** 500 MB free space
- **Display:** 1280x720 resolution

### Recommended Requirements
- **OS:** Windows 10/11
- **Python:** 3.10 or higher
- **RAM:** 4 GB or more
- **Storage:** 1 GB free space
- **Display:** 1920x1080 resolution

---

## 📥 Installation

### Step 1: Install Python
Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)

### Step 2: Clone or Download
```bash
git clone https://github.com/yourusername/university-exam-system.git
cd university-exam-system
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages:**
- PyQt5 (5.15.9) - GUI framework
- bcrypt (4.1.2) - Password hashing
- reportlab (4.0.7) - PDF generation
- pandas (2.1.4) - Data processing
- openpyxl (3.1.2) - Excel support
- Pillow (10.1.0) - Image processing
- matplotlib (3.8.2) - Charts and graphs
- schedule (1.2.0) - Automatic backups

### Step 4: Run Application
```bash
python main.py
```

---

## 🚀 Quick Start

### First Login
1. Run `python main.py`
2. Login with default credentials:
   - **Username:** `admin`
   - **Password:** `admin123`
3. **⚠️ Change password immediately after first login!**

### Basic Workflow
1. **Setup Departments** - Create departments (e.g., Computer Science, Mathematics)
2. **Add Courses** - Define courses for each department and semester
3. **Register Students** - Add student information
4. **Enter Marks** - Input marks for students in their courses
5. **Generate Results** - Calculate GPA and generate semester results
6. **Export Transcripts** - Create PDF transcripts for students

---

## 👥 User Roles
- View results and reports
- Export transcripts
- Limited user management

### 🟢 Student
**Personal Records**
- View own profile
- View own marks and results
- Download own transcript
- View course information

---

## 🗂️ Core Modules

### 1. Student Management (`ui/student_management.py`)
**Features:**
- Add/Edit/Delete students
- Search and filter students
- Import from CSV/Excel
- View student details
- Export student lists

**Fields:**
- Roll Number, Name, Father's Name
- Department, Semester, Gender
- Date of Birth, CNIC, Father's CNIC
- Phone, Email, Guardian Phone
- Address, Registration Number

### 2. Course Management (`ui/course_management.py`)
**Features:**
- Create courses with codes
- Set credits and marks
- Assign to departments/semesters
- Activate/deactivate courses
- Course filtering

**Fields:**
- Course Code, Course Name
- Department, Semester
- Credits, Max Marks, Pass Marks

### 3. Marks Entry (`ui/marks_entry.py`)
**Features:**
- Department/semester filtering
- Student and course selection
- Real-time grade calculation
- Validation and error checking
- Edit existing marks

**Grading Scale (4.0 GPA):**
- A+: 90-100% (4.0 points)
- A: 80-89% (4.0 points)
- B+: 70-79% (3.5 points)
- B: 60-69% (3.0 points)
- C+: 50-59% (2.5 points)
- C: 40-49% (2.0 points)
- F: 0-39% (0.0 points)

### 4. Result Generation (`ui/result_generation.py`)
**Features:**
- Semester-wise results
- CGPA and SGPA calculation
- Overall grade assignment
- Class ranking
- Result export to PDF/Excel

**Calculations:**
- SGPA = Σ(Grade Points × Credits) / Σ Credits
- CGPA = Average of all semester SGPAs
- Percentage = (Marks Obtained / Total Marks) × 100

### 5. Transcript Export (`ui/transcript_export.py`)
**Features:**
- Professional PDF format
- University branding
- Watermark support
- Custom fonts and styling
- Digital signature

**Transcript Contents:**
- Student information
- Department details
- Semester-wise courses and grades
- SGPA and CGPA
- Overall grade and status
- Official signature

### 6. Dashboard (`ui/dashboard.py`)
**Features:**
- Student statistics
- Department distribution charts
- Performance analytics
- Quick action buttons
- Recent activity

---

## 🗄️ Database

### Database Type
**SQLite 3** - Lightweight, serverless, zero-configuration

### Database Location
`data/exam_system.db`

### Enhanced Features
- **WAL Mode** - Write-Ahead Logging for better concurrency
- **Foreign Keys** - Enforced referential integrity
- **Transactions** - ACID compliance
- **Indexes** - Optimized query performance
- **30-second Timeouts** - Prevents "database locked" errors

### Database Schema

#### Tables

**1. departments**
- `department_id` (Primary Key)
- `department_name` (Unique)
- `department_code` (Unique)
- `created_at`, `is_active`

**2. students**
- `student_id` (Primary Key)
- `roll_number` (Unique)
- `name`, `father_name`
- `department_id` (Foreign Key)
- `semester`, `gender`, `date_of_birth`
- `cnic`, `father_cnic`
- `phone`, `email`, `guardian_phone`
- `address`, `registration_no`
- `created_at`, `is_active`

**3. courses**
- `course_id` (Primary Key)
- `course_code` (Unique)
- `course_name`
- `department_id` (Foreign Key)
- `semester`, `credits`
- `max_marks`, `pass_marks`
- `created_at`, `is_active`

**4. marks**
- `mark_id` (Primary Key)
- `student_id` (Foreign Key)
- `course_id` (Foreign Key)
- `marks_obtained`, `grade`, `status`
- `entered_by` (Foreign Key to users)
- `entered_at`, `updated_at`

**5. results**
- `result_id` (Primary Key)
- `student_id` (Foreign Key)
- `semester`
- `total_marks`, `marks_obtained`, `percentage`
- `sgpa`, `cgpa`, `overall_grade`
- `status`, `rank`
- `generated_at`

**6. users**
- `user_id` (Primary Key)
- `username` (Unique)
- `password_hash`
- `role` (Admin/Teacher/Student)
- `full_name`, `email`
- `created_at`, `is_active`

### Database Migrations
Run migrations for schema updates:
```bash
python database/migrate_student_fields.py
```

---

## 💾 Backup & Recovery

### Automatic Backups

**Hourly Backups**
- Runs every hour automatically
- Keeps last 24 backups
- Location: `backups/exam_system_backup_YYYYMMDD_HHMMSS.db`

**Daily Backups**
- Runs at 2:00 AM daily
- Kept separately for long-term storage
- Location: `backups/daily/exam_system_daily_YYYYMMDD.db`

### Manual Backup
1. Go to **Backup & Restore** menu
2. Click **Create Backup**
3. Choose save location
4. Backup file created with timestamp

### Restore from Backup
1. Go to **Backup & Restore** menu
2. Click **Restore Backup**
3. Select backup file
4. Confirm restoration
5. Application restarts with restored data

### Backup Service
Automatic backup service starts on application launch:
- Background thread (non-blocking)
- Progress notifications
- Integrity verification
- Auto-cleanup of old backups

---

## 📸 Screenshots

### Login Screen
Professional login interface with role-based authentication

### Admin Dashboard
Visual analytics with charts and quick actions

### Student Management
Comprehensive student records with search and filtering

### Marks Entry
Intuitive interface for entering and managing marks

### Result Generation
Automated result calculation with GPA and ranking

### Transcript Export
Professional PDF transcripts with university branding

---

## 🔧 Troubleshooting

### Database Locked Error
**Solution:** WAL mode is now enabled automatically. If issues persist:
```python
# Check WAL mode
sqlite3 data/exam_system.db "PRAGMA journal_mode;"
# Should return: wal
```

### Import Errors
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Backup Service Not Starting
**Solution:** Install schedule library:
```bash
pip install schedule
```

### PDF Generation Fails
**Solution:** Ensure reportlab and Pillow are installed:
```bash
pip install reportlab Pillow
```

### Font Issues in Transcript
**Solution:** Fonts are loaded from Windows fonts directory. Ensure:
- Bookman Old Style
- Goudy Old Style
- Times New Roman

are installed on your system.

---

## 📝 Configuration

### Database Path
Edit `config.py`:
```python
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'exam_system.db')
```

### Backup Directory
```python
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
```

### Grading Scale
Modify in `config.py`:
```python
GRADING_SCALE = {
    'A+': {'min': 90, 'max': 100, 'points': 4.0},
    # ... customize as needed
}
```

### Session Timeout
```python
SESSION_TIMEOUT_MINUTES = 30
```

---

## 🐛 Known Issues

1. **Large Datasets** - Performance may degrade with 10,000+ students
   - **Solution:** Consider MySQL migration for very large institutions

2. **Concurrent Access** - Limited to ~50-200 concurrent users
   - **Solution:** WAL mode improves this significantly

---

## 🤝 Support

### Documentation
- User Guide: `USER_GUIDE.md`
- Build Instructions: `BUILD_INSTRUCTIONS.md`
- API Documentation: `docs/api.md`

### Logs
- Database Logs: `database/logs/database_YYYYMMDD.log`
- Application Logs: Check console output

### Contact
For issues, questions, or feature requests:
- Email: support@university.edu
- GitHub Issues: [Create an issue](https://github.com/yourusername/university-exam-system/issues)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- PyQt5 for the excellent GUI framework
- ReportLab for PDF generation
- SQLite for the reliable database engine
- University of Balochistan for requirements and testing

---

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Complete student, course, and marks management
- Result generation with GPA calculation
- Professional transcript export
- Automatic backup system
- WAL mode for database reliability
- Role-based access control

---

**Made for University of Balochistan**
**Developed By Shayak Siraj**