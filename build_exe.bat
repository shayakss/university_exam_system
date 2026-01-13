@echo off
echo ========================================
echo Building University Exam System EXE
echo ========================================
echo.

echo Step 1: Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Step 2: Building executable with PyInstaller...
pyinstaller --clean UniversityExamSystem.spec

echo.
echo ========================================
if exist "dist\UniversityExamSystem.exe" (
    echo SUCCESS! Executable created!
    echo Location: dist\UniversityExamSystem.exe
    echo.
    echo You can now:
    echo 1. Copy the entire 'dist' folder to any location
    echo 2. Run UniversityExamSystem.exe
    echo.
    echo Note: The database file will be created in the same folder
) else (
    echo ERROR! Build failed. Check the output above for errors.
)
echo ========================================
pause
