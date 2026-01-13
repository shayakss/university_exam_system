# University Exam Result Management System - Configuration Guide

## 🎓 Customizing Your University Information

To customize the system for your university, edit the `config.py` file:

### University Details (Lines 11-15)
```python
UNIVERSITY_NAME = "Your University Name Here"  # Change this!
UNIVERSITY_ADDRESS = "Your Address Here"
UNIVERSITY_PHONE = "+1 (XXX) XXX-XXXX"
UNIVERSITY_EMAIL = "info@youruniversity.edu"
UNIVERSITY_WEBSITE = "www.youruniversity.edu"
```

### How It Works:
- **PDF Marksheets**: Will automatically use your university name
- **Excel Reports**: Will include your university name in headers
- **Login Screen**: Displays your university name

### Example:
```python
UNIVERSITY_NAME = "Stanford University"
UNIVERSITY_ADDRESS = "450 Serra Mall, Stanford, CA 94305"
UNIVERSITY_PHONE = "+1 (650) 723-2300"
UNIVERSITY_EMAIL = "registrar@stanford.edu"
UNIVERSITY_WEBSITE = "www.stanford.edu"
```

## 📝 Other Important Settings

### Default Admin Credentials (Lines 43-45)
**⚠️ IMPORTANT**: Change these after first login!
```python
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"  # Change this immediately!
```

### Grading Scale (Lines 27-35)
Customize your grading system if needed.

---

**Need Help?** Check `README.md` for full documentation.
