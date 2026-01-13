# Sample Data Files

This folder contains sample data files for testing the bulk import functionality.

## 📁 Files Included

### 1. `sample_students.csv` / `sample_students.xlsx`
Sample student data with 20 students from CSE and EE departments.

**Columns:**
- `roll_number` - Unique student roll number (e.g., CS001, EE001)
- `name` - Student full name
- `department_code` - Department code (CSE, EE, etc.)
- `semester` - Current semester (1-8)
- `gender` - Male/Female/Other
- `date_of_birth` - Format: YYYY-MM-DD
- `email` - Student email address
- `phone` - 10-digit phone number
- `address` - Student address (optional)

## 🚀 How to Use

### Step 1: Add Departments First
Before importing students, make sure you have created the departments:

1. Go to **Departments** tab
2. Click **"+ Add Department"**
3. Add these departments:
   - **Code:** CSE, **Name:** Computer Science & Engineering
   - **Code:** EE, **Name:** Electrical Engineering

### Step 2: Import Students
1. Go to **Students** tab
2. Click **"📁 Import CSV/Excel"** button
3. Select `sample_students.csv` or `sample_students.xlsx`
4. Click **Open**
5. Students will be imported automatically!

## 📝 Creating Your Own Import File

### Required Columns:
- `roll_number` (required)
- `name` (required)
- `department_code` (required)
- `semester` (required)
- `gender` (required)
- `date_of_birth` (required)

### Optional Columns:
- `email`
- `phone`
- `address`

### Example Format:
```csv
roll_number,name,department_code,semester,gender,date_of_birth,email,phone,address
CS001,John Doe,CSE,1,Male,2005-03-15,john@email.com,1234567890,123 Main St
```

## ⚠️ Important Notes

1. **Department codes must exist** - Create departments before importing students
2. **Roll numbers must be unique** - Duplicate roll numbers will be rejected
3. **Date format** - Use YYYY-MM-DD format for dates
4. **Semester range** - Must be between 1-8
5. **Gender values** - Must be: Male, Female, or Other

## 🎯 Sample Data Overview

The sample file includes:
- **10 CSE students** (CS001 - CS011)
- **10 EE students** (EE001 - EE009)
- Students across semesters 1-6
- Mix of male and female students
- Complete contact information

---

**Need Help?** Check the main `README.md` for full documentation.
