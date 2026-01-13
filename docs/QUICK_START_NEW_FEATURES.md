# QUICK START GUIDE - New Features

## 🚀 Getting Started with New Features

### Step 1: Database Setup (COMPLETED ✓)
The database has been migrated with all new tables. You're ready to use the new features!

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- qrcode (for ID card QR codes)
- numpy (for data processing)
- scikit-learn (for AI insights)
- plotly (for interactive charts)

### Step 3: Run the Application
```bash
python main.py
```

---

## 📚 Feature Quick Access

### 1. Attendance Tracking
**Location:** Main Menu → Attendance Management  
**Quick Action:**
1. Select department and semester
2. Choose date
3. Mark attendance (Present/Absent/Leave)
4. View attendance reports

### 2. Timetable & Scheduling
**Location:** Main Menu → Timetable Management  
**Quick Action:**
1. Click "Add Class Schedule"
2. Select course, teacher, day, time
3. Assign room
4. System checks for conflicts automatically

### 3. Assignment Management
**Location:** Main Menu → Assignments  
**For Teachers:**
1. Click "Create Assignment"
2. Enter details and due date
3. Students see it automatically

**For Students:**
1. View "My Assignments"
2. Submit before due date

### 4. Student Promotion
**Location:** Main Menu → Student Promotion  
**Quick Action:**
1. Select department and semester
2. Click "Check Eligibility"
3. Review eligible students
4. Click "Promote All Eligible"

### 5. ID Card Generation
**Location:** Main Menu → ID Card Generator  
**Quick Action:**
1. Select Student/Teacher/Staff
2. Choose individual or batch
3. Click "Generate"
4. Print or export PDF

### 6. Alumni Management
**Location:** Main Menu → Alumni  
**Quick Action:**
1. Select graduated student
2. Click "Move to Alumni"
3. Enter graduation details
4. Add employment info

### 7. Dark Mode
**Location:** Toolbar → Theme Toggle Button  
**Quick Action:**
- Click theme button to switch instantly
- Preference saved automatically

### 8. Analytics Dashboard
**Location:** Main Menu → Analytics  
**Features:**
- Interactive charts
- Department comparisons
- Performance trends
- Pass/fail rates

### 9. Custom Reports
**Location:** Main Menu → Report Builder  
**Quick Action:**
1. Select report type
2. Choose columns
3. Apply filters
4. Export to Excel/PDF

### 10. RBAC (Admin Only)
**Location:** Main Menu → RBAC Editor  
**Quick Action:**
1. Create custom role
2. Select permissions
3. Assign role to users

### 11. Audit Logs (Admin Only)
**Location:** Main Menu → Audit Viewer  
**Features:**
- View all system actions
- Filter by user/date/action
- Export audit reports

### 12. Database Archiving (Admin Only)
**Location:** Main Menu → Archive Manager  
**Quick Action:**
1. Select academic year
2. Preview data
3. Click "Archive"

### 13. Cloud Backup (Admin Only)
**Location:** Main Menu → Cloud Backup  
**Quick Action:**
1. Select Google Drive or Dropbox
2. Authenticate
3. Set schedule
4. Click "Backup Now"

### 14. AI Insights
**Location:** Main Menu → AI Insights  
**Features:**
- At-risk student list
- Risk scores and factors
- Intervention recommendations
- Performance predictions

---

## 🎯 Common Tasks

### Mark Attendance for a Class
1. Attendance Management
2. Select department, semester, course
3. Select date
4. Mark all students (bulk select)
5. Click "Save Attendance"

### Create Weekly Timetable
1. Timetable Management
2. For each class:
   - Select day and time
   - Choose course and teacher
   - Assign room
3. System prevents conflicts
4. Print timetable

### Promote Students to Next Semester
1. Student Promotion
2. Select current semester
3. System checks CGPA, attendance, F grades
4. Review eligible list
5. Promote all or individually

### Generate ID Cards for New Batch
1. ID Card Generator
2. Select "Batch Generation"
3. Choose department and semester
4. Upload photos (optional)
5. Generate all cards
6. Export to PDF for printing

### Find At-Risk Students
1. AI Insights
2. View at-risk list
3. Click student for details
4. See risk factors
5. Follow intervention recommendations

---

## ⚙️ Configuration

### Set Promotion Rules
1. Student Promotion → Rules
2. Set minimum CGPA (default: 2.0)
3. Set max F grades (default: 0)
4. Set min attendance (default: 75%)

### Configure Cloud Backup
1. Cloud Backup Settings
2. Choose provider
3. Authenticate with cloud account
4. Set backup folder
5. Enable auto-backup
6. Set frequency (daily/weekly)

### Create Custom Roles
1. RBAC Editor
2. Create role (e.g., "Exam Coordinator")
3. Assign permissions:
   - View marks ✓
   - Enter marks ✓
   - Generate results ✓
4. Assign role to users

---

## 🔧 Troubleshooting

### Issue: Can't see new menu items
**Solution:** Restart the application after migration

### Issue: QR codes not generating
**Solution:** Install qrcode library
```bash
pip install qrcode[pil]
```

### Issue: Charts not displaying
**Solution:** Install matplotlib and plotly
```bash
pip install matplotlib plotly
```

### Issue: Cloud backup not working
**Solution:** This requires API credentials for Google Drive/Dropbox. Contact admin for setup.

---

## 📖 Documentation

- **Full Feature Details:** NEW_FEATURES_DOCUMENTATION.txt
- **Implementation Plan:** implementation_plan.md
- **User Guide:** USER_GUIDE.md
- **Database Schema:** database/migrations/database_migration_v2.sql

---

## 💡 Tips

1. **Start with Attendance:** Most impactful feature for daily use
2. **Use Dark Mode:** Easier on eyes during long sessions
3. **Check AI Insights Weekly:** Identify at-risk students early
4. **Set Up Cloud Backup:** Protect your data
5. **Create Custom Reports:** Save time with templates
6. **Review Audit Logs:** Monitor system usage
7. **Archive Old Data:** Keep system fast

---

## 🎓 Training Recommendations

### For Teachers
1. Attendance marking (15 min)
2. Assignment creation (10 min)
3. Timetable viewing (5 min)

### For Admins
1. Student promotion (20 min)
2. RBAC setup (30 min)
3. Cloud backup configuration (15 min)
4. AI insights interpretation (20 min)

### For Students
1. View timetable (5 min)
2. Check attendance (5 min)
3. Submit assignments (10 min)

---

**Need Help?** Check NEW_FEATURES_DOCUMENTATION.txt for detailed explanations of each feature.

**Version:** 2.0.0  
**Last Updated:** December 2, 2025
