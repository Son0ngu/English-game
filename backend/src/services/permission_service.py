import time
from ..data.permission_repository import PermissionRepository

class PermissionService:
    def __init__(self, repository: PermissionRepository = None):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"permission_checks": 0, "permission_updates": 0}
        self.repository = repository
        
        # Initialize permission data
        if repository:
            data = repository.load_permissions()
            self.role_permissions = data["role_permissions"]
            self.temp_permissions = data["temp_permissions"]
        else:
            self.role_permissions = {
                "student": ["READ"],
                "teacher": ["READ", "WRITE"],
                "admin": ["READ", "WRITE", "DELETE"]
            }
            self.temp_permissions = {}  # Temporary permissions with expiry
            
        self.user_permissions = {}  # Custom permissions for specific users
    
    def add_permission(self, role: str, permission: str) -> bool:
        """Add a permission to a role"""
        self._stats["permission_updates"] += 1
        try:
            if role in self.role_permissions:
                if permission not in self.role_permissions[role]:
                    self.role_permissions[role].append(permission)
                self._save_permissions()
                return True
            else:
                self.role_permissions[role] = [permission]
                self._save_permissions()
                return True
        except Exception as e:
            self._last_error = e
            return False
    
    def delete_permission(self, role: str, permission: str) -> bool:
        """Delete a permission from a role"""
        self._stats["permission_updates"] += 1
        try:
            if role in self.role_permissions and permission in self.role_permissions[role]:
                self.role_permissions[role].remove(permission)
                self._save_permissions()
                return True
            return False
        except Exception as e:
            self._last_error = e
            return False
    
    def check_permission(self, role: str, permission: str) -> bool:
        """Check if a role has a specific permission"""
        self._stats["permission_checks"] += 1
        try:
            if role in self.role_permissions:
                return permission in self.role_permissions[role]
            return False
        except Exception as e:
            self._last_error = e
            return False
    
    def check_multiple_permission(self, role: str, permissions: list) -> bool:
        """Check if a role has all of the specified permissions"""
        self._stats["permission_checks"] += 1
        try:
            if role not in self.role_permissions:
                return False
            
            role_perms = self.role_permissions[role]
            return all(perm in role_perms for perm in permissions)
        except Exception as e:
            self._last_error = e
            return False
    
    def add_temp_permission(self, role: str, permission: str, duration: str) -> bool:
        """Add a temporary permission that expires after the specified duration"""
        self._stats["permission_updates"] += 1
        try:
            # Parse duration string (e.g., "1h", "30m", "1d")
            # For simplicity, let's assume duration is in seconds
            expiry = int(time.time() + int(duration))
            
            key = f"{role}:{permission}"
            self.temp_permissions[key] = expiry
            self._save_permissions()
            
            return True
        except Exception as e:
            self._last_error = e
            return False
    
    def check_internal(self) -> dict:
        """Internal health check for this service"""
        # Clean up expired temporary permissions
        current_time = int(time.time())
        expired = [k for k, v in self.temp_permissions.items() if v < current_time]
        for key in expired:
            del self.temp_permissions[key]
            
        return {
            "status": "healthy" if not self._last_error else "degraded",
            "uptime": time.time() - self._startup_time,
            "stats": self._stats,
            "roles_count": len(self.role_permissions),
            "temp_permissions_count": len(self.temp_permissions),
            "last_error": str(self._last_error) if self._last_error else None,
            "details": "Permission service running normally"
        }
    
    def add_user_permission(self, user_id: str, permission: str) -> bool:
        """Add a permission for a specific user"""
        self._stats["permission_updates"] += 1
        try:
            if user_id in self.user_permissions:
                if permission not in self.user_permissions[user_id]:
                    self.user_permissions[user_id].append(permission)
            else:
                self.user_permissions[user_id] = [permission]
                
            self._save_permissions()
            return True
        except Exception as e:
            self._last_error = e
            return False
            
    def check_user_permission(self, user_id: str, role: str, permission: str) -> bool:
        """Check permission for a user, combining role and user permissions"""
        self._stats["permission_checks"] += 1
        try:
            # Check temporary permissions
            key = f"{role}:{permission}"
            current_time = int(time.time())
            if key in self.temp_permissions and self.temp_permissions[key] > current_time:
                return True
                
            # Check user-specific permissions
            if user_id in self.user_permissions and permission in self.user_permissions[user_id]:
                return True
                
            # Check role-based permissions
            return self.check_permission(role, permission)
        except Exception as e:
            self._last_error = e
            return False
            
    def _save_permissions(self) -> bool:
        """Save permissions to repository"""
        if self.repository:
            return self.repository.save_permissions(
                self.role_permissions, 
                self.temp_permissions
            )
        return False