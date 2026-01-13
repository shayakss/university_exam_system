"""
Audit Controller
Manages comprehensive audit logging for all system actions
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import json

class AuditController:
    """Controller for audit logging"""
    
    def log_action(self, user_id: int, username: str, action_type: str,
                  table_name: str = None, record_id: int = None,
                  action_description: str = None, old_value: str = None,
                  new_value: str = None, ip_address: str = None) -> Tuple[bool, str]:
        """Log an action to the audit trail"""
        try:
            query = """
                INSERT INTO audit_logs
                (user_id, username, action_type, table_name, record_id,
                 action_description, old_value, new_value, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, log_id = db.execute_update(
                query,
                (user_id, username, action_type, table_name, record_id,
                 action_description, old_value, new_value, ip_address)
            )
            
            if success:
                return True, f"Action logged (ID: {log_id})"
            return False, "Failed to log action"
            
        except Exception as e:
            # Don't fail the main operation if logging fails
            print(f"Audit logging error: {e}")
            return False, f"Error: {str(e)}"
    
    def log_login(self, user_id: int, username: str, ip_address: str = None) -> Tuple[bool, str]:
        """Log a user login"""
        return self.log_action(
            user_id, username, 'LOGIN',
            action_description=f"User {username} logged in",
            ip_address=ip_address
        )
    
    def log_logout(self, user_id: int, username: str, ip_address: str = None) -> Tuple[bool, str]:
        """Log a user logout"""
        return self.log_action(
            user_id, username, 'LOGOUT',
            action_description=f"User {username} logged out",
            ip_address=ip_address
        )
    
    def log_create(self, user_id: int, username: str, table_name: str,
                  record_id: int, new_data: Dict, ip_address: str = None) -> Tuple[bool, str]:
        """Log a record creation"""
        return self.log_action(
            user_id, username, 'CREATE', table_name, record_id,
            action_description=f"Created new record in {table_name}",
            new_value=json.dumps(new_data),
            ip_address=ip_address
        )
    
    def log_update(self, user_id: int, username: str, table_name: str,
                  record_id: int, old_data: Dict, new_data: Dict,
                  ip_address: str = None) -> Tuple[bool, str]:
        """Log a record update"""
        return self.log_action(
            user_id, username, 'UPDATE', table_name, record_id,
            action_description=f"Updated record in {table_name}",
            old_value=json.dumps(old_data),
            new_value=json.dumps(new_data),
            ip_address=ip_address
        )
    
    def log_delete(self, user_id: int, username: str, table_name: str,
                  record_id: int, old_data: Dict, ip_address: str = None) -> Tuple[bool, str]:
        """Log a record deletion"""
        return self.log_action(
            user_id, username, 'DELETE', table_name, record_id,
            action_description=f"Deleted record from {table_name}",
            old_value=json.dumps(old_data),
            ip_address=ip_address
        )
    
    def get_audit_logs(self, user_id: int = None, action_type: str = None,
                      table_name: str = None, start_date: date = None,
                      end_date: date = None, limit: int = 1000) -> List[Dict]:
        """Get audit logs with filters"""
        try:
            query = """
                SELECT * FROM audit_logs
                WHERE 1=1
            """
            params = []
            
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            
            if action_type:
                query += " AND action_type = ?"
                params.append(action_type)
            
            if table_name:
                query += " AND table_name = ?"
                params.append(table_name)
            
            if start_date:
                query += " AND date(timestamp) >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND date(timestamp) <= ?"
                params.append(end_date)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting audit logs: {e}")
            return []
    
    def get_user_activity(self, user_id: int, days: int = 30) -> List[Dict]:
        """Get recent activity for a specific user"""
        try:
            query = """
                SELECT * FROM audit_logs
                WHERE user_id = ? AND timestamp >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
            """
            return db.execute_query(query, (user_id, days))
        except Exception as e:
            print(f"Error getting user activity: {e}")
            return []
    
    def get_record_history(self, table_name: str, record_id: int) -> List[Dict]:
        """Get complete history of changes to a specific record"""
        try:
            query = """
                SELECT * FROM audit_logs
                WHERE table_name = ? AND record_id = ?
                ORDER BY timestamp DESC
            """
            return db.execute_query(query, (table_name, record_id))
        except Exception as e:
            print(f"Error getting record history: {e}")
            return []
    
    def get_audit_statistics(self, start_date: date = None, end_date: date = None) -> Dict:
        """Get audit statistics"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_actions,
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(DISTINCT CASE WHEN action_type = 'LOGIN' THEN user_id END) as logins,
                    COUNT(DISTINCT CASE WHEN action_type = 'CREATE' THEN log_id END) as creates,
                    COUNT(DISTINCT CASE WHEN action_type = 'UPDATE' THEN log_id END) as updates,
                    COUNT(DISTINCT CASE WHEN action_type = 'DELETE' THEN log_id END) as deletes
                FROM audit_logs
                WHERE 1=1
            """
            params = []
            
            if start_date:
                query += " AND date(timestamp) >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND date(timestamp) <= ?"
                params.append(end_date)
            
            result = db.execute_query(query, tuple(params))
            return result[0] if result else {}
        except Exception as e:
            print(f"Error getting audit statistics: {e}")
            return {}
    
    def search_audit_logs(self, search_term: str, limit: int = 100) -> List[Dict]:
        """Search audit logs by description or username"""
        try:
            query = """
                SELECT * FROM audit_logs
                WHERE action_description LIKE ? OR username LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
            search_pattern = f"%{search_term}%"
            return db.execute_query(query, (search_pattern, search_pattern, limit))
        except Exception as e:
            print(f"Error searching audit logs: {e}")
            return []
    
    def cleanup_old_logs(self, days_to_keep: int = 365) -> Tuple[bool, str]:
        """Delete audit logs older than specified days"""
        try:
            query = """
                DELETE FROM audit_logs
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            """
            success, _ = db.execute_update(query, (days_to_keep,))
            
            if success:
                return True, f"Cleaned up logs older than {days_to_keep} days"
            return False, "Failed to cleanup old logs"
            
        except Exception as e:
            return False, f"Error: {str(e)}"

# Global instance
audit_controller = AuditController()
