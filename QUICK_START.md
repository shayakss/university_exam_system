# 🚀 Quick Start Guide

Get started with the University Exam Result Management System in 5 minutes!

## Step 1: Install Dependencies

```bash
cd "d:\New folder\New folder (2)\university_exam_system"
pip install -r requirements.txt
```

## Step 2: Run the Application

```bash
python main.py
```

## Step 3: Login

**Default Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change the password after first login!**

## Step 4: Setup Your University

### A. Configure University Information
Edit `config.py` (lines 11-15):
```python
UNIVERSITY_NAME = "Your University Name"  # ← Change this!
UNIVERSITY_ADDRESS = "Your Address"
UNIVERSITY_PHONE = "+1 (XXX) XXX-XXXX"
UNIVERSITY_EMAIL = "info@youruniversity.edu"
```

### B. Add Departments
1. Go to **Departments** tab
2. Click **"+ Add Department"**
3. Fill in:
   - Department Code (e.g., CSE)
   - Department Name (e.g., Computer Science & Engineering)
   - Head of Department (optional)

**OR** Use sample data:
- Import `sample_data/sample_departments.csv`

### C. Add Courses
1. Go to **Course/Subjects** tab
2. Click **"+ Add Subject"**
3. Fill in course details

### D. Add Students

**Option 1: Manual Entry**
1. Go to **Students** tab
2. Click **"+ Add Student"**
3. Fill in student details

**Option 2: Bulk Import (Recommended)**
1. Go to **Students** tab
2. Click **"📁 Import CSV/Excel"**
3. Select `sample_data/sample_students.csv`
4. Click Open

✅ **20 sample students imported!**

## Step 5: Enter Marks & Generate Results

1. **Marks Entry Tab:**
   - Select Department → Semester → Student → Course
   - Enter marks
   - Click "Save Marks"

2. **Generate Results Tab:**
   - Select student
   - Click "Calculate Result"
   - Export to PDF or Excel

## 📊 Features Overview

| Feature | Location | Description |
|---------|----------|-------------|
| Student Management | Students Tab | Add, edit, delete, import students |
| Department Management | Departments Tab | Manage departments |
| Course Management | Course/Subjects Tab | Manage courses |
| Marks Entry | Generate Results Tab | Enter student marks |
| Result Generation | Generate Results Tab | Calculate SGPA/CGPA |
| Reports | Reports Tab | View toppers, statistics |
| Backup/Restore | Backup & Restore Tab | Database backup |

## 🎓 GPA System

- **Max GPA:** 4.0
- **Grading Scale:**
  - A+/A: 4.0 (90-100%)
  - B+: 3.5 (70-79%)
  - B: 3.0 (60-69%)
  - C+: 2.5 (50-59%)
  - C: 2.0 (40-49%)
  - F: 0.0 (0-39%)

## 📁 Sample Data Files

Located in `sample_data/` folder:
- `sample_students.csv` - 20 sample students
- `sample_students.xlsx` - Same data in Excel format
- `sample_departments.csv` - 5 sample departments
- `README.md` - Detailed instructions

## 🔧 Building EXE File

```bash
pip install pyinstaller
pyinstaller UniversityExamSystem.spec
```

The `.exe` file will be in the `dist/` folder.

## 📚 Need More Help?

- **Full Documentation:** See `README.md`
- **Configuration Guide:** See `CONFIGURATION_GUIDE.md`
- **Build Instructions:** See `BUILD_INSTRUCTIONS.md`
- **Sample Data Guide:** See `sample_data/README.md`

---

**Developed By Shayak Siraj**
