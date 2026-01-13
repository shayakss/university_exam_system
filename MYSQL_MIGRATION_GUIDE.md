# SQLite to MySQL Migration Guide

## Overview

Your University Exam Management System has been successfully converted from SQLite to MySQL. This guide explains what was changed and how to use the new system.

## What Changed

### ✅ Core Files Modified

1. **`config.py`** - Now loads MySQL settings from `config.json`
2. **`db_manager.py`** - Complete rewrite supporting both MySQL and SQLite
3. **`requirements.txt`** - Added `mysql-connector-python>=8.2.0`
4. **All SQL schema files** - Converted to MySQL syntax

### ✅ SQL Syntax Conversions

| SQLite | MySQL |
|--------|-------|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `INT PRIMARY KEY AUTO_INCREMENT` |
| `TEXT` | `VARCHAR(255)` or `TEXT` |
| `REAL` | `DECIMAL(10,2)` |
| `INTEGER` | `INT` or `TINYINT` |
| `?` placeholders | `%s` (auto-converted) |
| No engine specified | `ENGINE=InnoDB` |

### ✅ New Features

- **Multi-PC Support**: All users connect to same central MySQL server
- **Automatic Placeholder Conversion**: Controllers don't need changes
- **Connection Pooling**: Better performance for multiple users
- **Network Error Handling**: Auto-reconnect on connection loss

## Setup Instructions

### Step 1: Install MySQL Server

1. Install MySQL Server 8+ on your server/PC
2. Start MySQL service
3. Note the host, port, username, and password

### Step 2: Create Database

Run these SQL commands in MySQL:

```sql
CREATE DATABASE exam_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ems_user'@'localhost' IDENTIFIED BY 'StrongPass123!';
GRANT ALL PRIVILEGES ON exam_management.* TO 'ems_user'@'localhost';
FLUSH PRIVILEGES;
```

For remote access (multi-PC):
```sql
CREATE USER 'ems_user'@'%' IDENTIFIED BY 'StrongPass123!';
GRANT ALL PRIVILEGES ON exam_management.* TO 'ems_user'@'%';
FLUSH PRIVILEGES;
```

### Step 3: Install Python Dependencies

```bash
pip install mysql-connector-python>=8.2.0
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Connection

The `config.json` file is already created with these settings:

```json
{
  "use": "mysql",
  "mysql_host": "localhost",
  "mysql_user": "ems_user",
  "mysql_password": "StrongPass123!",
  "mysql_database": "exam_management"
}
```

**For multi-PC setup**, change `mysql_host` to the server's IP address on client PCs.

### Step 5: Create Schema

Run the schema creation:

```bash
python -c "from database.db_manager import db; db.initialize_schema()"
```

Or use MySQL command line:
```bash
mysql -u ems_user -p exam_management < database/schema.sql
```

### Step 6: Migrate Data (Optional)

If you have existing SQLite data:

```bash
python migrate_sqlite_to_mysql.py
```

This will:
- Read all data from `exam_system.db`
- Transfer it to MySQL database
- Preserve all relationships and IDs
- Show progress for each table

### Step 7: Test Connection

```bash
python test_mysql_connection.py
```

Expected output:
```
✓ Database connection successful!
✓ Query execution successful!
✓ departments: X records
✓ students: X records
...
```

### Step 8: Run Application

```bash
python main.py
```

The application will now use MySQL automatically!

## Multi-PC Setup

### Server PC (Database Host)

1. Install MySQL Server
2. Create database and user (with `'%'` for remote access)
3. Configure firewall to allow MySQL port (3306)
4. Set `config.json` with `"mysql_host": "localhost"`

### Client PCs

1. Install Python and dependencies
2. Copy application files
3. Set `config.json` with `"mysql_host": "SERVER_IP_ADDRESS"`
4. Run application

**Example client config.json:**
```json
{
  "use": "mysql",
  "mysql_host": "192.168.1.100",
  "mysql_user": "ems_user",
  "mysql_password": "StrongPass123!",
  "mysql_database": "exam_management"
}
```

## Troubleshooting

### Connection Refused

- Check MySQL service is running: `systemctl status mysql`
- Check firewall allows port 3306
- Verify host IP address is correct

### Access Denied

- Verify username and password in `config.json`
- Check user has privileges: `SHOW GRANTS FOR 'ems_user'@'%';`
- Ensure user is created for correct host (`localhost` vs `%`)

### Table Not Found

- Run schema creation: `python -c "from database.db_manager import db; db.initialize_schema()"`
- Or manually: `mysql -u ems_user -p exam_management < database/schema.sql`

### Slow Performance

- Check network latency (for remote connections)
- Ensure MySQL is properly configured
- Consider adding indexes (already included in schema)

## Rollback to SQLite

If you need to revert to SQLite:

1. Rename or delete `config.json`
2. Application will automatically use SQLite
3. Your `exam_system.db` file is preserved

## Controller Code - No Changes Needed!

All controllers work without modification because `db_manager.py` automatically:
- Converts `?` to `%s` for MySQL
- Returns dictionaries from both SQLite and MySQL
- Handles connection differences transparently

Example - this code works for both:
```python
db.execute_query("SELECT * FROM students WHERE semester = ?", (1,))
```

## Files Summary

### Modified Files
- `config.py` - MySQL config loading
- `database/db_manager.py` - MySQL support
- `database/schema.sql` - MySQL syntax
- `database/migration_teacher_student.sql` - MySQL syntax
- `database/migrations/add_student_fields.sql` - MySQL syntax
- `requirements.txt` - Added MySQL driver

### New Files
- `config.json` - Database configuration
- `migrate_sqlite_to_mysql.py` - Data migration tool
- `test_mysql_connection.py` - Connection test
- `MYSQL_MIGRATION_GUIDE.md` - This file

### Unchanged Files
- All 24 controller files (work automatically!)
- All UI files
- All utility files
- Application logic

## Benefits of MySQL

✅ **Multi-PC Support**: Multiple users can access simultaneously
✅ **Better Performance**: Optimized for concurrent access
✅ **Centralized Data**: One database for entire organization
✅ **Better Security**: User authentication and permissions
✅ **Scalability**: Can handle larger datasets
✅ **Backup Tools**: Professional backup solutions available
✅ **Network Access**: Access from anywhere on network

## Next Steps

1. Test all features thoroughly
2. Train users on multi-PC access
3. Set up regular MySQL backups
4. Configure MySQL for production use
5. Monitor performance and optimize as needed

---

**Need Help?**
- Check MySQL logs: `/var/log/mysql/error.log`
- Test connection: `python test_mysql_connection.py`
- Review config: `cat config.json`
