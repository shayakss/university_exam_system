# Fix Log - Executable Issues

## Issues Reported
1. "Failed to initialize database schema" error when running .exe
2. Missing logo in login box

## Root Cause Analysis
1. **Schema Error**: The application was trying to load `database/schema.sql` from the file system, but in the frozen executable (PyInstaller), files are extracted to a temporary directory (`sys._MEIPASS`). The path resolution logic was incomplete.
2. **Missing Logo**: Similar issue. The `QPixmap` was trying to load `resources/images/uob_logo.png` relative to the executable, but the resources are inside the bundle.
3. **Build Config**: The build script was including `assets` folder, but the project uses `resources` folder.

## Fixes Applied
1. **Created `utils/resource_helper.py`**: Added a `resource_path()` function that correctly resolves paths for both development (normal run) and production (frozen .exe).
2. **Updated `ui/login_window.py`**: Modified to use `resource_path()` for loading the logo.
3. **Updated `database/db_manager.py`**: Modified `initialize_schema` to use `resource_path()` for loading `schema.sql`.
4. **Updated Build Command**: Changed `--add-data` to include `resources` and `database` folders correctly.

## Verification
- Rebuilding the executable with the new configuration.
- The new executable should correctly find both the schema file and the logo image.
