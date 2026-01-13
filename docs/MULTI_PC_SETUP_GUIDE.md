# Multi-PC Setup Guide
# University Exam Management System - MySQL Edition

## 🎯 Overview

Your application now supports multiple PCs accessing the same centralized MySQL database. This guide explains how to set it up.

---

## 📋 Prerequisites

1. **MySQL Server** installed on one PC (the "Server PC")
2. **Network connectivity** between all PCs
3. **Python 3.11+** installed on all PCs (or use the .exe)

---

## 🖥️ Server PC Setup (Database Host)

### Step 1: Install MySQL Server

1. Download MySQL Server 8+ from: https://dev.mysql.com/downloads/installer/
2. Install with default settings
3. Remember the root password you set during installation

### Step 2: Create Database and User

Open MySQL Workbench or MySQL Command Line and run:

```sql
-- Create database
CREATE DATABASE exam_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user for remote access
CREATE USER 'ems_user'@'%' IDENTIFIED BY 'Shayaksiraj123';

-- Grant privileges
GRANT ALL PRIVILEGES ON exam_management.* TO 'ems_user'@'%';
FLUSH PRIVILEGES;
```

**Note:** The `'%'` allows connections from any IP address. For better security, replace `'%'` with specific IP addresses.

### Step 3: Configure MySQL for Remote Access

1. Open MySQL configuration file:
   - Windows: `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`
   - Find the line: `bind-address = 127.0.0.1`
   - Change it to: `bind-address = 0.0.0.0`
   - Save and restart MySQL service

2. Restart MySQL:
   - Open Services (Win + R, type `services.msc`)
   - Find "MySQL80" service
   - Right-click → Restart

### Step 4: Configure Windows Firewall

1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. Select "TCP" and enter port `3306` → Next
6. Select "Allow the connection" → Next
7. Check all profiles → Next
8. Name it "MySQL Server" → Finish

### Step 5: Find Server IP Address

Open Command Prompt and run:
```cmd
ipconfig
```

Look for "IPv4 Address" (e.g., `192.168.1.100`)
**Write this down - you'll need it for client PCs!**

### Step 6: Setup Application on Server PC

1. Copy the application folder to Server PC
2. Edit `config.json`:
   ```json
   {
     "use": "mysql",
     "mysql_host": "localhost",
     "mysql_user": "ems_user",
     "mysql_password": "Shayaksiraj123",
     "mysql_database": "exam_management"
   }
   ```

3. Load the schema:
   ```cmd
   python init_mysql_schema.py
   ```

4. Create admin user:
   ```cmd
   python reset_admin_user.py
   ```

5. Run the application:
   ```cmd
   python main.py
   ```

---

## 💻 Client PC Setup (Other PCs)

### Step 1: Copy Application Files

Copy the entire application folder to each client PC.

### Step 2: Edit config.json

On each client PC, edit `config.json` with the **Server PC's IP address**:

```json
{
  "use": "mysql",
  "mysql_host": "192.168.1.100",  ← Change this to your Server PC IP
  "mysql_user": "ems_user",
  "mysql_password": "Shayaksiraj123",
  "mysql_database": "exam_management"
}
```

### Step 3: Install Python Dependencies (if not using .exe)

```cmd
pip install -r requirements.txt
```

### Step 4: Test Connection

```cmd
python test_mysql_connection.py
```

You should see:
```
✓ MySQL connected: ems_user@192.168.1.100/exam_management
✓ Multi-PC support enabled
```

### Step 5: Run Application

```cmd
python main.py
```

---

## 📦 Creating Executable (.exe)

### Option 1: Using PyInstaller (Recommended)

1. Install PyInstaller:
   ```cmd
   pip install pyinstaller
   ```

2. Create the executable:
   ```cmd
   pyinstaller --name="ExamSystem" --onefile --windowed --icon=assets/icon.ico main.py
   ```

3. The .exe will be in `dist/ExamSystem.exe`

### Option 2: Using Auto-py-to-exe (GUI Method)

1. Install:
   ```cmd
   pip install auto-py-to-exe
   ```

2. Run:
   ```cmd
   auto-py-to-exe
   ```

3. Configure:
   - Script Location: `main.py`
   - Onefile: One File
   - Console Window: Window Based
   - Icon: Select your icon file
   - Click "Convert .py to .exe"

---

## 📁 Distributing the Executable

### What to Include in Distribution Package:

```
ExamSystem/
├── ExamSystem.exe          ← The executable
├── config.json             ← Database configuration
├── assets/                 ← Images, icons, etc.
├── database/
│   └── schema.sql         ← For reference
├── README.txt             ← Instructions
└── MULTI_PC_SETUP.txt     ← This guide
```

### For Each Client PC:

1. Copy the entire folder
2. Edit `config.json` with correct server IP
3. Run `ExamSystem.exe`

---

## 🔧 Troubleshooting

### Cannot Connect to Server

**Check:**
1. Server PC IP address is correct in `config.json`
2. MySQL service is running on server
3. Firewall allows port 3306
4. Both PCs are on the same network

**Test connection:**
```cmd
ping 192.168.1.100
telnet 192.168.1.100 3306
```

### "Access Denied" Error

**Check:**
1. Username and password in `config.json` are correct
2. User has remote access permissions (`'%'` in CREATE USER)
3. Run on server: `SHOW GRANTS FOR 'ems_user'@'%';`

### Slow Performance

**Possible causes:**
1. Network latency - check network speed
2. Too many simultaneous users
3. Large database - consider indexing

---

## 🔒 Security Best Practices

### For Production Use:

1. **Change default password:**
   ```sql
   ALTER USER 'ems_user'@'%' IDENTIFIED BY 'YourStrongPassword123!';
   ```

2. **Restrict IP access:**
   ```sql
   -- Instead of '%', use specific IPs
   CREATE USER 'ems_user'@'192.168.1.101' IDENTIFIED BY 'password';
   CREATE USER 'ems_user'@'192.168.1.102' IDENTIFIED BY 'password';
   ```

3. **Enable SSL/TLS** for encrypted connections

4. **Regular backups:**
   ```cmd
   mysqldump -u ems_user -p exam_management > backup.sql
   ```

---

## 📊 Network Diagram

```
┌─────────────────────┐
│   Server PC         │
│  (192.168.1.100)    │
│                     │
│  ┌───────────────┐  │
│  │ MySQL Server  │  │
│  │ Port 3306     │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │ Application   │  │
│  └───────────────┘  │
└──────────┬──────────┘
           │
    Network Switch/Router
           │
     ┌─────┴─────┬─────────┬─────────┐
     │           │         │         │
┌────▼────┐ ┌───▼────┐ ┌──▼─────┐ ┌─▼──────┐
│Client 1 │ │Client 2│ │Client 3│ │Client N│
│ (.101)  │ │ (.102) │ │ (.103) │ │ (.xxx) │
└─────────┘ └────────┘ └────────┘ └────────┘
```

---

## ✅ Quick Checklist

**Server PC:**
- [ ] MySQL Server installed
- [ ] Database and user created
- [ ] Firewall configured (port 3306)
- [ ] `config.json` has `"mysql_host": "localhost"`
- [ ] Schema loaded
- [ ] Admin user created

**Client PCs:**
- [ ] Application files copied
- [ ] `config.json` has server IP address
- [ ] Connection test successful
- [ ] Application runs

---

## 🎉 You're Ready!

All PCs can now access the same database simultaneously. Changes made on one PC are instantly visible on all others!

**Login credentials:**
- Username: `admin`
- Password: `admin123`

**Remember to change the admin password after first login!**
