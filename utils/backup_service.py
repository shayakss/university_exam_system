"""
Automatic Database Backup Service
Runs periodic backups to prevent data loss
"""
import schedule
import time
import threading
from database.db_manager import db
from datetime import datetime
import os


class BackupService:
    """Background service for automatic database backups"""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the backup service"""
        if self.running:
            print("⚠ Backup service already running")
            return
        
        self.running = True
        
        # Schedule backups
        schedule.every(1).hours.do(self.perform_backup)  # Hourly backups
        schedule.every().day.at("02:00").do(self.perform_daily_backup)  # Daily at 2 AM
        
        # Start background thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        print("✓ Automatic backup service started")
        print("  - Hourly backups enabled")
        print("  - Daily backups at 2:00 AM")
    
    def stop(self):
        """Stop the backup service"""
        self.running = False
        schedule.clear()
        print("✓ Backup service stopped")
    
    def perform_backup(self):
        """Perform a backup"""
        try:
            success, backup_path = db.backup_database()
            if success:
                print(f"✓ Auto-backup completed: {backup_path}")
                self.cleanup_old_backups()
            else:
                print(f"✗ Auto-backup failed: {backup_path}")
        except Exception as e:
            print(f"✗ Backup error: {e}")
    
    def perform_daily_backup(self):
        """Perform daily backup with special naming"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            backup_filename = f"exam_system_daily_{timestamp}.db"
            
            import config
            backup_path = os.path.join(config.BACKUP_DIR, "daily", backup_filename)
            
            success, path = db.backup_database(backup_path)
            if success:
                print(f"✓ Daily backup completed: {path}")
        except Exception as e:
            print(f"✗ Daily backup error: {e}")
    
    def cleanup_old_backups(self, keep_count=24):
        """Keep only the last N hourly backups"""
        try:
            import config
            backup_dir = config.BACKUP_DIR
            
            if not os.path.exists(backup_dir):
                return
            
            # Get all backup files
            backups = []
            for file in os.listdir(backup_dir):
                if file.startswith("exam_system_backup_") and file.endswith(".db"):
                    filepath = os.path.join(backup_dir, file)
                    backups.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (newest first)
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Delete old backups
            for filepath, _ in backups[keep_count:]:
                try:
                    os.remove(filepath)
                    print(f"✓ Removed old backup: {os.path.basename(filepath)}")
                except Exception as e:
                    print(f"✗ Failed to remove {filepath}: {e}")
        
        except Exception as e:
            print(f"✗ Cleanup error: {e}")
    
    def _run_scheduler(self):
        """Run the scheduler in background"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


# Global backup service instance
backup_service = BackupService()
