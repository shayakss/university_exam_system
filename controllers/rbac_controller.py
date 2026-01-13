"""
RBAC (Role-Based Access Control) Controller
Manages custom roles and permissions
"""
from database.db_manager import db
from typing import List, Dict, Optional, Tuple

class RBACController:
    """Controller for role-based access control"""
    
    def create_role(self, role_name: str, description: str = None) -> Tuple[bool, str]:
        """Create a new custom role"""
        try:
            query = """
                INSERT INTO roles (role_name, description, is_system_role)
                VALUES (?, ?, 0)
            """
            success, role_id = db.execute_update(query, (role_name, description))
            
            if success:
                return True, f"Role created successfully (ID: {role_id})"
            return False, "Failed to create role"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def assign_permission_to_role(self, role_id: int, permission_id: int) -> Tuple[bool, str]:
        """Assign a permission to a role"""
        try:
            query = """
                INSERT INTO role_permissions (role_id, permission_id)
                VALUES (?, ?)
            """
            success, _ = db.execute_update(query, (role_id, permission_id))
            
            if success:
                return True, "Permission assigned to role"
            return False, "Failed to assign permission"
            
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                return False, "Permission already assigned to this role"
            return False, f"Error: {str(e)}"
    
    def remove_permission_from_role(self, role_id: int, permission_id: int) -> Tuple[bool, str]:
        """Remove a permission from a role"""
        try:
            query = "DELETE FROM role_permissions WHERE role_id = ? AND permission_id = ?"
            success, _ = db.execute_update(query, (role_id, permission_id))
            
            if success:
                return True, "Permission removed from role"
            return False, "Failed to remove permission"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def assign_role_to_user(self, user_id: int, role_id: int, assigned_by: int) -> Tuple[bool, str]:
        """Assign a role to a user"""
        try:
            query = """
                INSERT INTO user_roles (user_id, role_id, assigned_by)
                VALUES (?, ?, ?)
            """
            success, _ = db.execute_update(query, (user_id, role_id, assigned_by))
            
            if success:
                return True, "Role assigned to user"
            return False, "Failed to assign role"
            
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                return False, "User already has this role"
            return False, f"Error: {str(e)}"
    
    def remove_role_from_user(self, user_id: int, role_id: int) -> Tuple[bool, str]:
        """Remove a role from a user"""
        try:
            query = "DELETE FROM user_roles WHERE user_id = ? AND role_id = ?"
            success, _ = db.execute_update(query, (user_id, role_id))
            
            if success:
                return True, "Role removed from user"
            return False, "Failed to remove role"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Get all permission codes for a user"""
        try:
            query = """
                SELECT DISTINCT p.permission_code
                FROM permissions p
                JOIN role_permissions rp ON p.permission_id = rp.permission_id
                JOIN user_roles ur ON rp.role_id = ur.role_id
                WHERE ur.user_id = ?
            """
            results = db.execute_query(query, (user_id,))
            return [r['permission_code'] for r in results] if results else []
        except Exception as e:
            print(f"Error getting user permissions: {e}")
            return []
    
    def check_permission(self, user_id: int, permission_code: str) -> bool:
        """Check if user has a specific permission"""
        try:
            permissions = self.get_user_permissions(user_id)
            return permission_code in permissions
        except Exception as e:
            print(f"Error checking permission: {e}")
            return False
    
    def get_all_roles(self, include_system: bool = True) -> List[Dict]:
        """Get all roles"""
        try:
            query = "SELECT * FROM roles WHERE is_active = 1"
            params = []
            
            if not include_system:
                query += " AND is_system_role = 0"
            
            query += " ORDER BY role_name"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting roles: {e}")
            return []
    
    def get_all_permissions(self, category: str = None) -> List[Dict]:
        """Get all permissions"""
        try:
            query = "SELECT * FROM permissions WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY category, permission_name"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting permissions: {e}")
            return []
    
    def get_role_permissions(self, role_id: int) -> List[Dict]:
        """Get all permissions assigned to a role"""
        try:
            query = """
                SELECT p.*
                FROM permissions p
                JOIN role_permissions rp ON p.permission_id = rp.permission_id
                WHERE rp.role_id = ?
                ORDER BY p.category, p.permission_name
            """
            return db.execute_query(query, (role_id,))
        except Exception as e:
            print(f"Error getting role permissions: {e}")
            return []
    
    def get_user_roles(self, user_id: int) -> List[Dict]:
        """Get all roles assigned to a user"""
        try:
            query = """
                SELECT r.*, ur.assigned_at, u.full_name as assigned_by_name
                FROM roles r
                JOIN user_roles ur ON r.role_id = ur.role_id
                LEFT JOIN users u ON ur.assigned_by = u.user_id
                WHERE ur.user_id = ?
                ORDER BY r.role_name
            """
            return db.execute_query(query, (user_id,))
        except Exception as e:
            print(f"Error getting user roles: {e}")
            return []

# Global instance
rbac_controller = RBACController()
