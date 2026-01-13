"""
Quick fix for teacher department filtering
Run this to restore corrupted files and apply fixes
"""
import os
import shutil

print("=== Restoring Files from Backup ===\n")

# Files that got corrupted
corrupted_files = [
    "ui/course_management.py",
    "ui/marks_entry.py"
]

for file_path in corrupted_files:
    backup_path = file_path + ".bak"
    if os.path.exists(backup_path):
        shutil.copy(backup_path, file_path)
        print(f"✓ Restored {file_path}")
    else:
        print(f"✗ No backup for {file_path}")

print("\n✅ File restoration complete!")
print("\nNOTE: You may need to manually update these files with department filtering.")
print("See implementation_plan.md for details.")
