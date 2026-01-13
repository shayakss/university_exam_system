# University Exam Result Management System - User Guide

## 📋 Table of Contents
1. [Installation](#installation)
2. [First Time Setup](#first-time-setup)
3. [User Roles](#user-roles)
4. [Features](#features)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### Running the Executable
1. Extract the application folder
2. Double-click `UniversityExamSystem.exe`
3. The application will start automatically

### System Requirements
- **Operating System:** Windows 7 or later
- **RAM:** Minimum 2GB
- **Storage:** 100MB free space
- **Display:** 1024x768 or higher

---

## 🔐 First Time Setup

### Default Login Credentials

**Administrator Account:**
- Username: `admin`
- Password: `admin123`

**⚠️ Important:** Change the default password after first login!

### Initial Configuration
1. Login as administrator
2. Go to **User Management**
3. Create departments
4. Add courses
5. Create teacher and student accounts

---

## 👥 User Roles

### 1. Administrator
**Full Access:**
- User management
- Department management
- Course management
- Student management
- Marks entry
- Result generation
- Reports and analytics
- System backup/restore

### 2. Data Entry
**Limited Access:**
- Student management
- Marks entry
- View reports

### 3. Teacher
**Department-Specific Access:**
- View students in their department only
- Enter marks for their courses
- Generate results for their students
- View department reports

### 4. Student
**Personal Access:**
- View own results
- View own profile
- Check grades and GPA

---

## ✨ Features

### Student Management
- Add/Edit/Delete students
- Import students from Excel/CSV
- Track student information:
  - Roll Number
  - Name
  - Father Name
  - Registration Number
  - CNIC
  - Father CNIC
  - Address
  - Phone (11 digits)
  - Guardian Phone
  - Email
  - Date of Birth

### Department Management
- Create departments
- Assign head of department
- View student counts (Male/Female)

### Course Management
- Add courses per department
- Set credits and marks
- Assign to semesters

### Marks Entry
- Enter marks by course
- Automatic validation
- Update existing marks

### Result Generation
- Calculate SGPA/CGPA
- Automatic grading
- Pass/Fail status
- Class ranking

### Reports & Analytics
- Pass/Fail statistics
- Department-wise reports
- Semester-wise analysis
- Export to Excel/PDF

---

## 🎓 How to Use

### Adding a New Student
1. Go to **Student Management**
2. Click **➕ Add Student**
3. Fill in all required fields (marked with *)
4. Click **Save**

### Entering Marks
1. Go to **Marks Entry**
2. Select Department
3. Select Semester
4. Select Student
5. Select Course
6. Enter marks
7. Click **💾 Save Marks**

### Generating Results
1. Go to **Result Generation**
2. Select student from dropdown
3. Click **📊 Generate Result**
4. View calculated GPA and grades
5. Export to PDF if needed

### Creating Reports
1. Go to **Reports & Analytics**
2. Select filters (Department, Semester)
3. Click **📊 Generate Report**
4. View statistics
5. Export to Excel

---

## 🔧 Troubleshooting

### Application Won't Start
**Solution:**
- Run as Administrator
- Check Windows Defender
- Install Visual C++ Redistributable

### Database Error
**Solution:**
- Ensure write permissions
- Don't run from read-only location
- Check disk space

### "Failed to Create Student" Error
**Solution:**
- Check phone number (must be 11 digits)
- Verify all required fields are filled
- Ensure roll number is unique

### Table Not Refreshing After Delete
**Solution:**
- Click the 🔄 Refresh button
- Switch to another tab and back

### Can't Login
**Solution:**
- Check username/password
- Use default: admin/admin123
- Contact administrator to reset

---

## 📞 Support

### Common Issues

**Q: How do I change my password?**
A: Go to My Profile → Change Password

**Q: Can I import multiple students at once?**
A: Yes, use the Import feature with Excel/CSV file

**Q: How is GPA calculated?**
A: SGPA = Sum(Grade Points × Credits) / Total Credits

**Q: Can teachers see other departments?**
A: No, teachers only see their assigned department

**Q: How do I backup data?**
A: Admin → Backup/Restore → Create Backup

---

## 📊 Grading System

| Marks Range | Grade | Grade Points |
|-------------|-------|--------------|
| 85-100      | A+    | 4.0          |
| 80-84       | A     | 4.0          |
| 75-79       | A-    | 3.7          |
| 71-74       | B+    | 3.3          |
| 68-70       | B     | 3.0          |
| 64-67       | B-    | 2.7          |
| 61-63       | C+    | 2.3          |
| 58-60       | C     | 2.0          |
| 54-57       | C-    | 1.7          |
| 50-53       | D     | 1.0          |
| Below 50    | F     | 0.0          |

---

## 🚀 Deployment & Security (Important)

### 1. Multi-User Usage
This application uses **SQLite**, which is a file-based database.
- **Recommended:** Single-user use (one person at a time).
- **Network Use:** You can place the `Release` folder on a shared network drive. Multiple users can open it, but **simultaneous writing** (e.g., two people saving marks at the exact same time) may cause "Database Locked" errors.
- **Best Practice:** If multiple teachers need to enter marks, assign them specific time slots or ensure they don't work simultaneously.

### 2. Data Security
- **App Security:** Access to the application is protected by username/password. Passwords are encrypted using **Bcrypt** (industry standard), so they cannot be reverse-engineered.
- **Database File:** The data is stored in `exam_system.db`.
  - ⚠️ **Warning:** Anyone with access to the computer/folder can copy this file.
  - **Protection:** Restrict Windows folder permissions so only authorized users can access the `Release` folder.
  - **Backups:** Keep backups in a secure, separate location.

### 3. Is it Client Ready?
Yes, the software is feature-complete for a desktop application.
- **Features:** All requested modules (Student, Dept, Course, Marks, Result, Reports) are working.
- **Stability:** Input validation (phone, email) prevents bad data.
- **Portability:** The EXE runs without installation.

---

## 💾 Data Management

### Backup
- Regular backups recommended
- Backup includes all data
- Store backups securely

### Restore
- Use backup file to restore
- All data will be replaced
- Cannot be undone

---

## 🎯 Best Practices

1. **Regular Backups:** Backup data weekly
2. **Strong Passwords:** Use complex passwords
3. **User Roles:** Assign appropriate roles
4. **Data Validation:** Verify data before entry
5. **Regular Updates:** Keep system updated

---

## 📝 Notes

- Database file: `exam_system.db`
- Located in application folder
- Don't delete or modify manually
- Backup before major changes

---

**Version:** 1.0
**Last Updated:** November 2025
