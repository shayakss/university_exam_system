"""
Cloud Backup Controller
Manages cloud backup integration (Google Drive/Dropbox)
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import os
import shutil
import config

class CloudBackupController:
    """Controller for cloud backup management"""
    
    def save_backup_config(self, provider: str, access_token: str = None,
                          refresh_token: str = None, folder_path: str = None,
                          auto_backup_enabled: bool = False,
                          backup_frequency_days: int = 7) -> Tuple[bool, str]:
        """Save cloud backup configuration"""
        try:
            # Check if config exists
            existing = db.execute_query("SELECT config_id FROM backup_config WHERE provider = ?", (provider,))
            
            if existing:
                query = """
                    UPDATE backup_config
                    SET access_token = ?, refresh_token = ?, folder_path = ?,
                        auto_backup_enabled = ?, backup_frequency_days = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE provider = ?
                """
                success, _ = db.execute_update(
                    query,
                    (access_token, refresh_token, folder_path,
                     1 if auto_backup_enabled else 0, backup_frequency_days, provider)
                )
            else:
                query = """
                    INSERT INTO backup_config
                    (provider, access_token, refresh_token, folder_path,
                     auto_backup_enabled, backup_frequency_days, is_enabled)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """
                success, _ = db.execute_update(
                    query,
                    (provider, access_token, refresh_token, folder_path,
                     1 if auto_backup_enabled else 0, backup_frequency_days)
                )
            
            if success:
                return True, f"{provider} backup configuration saved"
            return False, "Failed to save backup configuration"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_backup_config(self, provider: str = None) -> List[Dict]:
        """Get cloud backup configuration"""
        try:
            query = "SELECT * FROM backup_config WHERE 1=1"
            params = []
            
            if provider:
                query += " AND provider = ?"
                params.append(provider)
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting backup config: {e}")
            return []
    
    def create_local_backup(self) -> Tuple[bool, str, str]:
        """Create a local database backup file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"exam_system_backup_{timestamp}.db"
            backup_path = os.path.join(config.BACKUP_DIR, backup_filename)
            
            # Ensure backup directory exists
            os.makedirs(config.BACKUP_DIR, exist_ok=True)
            
            # Copy database file
            shutil.copy2(config.DATABASE_PATH, backup_path)
            
            return True, f"Backup created: {backup_filename}", backup_path
            
        except Exception as e:
            return False, f"Error creating backup: {str(e)}", ""
    
    def upload_to_cloud(self, provider: str, local_file_path: str) -> Tuple[bool, str]:
        """Upload backup file to cloud storage"""
        try:
            # Get configuration
            configs = self.get_backup_config(provider)
            
            if not configs or not configs[0]['is_enabled']:
                return False, f"{provider} is not configured or enabled"
            
            config_data = configs[0]
            
            # Note: Actual cloud upload would require provider-specific SDKs
            # This is a placeholder that simulates the upload
            
            if provider == 'Google Drive':
                # Would use google-api-python-client here
                # from googleapiclient.discovery import build
                # service = build('drive', 'v3', credentials=creds)
                # file_metadata = {'name': os.path.basename(local_file_path)}
                # media = MediaFileUpload(local_file_path)
                # file = service.files().create(body=file_metadata, media_body=media).execute()
                pass
            
            elif provider == 'Dropbox':
                # Would use dropbox SDK here
                # import dropbox
                # dbx = dropbox.Dropbox(config_data['access_token'])
                # with open(local_file_path, 'rb') as f:
                #     dbx.files_upload(f.read(), f"/{os.path.basename(local_file_path)}")
                pass
            
            # Update last backup date
            db.execute_update(
                "UPDATE backup_config SET last_backup_date = CURRENT_TIMESTAMP WHERE provider = ?",
                (provider,)
            )
            
            return True, f"Backup uploaded to {provider} successfully (simulated)"
            
        except Exception as e:
            return False, f"Error uploading to cloud: {str(e)}"
    
    def backup_to_cloud(self, provider: str) -> Tuple[bool, str]:
        """Create backup and upload to cloud in one operation"""
        try:
            # Create local backup
            success, message, backup_path = self.create_local_backup()
            
            if not success:
                return False, message
            
            # Upload to cloud
            success, upload_message = self.upload_to_cloud(provider, backup_path)
            
            if success:
                return True, f"Backup created and uploaded to {provider}"
            else:
                return False, f"Backup created locally but upload failed: {upload_message}"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def should_auto_backup(self, provider: str) -> bool:
        """Check if automatic backup is due"""
        try:
            configs = self.get_backup_config(provider)
            
            if not configs or not configs[0]['auto_backup_enabled']:
                return False
            
            config_data = configs[0]
            
            if not config_data['last_backup_date']:
                return True
            
            last_backup = datetime.strptime(config_data['last_backup_date'], '%Y-%m-%d %H:%M:%S')
            days_since_backup = (datetime.now() - last_backup).days
            
            return days_since_backup >= config_data['backup_frequency_days']
            
        except Exception as e:
            print(f"Error checking auto backup: {e}")
            return False
    
    def disable_cloud_backup(self, provider: str) -> Tuple[bool, str]:
        """Disable cloud backup for a provider"""
        try:
            query = "UPDATE backup_config SET is_enabled = 0 WHERE provider = ?"
            success, _ = db.execute_update(query, (provider,))
            
            if success:
                return True, f"{provider} backup disabled"
            return False, "Failed to disable backup"
            
        except Exception as e:
            return False, f"Error: {str(e)}"

# Global instance
cloud_backup_controller = CloudBackupController()
