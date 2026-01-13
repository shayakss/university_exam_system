# University Exam Result Management System - Build Instructions

## Building the Executable

### Quick Build (Recommended)
1. Double-click `build_exe.bat`
2. Wait for the build to complete
3. Find the executable in the `dist` folder

### Manual Build
```bash
# Clean old builds
pyinstaller --clean UniversityExamSystem.spec

# Or use the simple command
pyinstaller --onefile --windowed --name="UniversityExamSystem" main.py
```

## Distribution

### What to Distribute
After building, you'll find:
- `dist/UniversityExamSystem.exe` - The main executable
- The database will be created automatically on first run

### How to Distribute
1. **Option 1: Single Folder**
   - Copy the entire `dist` folder
   - Rename it to "University Exam System"
   - Share this folder

2. **Option 2: Installer** (Advanced)
   - Use Inno Setup or NSIS to create an installer
   - Include the exe and any required files

## Running the Application

### First Time Setup
1. Run `UniversityExamSystem.exe`
2. Database will be created automatically
3. Login with default credentials:
   - Username: `admin`
   - Password: `admin123`

### System Requirements
- Windows 7 or later
- No Python installation required
- Minimum 2GB RAM
- 100MB free disk space

## Troubleshooting

### "Missing DLL" Error
- Install Visual C++ Redistributable
- Download from Microsoft's website

### "Database Error"
- Ensure the exe has write permissions
- Run as administrator if needed

### Application Won't Start
- Check Windows Defender/Antivirus
- Add exception for the exe file

## Build Options

### Include Icon
Add to spec file:
```python
icon='path/to/icon.ico'
```

### Reduce File Size
```bash
pyinstaller --onefile --windowed --strip main.py
```

### Debug Mode
```bash
pyinstaller --onefile --console main.py
```

## Notes
- First run may take longer (extracting files)
- Database file created in same directory as exe
- All dependencies are bundled
- No internet connection required
