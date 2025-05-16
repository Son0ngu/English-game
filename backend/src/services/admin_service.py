import time
from typing import Dict, List, Any, Optional
from .user_service import UserProfileService
from ..models.user import TeacherProfile

class AdminService:
    def __init__(self, user_service=None):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"service_checks": 0, "user_management_actions": 0}
        self.user_service = user_service
        self.services = {}  # Registry for services
        
        # Đăng ký user_service nếu có
        if user_service:
            self.register_service("users", user_service)
            
    def register_service(self, name: str, service) -> None:
        """Đăng ký một service để health check"""
        self.services[name] = service
        
    def check_service_availability(self, service_name: str = None) -> dict:
        """Check health of registered services"""
        self._stats["service_checks"] += 1
        results = {}
        
        if service_name:
            if service_name in self.services:
                service = self.services[service_name]
                if hasattr(service, 'check_internal'):
                    results[service_name] = service.check_internal()
                else:
                    results[service_name] = {"status": "unknown", "details": "No health check implemented"}
            else:
                results[service_name] = {"status": "not_found", "details": "Service not registered"}
        else:
            # Check all services
            for name, service in self.services.items():
                if hasattr(service, 'check_internal'):
                    results[name] = service.check_internal()
                else:
                    results[name] = {"status": "unknown", "details": "No health check implemented"}
                    
        return results
    
    def get_users(self, role: str = None) -> List[Dict[str, Any]]:
        """Get all users, optionally filtered by role"""
        self._stats["user_management_actions"] += 1
        try:
            if not self.user_service:
                return []
                
            if role == "student":
                return self.user_service.get_all_students()
            elif role == "teacher":
                return self.user_service.get_all_teachers()
            else:
                students = self.user_service.get_all_students()
                teachers = self.user_service.get_all_teachers()
                return students + teachers
        except Exception as e:
            self._last_error = e
            return []
            
    def change_user_role(self, user_id: str, new_role: str) -> bool:
        """Change a user's role"""
        self._stats["user_management_actions"] += 1
        try:
            if not self.user_service:
                return False
                
            result = self.user_service.update_profile(user_id, {"role": new_role})
            return result.get("success", False)
        except Exception as e:
            self._last_error = e
            return False
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get general system statistics"""
        try:
            stats = {
                "uptime": time.time() - self._startup_time,
                "registered_services": list(self.services.keys())
            }
            
            # Gather stats from user service if available
            if self.user_service and hasattr(self.user_service, 'check_internal'):
                user_health = self.user_service.check_internal()
                if "user_stats" in user_health:
                    stats["users"] = user_health["user_stats"]
                    
            return stats
        except Exception as e:
            self._last_error = e
            return {"error": str(e)}
    
    def check_internal(self) -> dict:
        """Internal health check for this service"""
        return {
            "status": "healthy" if not self._last_error else "degraded",
            "uptime": time.time() - self._startup_time,
            "stats": self._stats,
            "last_error": str(self._last_error) if self._last_error else None,
            "details": "Admin service running normally"
        }