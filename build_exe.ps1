# Build Executable Script
# Creates a standalone .exe for the University Exam System

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Building Exam System Executable" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue

if (-not $pyinstaller) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install PyInstaller!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ PyInstaller ready" -ForegroundColor Green
Write-Host ""

# Build the executable
Write-Host "Building executable..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

pyinstaller --name="ExamSystem" `
    --onefile `
    --windowed `
    --add-data="resources;resources" `
    --add-data="database;database" `
    --add-data="config.json;." `
    --collect-data mysql.connector `
    --hidden-import="mysql.connector" `
    --hidden-import="mysql.connector.locales" `
    --hidden-import="mysql.connector.locales.eng" `
    --hidden-import="bcrypt" `
    --hidden-import="PyQt5" `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✓ BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: dist\ExamSystem.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Copy dist\ExamSystem.exe to your distribution folder" -ForegroundColor White
    Write-Host "2. Include config.json in the same folder" -ForegroundColor White
    Write-Host "3. Include assets folder if needed" -ForegroundColor White
    Write-Host "4. Distribute to client PCs" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Build failed!" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Red
    exit 1
}
