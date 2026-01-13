# 📚 University Exam System - Complete Documentation
## From Installation to Advanced Usage

---

## 📋 Table of Contents

1. [System Overview](#1-system-overview)
2. [Installation Guide](#2-installation-guide)
3. [Database Configuration](#3-database-configuration)
4. [First Time Setup](#4-first-time-setup)
5. [User Roles & Permissions](#5-user-roles--permissions)
6. [Core Features](#6-core-features)
7. [Step-by-Step Usage Guide](#7-step-by-step-usage-guide)
8. [Advanced Features](#8-advanced-features)
9. [Reports & Analytics](#9-reports--analytics)
10. [Backup & Recovery](#10-backup--recovery)
11. [Troubleshooting](#11-troubleshooting)
12. [Technical Reference](#12-technical-reference)
13. [FAQ](#13-faq)

---

## 1. System Overview

### 1.1 What is This System?

The **University Exam Result Management System** is a comprehensive desktop application designed to manage all aspects of university examination processes, including:

- Student enrollment and management
- Course and department administration
- Marks entry and grade calculation
- Result generation with CGPA/SGPA
- Professional transcript generation
- Advanced analytics and reporting

### 1.2 Key Features

✅ **Complete Student Management** - Track student profiles, enrollment, and academic records  
✅ **Department & Course Management** - Organize academic structure  
✅ **Marks Entry System** - Efficient marks entry with validation  
✅ **Automated Result Generation** - Calculate GPA, grades, and rankings  
✅ **Professional Transcripts** - Generate PDF transcripts with watermarks  
✅ **Role-Based Access Control** - Admin, Teacher, and Student roles  
✅ **Analytics Dashboard** - Visual insights and statistics  
✅ **Automatic Backups** - Hourly and daily backup system  
✅ **Multi-Database Support** - SQLite and MySQL/TiDB Cloud  

### 1.3 System Requirements

#### Minimum Requirements
- **OS:** Windows 7/8/10/11, macOS 10.12+, or Linux (Ubuntu 18.04+)
- **Python:** 3.8 or higher
- **RAM:** 2 GB
- **Storage:** 500 MB free space
- **Display:** 1280x720 resolution

#### Recommended Requirements
- **OS:** Windows 10/11
- **Python:** 3.10 or higher
- **RAM:** 4 GB or more
- **Storage:** 1 GB free space
- **Display:** 1920x1080 resolution

---

## 2. Installation Guide

### 2.1 Option A: Running from Source (Developers)

#### Step 1: Install Python
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

#### Step 2: Download the Project
```bash
# Clone from Git (if available)
git clone https://github.com/yourusername/university-exam-system.git
cd university-exam-system

# OR extract from ZIP file
# Extract to: d:\New folder\New folder (2)\university_exam_system
```

#### Step 3: Install Dependencies
```bash
cd "d:\New folder\New folder (2)\university_exam_system"
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
- pymysql (1.1.0) - MySQL database support

#### Step 4: Run the Application
```bash
python main.py
```

### 2.2 Option B: Running the Executable (End Users)

#### Step 1: Extract the Application
1. Extract `University Examination managing System.zip`
2. Navigate to the `Release` folder
3. You'll find `UniversityExamSystem.exe`

#### Step 2: Run the Application
1. Double-click `UniversityExamSystem.exe`
2. If Windows Defender blocks it:
   - Click "More info"
   - Click "Run anyway"
3. The application will start automatically

> **Note:** The executable is self-contained and doesn't require Python installation.

### 2.3 Building Your Own Executable

If you want to create your own executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller UniversityExamSystem.spec

# Or use the build script
.\build_exe.ps1
```

The executable will be created in the `dist/` folder.

---

## 3. Database Configuration

### 3.1 Database Options

The system supports two database backends:

1. **SQLite** (Default) - File-based, no setup required
2. **MySQL/TiDB Cloud** - For multi-user environments

### 3.2 SQLite Configuration (Default)

**No configuration needed!** The system automatically creates `exam_system.db` in the application folder.

**Features:**
- ✅ Zero configuration
- ✅ Portable (single file)
- ✅ Perfect for single-user or small deployments
- ⚠️ Limited concurrent access (1-5 users)

**Location:** `exam_system.db` (in application folder)

### 3.3 MySQL/TiDB Cloud Configuration

For multi-user environments or cloud deployment:

#### Step 1: Edit config.json
```json
{
    "use": "mysql",
    "mysql_host": "your-database-host.com",
    "mysql_port": 4000,
    "mysql_user": "your_username",
    "mysql_password": "your_password",
    "mysql_database": "test"
}
```

#### Step 2: Initialize MySQL Schema
```bash
python init_mysql_schema.py
```

#### Step 3: Verify Connection
```bash
python test_mysql_connection.py
```

**TiDB Cloud Setup:**
1. Create account at [tidbcloud.com](https://tidbcloud.com)
2. Create a new cluster
3. Get connection details
4. Update `config.json` with your credentials

---

## 4. First Time Setup

### 4.1 Initial Login

When you first run the application, you'll see the login screen.

**Default Administrator Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ **CRITICAL:** Change this password immediately after first login!

### 4.2 Changing the Default Password

1. Login with default credentials
2. Click on **"My Profile"** in the menu
3. Click **"Change Password"**
4. Enter:
   - Current Password: `admin123`
   - New Password: (your secure password)
   - Confirm Password: (repeat new password)
5. Click **"Save"**

### 4.3 Initial Configuration Workflow

Follow these steps to set up your university:

```
1. Configure University Information
   ↓
2. Create Departments
   ↓
3. Add Courses
   ↓
4. Create User Accounts (Teachers, Data Entry)
   ↓
5. Add Students
   ↓
6. Start Using the System!
```

#### Step 1: Configure University Information

Edit `config.py` (lines 11-15):
```python
UNIVERSITY_NAME = "University of Balochistan"  # ← Change this!
UNIVERSITY_ADDRESS = "Sariab Road, Quetta"
UNIVERSITY_PHONE = "+92 (XXX) XXX-XXXX"
UNIVERSITY_EMAIL = "info@uob.edu.pk"
```

#### Step 2: Create Departments

1. Go to **Department Management** tab
2. Click **"+ Add Department"**
3. Fill in:
   - **Department Code:** e.g., "CS", "MATH", "PHY"
   - **Department Name:** e.g., "Computer Science"
   - **Head of Department:** (optional)
4. Click **"Save"**

**Example Departments:**
- CS - Computer Science
- MATH - Mathematics
- PHY - Physics
- CHEM - Chemistry
- ENG - English

#### Step 3: Add Courses

1. Go to **Course Management** tab
2. Click **"+ Add Course"**
3. Fill in:
   - **Course Code:** e.g., "CS101"
   - **Course Name:** e.g., "Introduction to Programming"
   - **Department:** Select from dropdown
   - **Semester:** 1-8
   - **Credits:** e.g., 3
   - **Max Marks:** e.g., 100
   - **Pass Marks:** e.g., 50
4. Click **"Save"**

#### Step 4: Create User Accounts

1. Go to **User Management** tab
2. Click **"+ Add User"**
3. Fill in:
   - **Username:** unique username
   - **Password:** secure password
   - **Role:** Admin / Teacher / Student
   - **Full Name:** user's full name
   - **Email:** user's email
4. Click **"Save"**

**User Roles:**
- **Admin:** Full system access
- **Teacher:** Department-specific access
- **Student:** Personal records only

#### Step 5: Add Students

**Option A: Manual Entry**
1. Go to **Student Management** tab
2. Click **"+ Add Student"**
3. Fill in all required fields (marked with *)
4. Click **"Save"**

**Option B: Bulk Import (Recommended)**
1. Prepare CSV/Excel file with columns:
   - roll_number, name, father_name, department, semester, gender, etc.
2. Go to **Student Management** tab
3. Click **"📁 Import CSV/Excel"**
4. Select your file
5. Click **"Open"**
6. Review and confirm import

---

## 5. User Roles & Permissions

### 5.1 Administrator

**Full System Access:**

✅ **User Management**
- Create, edit, delete users
- Assign roles and permissions
- Reset passwords

✅ **Department Management**
- Create and manage departments
- Assign department heads

✅ **Course Management**
- Add, edit, delete courses
- Configure credits and marks

✅ **Student Management**
- Full access to all student records
- Import/export students
- Multi-select operations

✅ **Marks Entry**
- Enter marks for any course
- Edit existing marks
- Bulk marks entry

✅ **Result Generation**
- Generate results for any student
- Calculate CGPA/SGPA
- Assign rankings

✅ **Reports & Analytics**
- Access all reports
- Export to Excel/PDF
- View system-wide statistics

✅ **System Administration**
- Backup and restore
- System configuration
- Audit logs

### 5.2 Teacher

**Department-Specific Access:**

✅ **View Students**
- View students in assigned department only
- Search and filter students

✅ **Marks Entry**
- Enter marks for assigned courses
- Edit marks for own courses

✅ **Result Generation**
- Generate results for own students
- View department statistics

✅ **Reports**
- View department-specific reports
- Export student lists

❌ **Cannot:**
- Access other departments
- Manage users
- System configuration

### 5.3 Student

**Personal Access Only:**

✅ **View Profile**
- View own student information
- View enrollment details

✅ **View Results**
- View own marks and grades
- View CGPA/SGPA
- View semester-wise results

✅ **Download Transcript**
- Generate own transcript
- Export to PDF

❌ **Cannot:**
- View other students' records
- Enter or edit marks
- Access administrative functions

---

## 6. Core Features

### 6.1 Student Management

#### Adding a Student

1. Navigate to **Student Management** tab
2. Click **"+ Add Student"** button
3. Fill in the form:

**Required Fields (*):**
- **Roll Number:** Unique identifier (e.g., "BSCS-01-21")
- **Name:** Student's full name
- **Father Name:** Father's full name
- **Department:** Select from dropdown
- **Semester:** 1-8
- **Gender:** Male/Female

**Optional Fields:**
- Registration Number
- CNIC (13 digits)
- Father's CNIC
- Date of Birth
- Phone (11 digits)
- Guardian Phone
- Email
- Address

4. Click **"Save"**

#### Editing a Student

1. Find the student in the table
2. Double-click the row OR select and click **"✏️ Edit"**
3. Modify the information
4. Click **"Save"**

#### Deleting Students

**Single Delete:**
1. Select the student
2. Click **"🗑️ Delete"**
3. Confirm deletion

**Multi-Select Delete:**
1. Hold `Ctrl` and click multiple students
2. OR press `Ctrl+A` to select all
3. Click **"🗑️ Delete Selected"**
4. Confirm deletion

#### Searching Students

Use the search box to find students by:
- Roll Number
- Name
- Father Name
- Department
- Semester

**Example:** Type "BSCS" to find all Computer Science students

#### Importing Students

1. Prepare CSV/Excel file with these columns:
   ```
   roll_number, name, father_name, department, semester, gender,
   registration_no, cnic, father_cnic, dob, phone, guardian_phone,
   email, address
   ```

2. Click **"📁 Import CSV/Excel"**
3. Select your file
4. Review the preview
5. Click **"Import"**

**Sample File:** See `sample_data/sample_students.csv`

#### Exporting Students

1. Click **"📤 Export"**
2. Choose format: Excel or CSV
3. Select save location
4. Click **"Save"**

### 6.2 Department Management

#### Creating a Department

1. Go to **Department Management** tab
2. Click **"+ Add Department"**
3. Fill in:
   - **Department Code:** 2-10 characters (e.g., "CS")
   - **Department Name:** Full name (e.g., "Computer Science")
   - **Head of Department:** (optional)
4. Click **"Save"**

#### Viewing Department Statistics

The department table shows:
- Department Code
- Department Name
- Total Students
- Male Students
- Female Students
- Head of Department

### 6.3 Course Management

#### Adding a Course

1. Go to **Course Management** tab
2. Click **"+ Add Course"**
3. Fill in:
   - **Course Code:** Unique (e.g., "CS101")
   - **Course Name:** Full name (e.g., "Programming Fundamentals")
   - **Department:** Select department
   - **Semester:** 1-8
   - **Credits:** Credit hours (e.g., 3)
   - **Max Marks:** Maximum marks (e.g., 100)
   - **Pass Marks:** Passing threshold (e.g., 50)
4. Click **"Save"**

#### Filtering Courses

Use filters to view:
- Courses by Department
- Courses by Semester
- Active/Inactive courses

#### Activating/Deactivating Courses

1. Select the course
2. Click **"Activate"** or **"Deactivate"**
3. Inactive courses won't appear in marks entry

### 6.4 Marks Entry

#### Entering Marks for a Student

1. Go to **Marks Entry** tab
2. **Select Filters:**
   - Department
   - Semester
3. **Select Student** from dropdown
4. **Select Course** from dropdown
5. **Enter Marks** (0 to max marks)
6. Click **"💾 Save Marks"**

**Automatic Calculations:**
- Grade is calculated automatically
- Pass/Fail status is determined
- Validation ensures marks don't exceed maximum

#### Editing Existing Marks

1. Select the same student and course
2. The existing marks will appear
3. Modify the marks
4. Click **"💾 Save Marks"**

#### Grade Calculation

The system automatically assigns grades based on percentage:

| Percentage | Grade | Grade Points |
|------------|-------|--------------|
| 90-100%    | A+    | 4.0          |
| 80-89%     | A     | 4.0          |
| 70-79%     | B+    | 3.5          |
| 60-69%     | B     | 3.0          |
| 50-59%     | C+    | 2.5          |
| 40-49%     | C     | 2.0          |
| 0-39%      | F     | 0.0          |

### 6.5 Result Generation

#### Generating a Student's Result

1. Go to **Result Generation** tab
2. **Select Student** from dropdown
3. **Select Semester** (or "All Semesters")
4. Click **"📊 Generate Result"**

**The system calculates:**
- Total Marks Obtained
- Total Marks
- Percentage
- SGPA (Semester GPA)
- CGPA (Cumulative GPA)
- Overall Grade
- Class Rank
- Pass/Fail Status

#### Understanding GPA Calculation

**SGPA (Semester GPA):**
```
SGPA = Σ(Grade Points × Credits) / Σ Credits
```

**Example:**
- CS101 (3 credits): A+ (4.0 points)
- MATH101 (3 credits): B+ (3.5 points)
- ENG101 (2 credits): A (4.0 points)

```
SGPA = (4.0×3 + 3.5×3 + 4.0×2) / (3+3+2)
     = (12 + 10.5 + 8) / 8
     = 30.5 / 8
     = 3.81
```

**CGPA (Cumulative GPA):**
```
CGPA = Average of all semester SGPAs
```

#### Exporting Results

After generating a result:
1. Click **"📄 Export to PDF"** for PDF report
2. OR click **"📊 Export to Excel"** for Excel spreadsheet

### 6.6 Transcript Export

#### Generating a Professional Transcript

1. Go to **Transcript Export** tab
2. **Select Student** from dropdown
3. Click **"📄 Generate Transcript"**
4. Choose save location
5. Click **"Save"**

**Transcript Features:**
- University branding and logo
- Student information
- Semester-wise course details
- Grades and GPA
- Watermark (15% opacity, 140% scale)
- Digital signature
- Professional fonts (Bookman Old Style, Goudy Old Style)

**Transcript Contents:**
- Student Name, Roll Number, Registration Number
- Department and Program
- Semester-wise courses with:
  - Course Code and Name
  - Credits
  - Marks Obtained
  - Grade
- SGPA for each semester
- Overall CGPA
- Overall Grade
- Official signature (Assistant Director Examination)

---

## 7. Step-by-Step Usage Guide

### 7.1 Complete Workflow: From Student Enrollment to Transcript

#### Scenario: Adding a new student and generating their transcript

**Step 1: Add the Student**
1. Go to **Student Management**
2. Click **"+ Add Student"**
3. Enter details:
   - Roll Number: BSCS-15-21
   - Name: Ahmed Khan
   - Father Name: Muhammad Khan
   - Department: Computer Science
   - Semester: 1
   - Gender: Male
4. Click **"Save"**

**Step 2: Ensure Courses Exist**
1. Go to **Course Management**
2. Verify courses for Semester 1 exist:
   - CS101 - Programming Fundamentals (3 credits)
   - MATH101 - Calculus I (3 credits)
   - ENG101 - English Composition (2 credits)

**Step 3: Enter Marks**
1. Go to **Marks Entry**
2. Select Department: Computer Science
3. Select Semester: 1
4. Select Student: Ahmed Khan (BSCS-15-21)
5. Select Course: CS101
6. Enter Marks: 85
7. Click **"Save Marks"**
8. Repeat for other courses:
   - MATH101: 78
   - ENG101: 92

**Step 4: Generate Result**
1. Go to **Result Generation**
2. Select Student: Ahmed Khan
3. Select Semester: 1 (or All Semesters)
4. Click **"Generate Result"**
5. Review calculated SGPA and grades

**Step 5: Export Transcript**
1. Go to **Transcript Export**
2. Select Student: Ahmed Khan
3. Click **"Generate Transcript"**
4. Save PDF to desired location

### 7.2 Bulk Operations

#### Importing 100 Students at Once

1. **Prepare Excel File:**
   - Open Excel
   - Create columns: roll_number, name, father_name, department, semester, gender
   - Fill in 100 rows of student data
   - Save as `students_batch1.xlsx`

2. **Import:**
   - Go to **Student Management**
   - Click **"Import CSV/Excel"**
   - Select `students_batch1.xlsx`
   - Review preview
   - Click **"Import"**

3. **Verify:**
   - Check student count
   - Search for a few students to verify

#### Deleting Multiple Students

1. Go to **Student Management**
2. Press `Ctrl+A` to select all (or `Ctrl+Click` for specific students)
3. Click **"Delete Selected"**
4. Confirm deletion

---

## 8. Advanced Features

### 8.1 Attendance Management

Track student attendance for courses.

**Features:**
- Mark attendance by date and course
- View attendance percentage
- Generate attendance reports
- Export attendance sheets

### 8.2 Assignment Management

Manage course assignments and submissions.

**Features:**
- Create assignments with deadlines
- Track submissions
- Grade assignments
- View submission statistics

### 8.3 Timetable Management

Create and manage class schedules.

**Features:**
- Create timetables for departments
- Assign teachers to time slots
- Avoid scheduling conflicts
- Export timetables to PDF

### 8.4 ID Card Generator

Generate student ID cards.

**Features:**
- Professional ID card design
- QR code generation
- Student photo support
- Batch generation

### 8.5 Alumni Management

Track alumni information and achievements.

**Features:**
- Alumni database
- Track employment and achievements
- Alumni events
- Contact management

### 8.6 AI Insights

Get AI-powered insights on student performance.

**Features:**
- Performance predictions
- At-risk student identification
- Trend analysis
- Recommendations

### 8.7 Advanced Analytics

Detailed analytics and visualizations.

**Features:**
- Performance trends over time
- Department comparisons
- Course difficulty analysis
- Interactive charts

### 8.8 Audit Logs

Track all system activities.

**Features:**
- User activity logs
- Data modification history
- Login/logout tracking
- Security audit trail

### 8.9 Role-Based Access Control (RBAC)

Fine-grained permission management.

**Features:**
- Custom roles
- Permission assignment
- Access control lists
- Role hierarchy

---

## 9. Reports & Analytics

### 9.1 Dashboard

The dashboard provides an overview of:

**Statistics:**
- Total Students
- Total Departments
- Total Courses
- Active Users

**Charts:**
- Student Distribution by Department (Pie Chart)
- Gender Distribution (Bar Chart)
- Semester-wise Enrollment (Line Chart)
- Performance Trends (Area Chart)

**Quick Actions:**
- Add Student
- Enter Marks
- Generate Result
- View Reports

### 9.2 Available Reports

#### Student Reports
- **Student List:** All students with filters
- **Department-wise Students:** Students grouped by department
- **Semester-wise Students:** Students grouped by semester
- **Gender Distribution:** Male/Female ratio

#### Performance Reports
- **Top Performers:** Students with highest CGPA
- **Pass/Fail Statistics:** Pass rates by department/semester
- **Grade Distribution:** Distribution of grades (A+, A, B+, etc.)
- **Course Performance:** Average marks by course

#### Department Reports
- **Department Statistics:** Student count, performance metrics
- **Department Comparison:** Compare departments
- **Faculty Reports:** Teacher assignments and workload

#### Custom Reports
- **Report Builder:** Create custom reports with filters
- **Export Options:** PDF, Excel, CSV
- **Scheduled Reports:** Automatic report generation

### 9.3 Exporting Reports

1. Generate the desired report
2. Click **"Export"** button
3. Choose format:
   - **PDF:** For printing and sharing
   - **Excel:** For further analysis
   - **CSV:** For data import
4. Select save location
5. Click **"Save"**

---

## 10. Backup & Recovery

### 10.1 Automatic Backup System

The system automatically backs up your data:

**Hourly Backups:**
- Runs every hour
- Keeps last 24 backups
- Location: `backups/exam_system_backup_YYYYMMDD_HHMMSS.db`

**Daily Backups:**
- Runs at 2:00 AM daily
- Kept for long-term storage
- Location: `backups/daily/exam_system_daily_YYYYMMDD.db`

**Auto-Cleanup:**
- Automatically deletes backups older than 30 days
- Keeps daily backups for 90 days

### 10.2 Manual Backup

#### Creating a Manual Backup

1. Go to **Backup & Restore** menu
2. Click **"Create Backup"**
3. Choose save location
4. Enter backup name (optional)
5. Click **"Save"**

**Backup includes:**
- All student records
- All marks and results
- All courses and departments
- All user accounts (passwords are hashed)
- System configuration

### 10.3 Restoring from Backup

#### Restore Process

1. Go to **Backup & Restore** menu
2. Click **"Restore Backup"**
3. Select backup file (`.db` file)
4. Click **"Open"**
5. **Confirm restoration** (this will replace current data!)
6. Application will restart with restored data

> ⚠️ **WARNING:** Restoring a backup will **replace all current data**. This action cannot be undone!

**Best Practice:**
- Create a backup before restoring
- Verify backup file integrity
- Test restore on a copy first (if critical)

### 10.4 Backup Best Practices

1. **Regular Backups:**
   - Weekly manual backups recommended
   - Before major operations (bulk delete, import)

2. **Off-site Storage:**
   - Copy backups to external drive
   - Use cloud storage (Google Drive, Dropbox)

3. **Backup Verification:**
   - Periodically test restore process
   - Verify backup file size and date

4. **Retention Policy:**
   - Keep daily backups for 1 month
   - Keep weekly backups for 3 months
   - Keep monthly backups for 1 year

---

## 11. Troubleshooting

### 11.1 Installation Issues

#### Problem: "Python is not recognized"
**Solution:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Restart command prompt

#### Problem: "pip install fails"
**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, install individually
pip install PyQt5==5.15.9
```

#### Problem: "Module not found" error
**Solution:**
```bash
# Verify all packages installed
pip list

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### 11.2 Database Issues

#### Problem: "Database is locked"
**Solution:**
- Close all instances of the application
- Check if another program is accessing the database
- Restart the application
- If using MySQL, check connection

#### Problem: "Failed to initialize database"
**Solution:**
1. Check write permissions on folder
2. Ensure disk space available
3. Delete `exam_system.db` and restart (creates fresh database)
4. Check logs in `database/logs/`

#### Problem: "Connection to MySQL failed"
**Solution:**
1. Verify `config.json` settings
2. Check network connectivity
3. Verify MySQL server is running
4. Test connection:
   ```bash
   python test_mysql_connection.py
   ```

### 11.3 Application Issues

#### Problem: Application won't start
**Solution:**
1. Run from command line to see errors:
   ```bash
   python main.py
   ```
2. Check Python version: `python --version`
3. Reinstall dependencies
4. Check antivirus/firewall

#### Problem: "Failed to create student"
**Solution:**
- Check phone number (must be 11 digits)
- Verify roll number is unique
- Ensure all required fields filled
- Check CNIC format (13 digits)

#### Problem: Table not refreshing after delete
**Solution:**
- Click 🔄 Refresh button
- Switch tabs and return
- Restart application

#### Problem: Can't login
**Solution:**
- Verify username/password
- Try default: admin/admin123
- Reset password:
  ```bash
  python reset_admin_user.py
  ```

### 11.4 PDF/Transcript Issues

#### Problem: "PDF generation failed"
**Solution:**
1. Install reportlab:
   ```bash
   pip install reportlab Pillow
   ```
2. Check write permissions on output folder
3. Ensure fonts are installed (Windows fonts)

#### Problem: Fonts not displaying correctly
**Solution:**
- Ensure these fonts are installed:
  - Bookman Old Style
  - Goudy Old Style
  - Times New Roman
- On Windows, they should be pre-installed

#### Problem: Watermark not showing
**Solution:**
- Check if logo file exists in `resources/images/`
- Verify image format (PNG recommended)
- Check image file size (< 5MB)

### 11.5 Performance Issues

#### Problem: Slow performance with many students
**Solution:**
1. Use filters to limit displayed records
2. Consider MySQL migration for 10,000+ students
3. Close other applications
4. Increase RAM if possible

#### Problem: Import taking too long
**Solution:**
- Import in smaller batches (500-1000 at a time)
- Close other applications
- Use CSV instead of Excel for faster import

### 11.6 Executable Issues

#### Problem: "Windows Defender blocked the app"
**Solution:**
1. Click "More info"
2. Click "Run anyway"
3. OR add to Windows Defender exclusions

#### Problem: "Failed to execute script"
**Solution:**
1. Extract to a folder with write permissions
2. Don't run from Downloads folder
3. Run as Administrator
4. Check antivirus logs

---

## 12. Technical Reference

### 12.1 Database Schema

#### Tables Overview

**1. departments**
```sql
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL,
    department_code TEXT UNIQUE NOT NULL,
    hod TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

**2. students**
```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    father_name TEXT NOT NULL,
    department_id INTEGER,
    semester INTEGER,
    gender TEXT,
    date_of_birth DATE,
    cnic TEXT,
    father_cnic TEXT,
    phone TEXT,
    email TEXT,
    guardian_phone TEXT,
    address TEXT,
    registration_no TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```

**3. courses**
```sql
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    department_id INTEGER,
    semester INTEGER,
    credits INTEGER,
    max_marks INTEGER,
    pass_marks INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```

**4. marks**
```sql
CREATE TABLE marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    marks_obtained REAL,
    grade TEXT,
    status TEXT,
    entered_by INTEGER,
    entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (entered_by) REFERENCES users(user_id)
);
```

**5. results**
```sql
CREATE TABLE results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    semester INTEGER,
    total_marks REAL,
    marks_obtained REAL,
    percentage REAL,
    sgpa REAL,
    cgpa REAL,
    overall_grade TEXT,
    status TEXT,
    rank INTEGER,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

**6. users**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT,
    email TEXT,
    assigned_subject_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (assigned_subject_id) REFERENCES courses(course_id)
);
```

### 12.2 Project Structure

```
university_exam_system/
│
├── main.py                      # Application entry point
├── config.py                    # Configuration settings
├── config.json                  # Database configuration
├── requirements.txt             # Python dependencies
│
├── controllers/                 # Business logic
│   ├── auth_controller.py       # Authentication
│   ├── student_controller.py    # Student operations
│   ├── course_controller.py     # Course operations
│   ├── marks_controller.py      # Marks operations
│   ├── result_controller.py     # Result generation
│   └── ...
│
├── database/                    # Database layer
│   ├── db_manager.py            # Database manager
│   └── migrations/              # Schema migrations
│
├── ui/                          # User interface
│   ├── login_window.py          # Login screen
│   ├── main_window.py           # Main application window
│   ├── student_management.py    # Student management UI
│   ├── course_management.py     # Course management UI
│   ├── marks_entry.py           # Marks entry UI
│   ├── result_generation.py     # Result generation UI
│   └── ...
│
├── utils/                       # Utility functions
│   ├── security.py              # Password hashing
│   ├── backup_service.py        # Automatic backups
│   └── validators.py            # Input validation
│
├── resources/                   # Application resources
│   ├── images/                  # Images and logos
│   ├── fonts/                   # Custom fonts
│   └── styles/                  # Stylesheets
│
├── backups/                     # Automatic backups
│   └── daily/                   # Daily backups
│
├── sample_data/                 # Sample CSV/Excel files
│
└── docs/                        # Documentation
```

### 12.3 Configuration Options

Edit `config.py` to customize:

```python
# Application Info
APP_NAME = "University Exam Result Management System"
APP_VERSION = "1.0.0"

# University Info
UNIVERSITY_NAME = "University of Balochistan"
UNIVERSITY_ADDRESS = "Sariab Road, Quetta"
UNIVERSITY_PHONE = "+92 (XXX) XXX-XXXX"
UNIVERSITY_EMAIL = "info@uob.edu.pk"

# Database
DATABASE_PATH = os.path.join(BASE_DIR, 'exam_system.db')

# Backup Settings
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
BACKUP_RETENTION_DAYS = 30
DAILY_BACKUP_RETENTION_DAYS = 90

# Security
SESSION_TIMEOUT_MINUTES = 30
PASSWORD_MIN_LENGTH = 6

# Grading Scale
GRADING_SCALE = {
    'A+': {'min': 90, 'max': 100, 'points': 4.0},
    'A': {'min': 80, 'max': 89, 'points': 4.0},
    'B+': {'min': 70, 'max': 79, 'points': 3.5},
    'B': {'min': 60, 'max': 69, 'points': 3.0},
    'C+': {'min': 50, 'max': 59, 'points': 2.5},
    'C': {'min': 40, 'max': 49, 'points': 2.0},
    'F': {'min': 0, 'max': 39, 'points': 0.0}
}

# Default Admin
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_FULLNAME = "System Administrator"
```

### 12.4 API Reference (For Developers)

#### Student Controller

```python
from controllers.student_controller import student_controller

# Get all students
students = student_controller.get_all_students()

# Get student by ID
student = student_controller.get_student_by_id(student_id)

# Create student
success, student_id = student_controller.create_student(
    roll_number="BSCS-01-21",
    name="Ahmed Khan",
    father_name="Muhammad Khan",
    department_id=1,
    semester=1,
    gender="Male"
)

# Update student
success = student_controller.update_student(student_id, **data)

# Delete student
success = student_controller.delete_student(student_id)
```

#### Marks Controller

```python
from controllers.marks_controller import marks_controller

# Enter marks
success, mark_id = marks_controller.enter_marks(
    student_id=1,
    course_id=1,
    marks_obtained=85,
    entered_by=1
)

# Get student marks
marks = marks_controller.get_student_marks(student_id, semester)
```

#### Result Controller

```python
from controllers.result_controller import result_controller

# Generate result
result = result_controller.generate_result(student_id, semester)

# Calculate CGPA
cgpa = result_controller.calculate_cgpa(student_id)
```

---

## 13. FAQ

### General Questions

**Q: Is this system free to use?**  
A: Yes, this is an open-source project. You can use, modify, and distribute it freely.

**Q: Can I use this for my university?**  
A: Absolutely! The system is designed for universities and can be customized to your needs.

**Q: Do I need internet connection?**  
A: No, the system works completely offline with SQLite. Internet is only needed for MySQL/TiDB Cloud.

**Q: How many students can the system handle?**  
A: SQLite: Up to 10,000 students comfortably. MySQL: 100,000+ students.

### Installation & Setup

**Q: I don't have Python. Can I still use it?**  
A: Yes! Use the executable version (`UniversityExamSystem.exe`). No Python required.

**Q: Can I install this on Mac or Linux?**  
A: Yes, but you'll need to run from source (Python). The executable is Windows-only.

**Q: How do I update the system?**  
A: Download the latest version and replace files. Your database (`exam_system.db`) will be preserved.

### Database & Data

**Q: Where is my data stored?**  
A: In `exam_system.db` file in the application folder.

**Q: Can I access the database directly?**  
A: Yes, it's a standard SQLite database. Use tools like DB Browser for SQLite.

**Q: How do I migrate from SQLite to MySQL?**  
A: Use the migration script:
```bash
python migrate_sqlite_to_mysql.py
```

**Q: Can multiple users access simultaneously?**  
A: SQLite: Limited (1-5 users). MySQL: Yes, hundreds of concurrent users.

### Features & Usage

**Q: How is GPA calculated?**  
A: SGPA = Σ(Grade Points × Credits) / Σ Credits  
CGPA = Average of all semester SGPAs

**Q: Can I customize the grading scale?**  
A: Yes, edit `GRADING_SCALE` in `config.py`.

**Q: Can students see other students' marks?**  
A: No, students can only see their own records.

**Q: Can I import students from Excel?**  
A: Yes, use the Import feature in Student Management.

**Q: How do I generate transcripts?**  
A: Go to Transcript Export tab, select student, click Generate.

### Security & Backup

**Q: Are passwords encrypted?**  
A: Yes, using bcrypt (industry-standard hashing).

**Q: How often should I backup?**  
A: The system auto-backs up hourly. Manual weekly backups recommended.

**Q: Can I recover deleted data?**  
A: Only if you have a backup. Deletions are permanent.

**Q: Is the data secure?**  
A: App-level: Yes (encrypted passwords, role-based access).  
File-level: Protect the folder with Windows permissions.

### Troubleshooting

**Q: "Database is locked" error?**  
A: Close all app instances. If using network drive, ensure only one user writes at a time.

**Q: Application is slow?**  
A: Use filters to limit displayed records. Consider MySQL for large datasets.

**Q: Can't login with default credentials?**  
A: Run `python reset_admin_user.py` to reset admin password.

**Q: PDF generation fails?**  
A: Ensure reportlab and Pillow are installed: `pip install reportlab Pillow`

### Advanced

**Q: Can I add custom fields to student records?**  
A: Yes, but requires database schema modification. See `database/migrations/`.

**Q: Can I integrate with other systems?**  
A: Yes, the database can be accessed by other applications.

**Q: Can I customize the UI?**  
A: Yes, modify files in `ui/` and `resources/styles/`.

**Q: Is there an API?**  
A: Not currently, but you can access the controllers programmatically.

---

## 📞 Support & Contact

### Documentation
- **Complete Documentation:** This file
- **Quick Start:** `QUICK_START.md`
- **User Guide:** `USER_GUIDE.md`
- **Build Instructions:** `BUILD_INSTRUCTIONS.md`
- **MySQL Migration:** `MYSQL_MIGRATION_GUIDE.md`

### Logs
- **Database Logs:** `database/logs/database_YYYYMMDD.log`
- **Application Logs:** Console output

### Getting Help
- **Email:** support@university.edu
- **GitHub Issues:** [Create an issue](https://github.com/yourusername/university-exam-system/issues)

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **PyQt5** - Excellent GUI framework
- **ReportLab** - PDF generation
- **SQLite** - Reliable database engine
- **University of Balochistan** - Requirements and testing

---

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Complete student, course, and marks management
- ✅ Result generation with GPA calculation
- ✅ Professional transcript export
- ✅ Automatic backup system
- ✅ Role-based access control
- ✅ Advanced analytics
- ✅ MySQL/TiDB Cloud support

---

## 📝 Quick Reference Card

### Default Credentials
- Username: `admin`
- Password: `admin123`

### Important Commands
```bash
# Run application
python main.py

# Install dependencies
pip install -r requirements.txt

# Build executable
pyinstaller UniversityExamSystem.spec

# Reset admin password
python reset_admin_user.py

# Test MySQL connection
python test_mysql_connection.py
```

### Important Files
- Database: `exam_system.db`
- Config: `config.py`, `config.json`
- Backups: `backups/`
- Logs: `database/logs/`

### Keyboard Shortcuts
- `Ctrl+A` - Select all
- `Ctrl+Click` - Multi-select
- `F5` - Refresh
- `Ctrl+F` - Search

---

**Made for University of Balochistan**  
**Developed By Shayak Siraj**  
**Version 1.0.0 | December 2025**

---

*This documentation covers everything from installation to advanced usage. For specific issues, refer to the Troubleshooting section or contact support.*
