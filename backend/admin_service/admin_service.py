import time
from typing import Dict, Any, List
from auth_service.signup import signup
from auth_service.permission_service import permission_service
from userProfile_service.user.user import StudentProfile, TeacherProfile

class AdminService:
    """
    Dịch vụ quản trị hệ thống.
    Lớp này cung cấp các chức năng quản trị như kiểm tra sức khỏe dịch vụ, 
    quản lý người dùng và thu thập số liệu thống kê hệ thống.
    
    Tích hợp chức năng ServiceRegistry để đăng ký và quản lý các dịch vụ.
    """
    
    def __init__(self, user_service):
        """
        Khởi tạo AdminService
        
        Args:
            user_service: Service quản lý người dùng
        """
        self.user_service = user_service
        self.services = {}
        self.signup = signup()
        self.permission_service = permission_service()

    def register_service(self, name: str, service):
        """
        Đăng ký service để theo dõi
        
        Args:
            name: Tên service
            service: Đối tượng service
        """
        self.services[name] = service
        
    def get_system_health(self) -> Dict[str, Any]:
        """
        Kiểm tra sức khỏe của toàn bộ hệ thống
        
        Returns:
            Dictionary chứa thông tin sức khỏe hệ thống
        """
        health_status = {}
        overall_status = "healthy"
        
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'check_internal'):
                    service_health = service.check_internal()
                else:
                    service_health = {"status": "unknown", "details": "No health check method"}
                    
                health_status[service_name] = service_health
                
                # Nếu có service nào không khỏe mạnh, đánh dấu overall status
                if service_health.get('status') != 'healthy':
                    overall_status = "degraded"
                    
            except Exception as e:
                health_status[service_name] = {
                    "status": "error",
                    "error": str(e)
                }
                overall_status = "degraded"
        
        return {
            "overall_status": overall_status,
            "services": health_status,
            "total_services": len(self.services)
        }
        
    def get_service_list(self) -> List[str]:
        """
        Lấy danh sách các service đã đăng ký
        
        Returns:
            Danh sách tên các service
        """
        return list(self.services.keys())
        
    def get_user_statistics(self) -> Dict[str, Any]:
        """
        Lấy thống kê người dùng từ user service
        
        Returns:
            Dictionary chứa thống kê người dùng
        """
        try:
            # Sử dụng user_service mà không cần import
            students = self.user_service.get_all_students()
            teachers = self.user_service.get_all_teachers()
            
            return {
                "total_students": len(students),
                "total_teachers": len(teachers),
                "total_users": len(students) + len(teachers)
            }
        except Exception as e:
            return {
                "total_students": 0,
                "total_teachers": 0,
                "total_users": 0,
                "error": str(e)
            }
    
    def check_internal(self) -> Dict[str, Any]:
        """
        Kiểm tra trạng thái nội bộ của AdminService
        
        Returns:
            Dictionary chứa thông tin trạng thái
        """
        try:
            system_health = self.get_system_health()
            user_stats = self.get_user_statistics()
            
            return {
                "status": "healthy",
                "system_health": system_health,
                "user_statistics": user_stats,
                "registered_services": len(self.services)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    def add_specialized_user(self,username,password,role):
        return self.signup.add_specialized_user(username,password,role)

    def add_permission(self, role: str, path: str, service: str, method: str) -> Dict[str, Any]:
        """
        Thêm permission mới sử dụng permission_service có sẵn
        
        Args:
            role: Role của user
            path: Đường dẫn route
            service: Tên service
            method: HTTP method
            
        Returns:
            Dictionary chứa kết quả
        """
        try:
            # Check if permission already exists
            existing = self.permission_service.check_permission(role, path, service, method)
            if existing:
                return {
                    "success": False,
                    "error": f"Permission already exists for role '{role}' on {method} {service}/{path}"
                }
            
            # Add permission using existing permission service
            success = self.permission_service.add_permission(role, path, service, method)
            
            if success:
                return {
                    "success": True,
                    "message": "Permission added successfully",
                    "permission": {
                        "role": role,
                        "path": path,
                        "service": service,
                        "method": method
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to add permission to database"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add permission: {str(e)}"
            }

    def list_permissions(self, role: str = None, service: str = None) -> Dict[str, Any]:
        """
        Lấy danh sách permissions với filter
        
        Args:
            role: Filter theo role (optional)
            service: Filter theo service (optional)
            
        Returns:
            Dictionary chứa kết quả
        """
        try:
            # Sử dụng permission_service có sẵn để lấy permissions
            permissions = self.permission_service.get_all_permissions()
            
            # Apply filters
            if role:
                permissions = [p for p in permissions if p.get('role') == role]
            if service:
                permissions = [p for p in permissions if p.get('service') == service]
            
            return {
                "success": True,
                "permissions": permissions,
                "total_count": len(permissions)
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list permissions: {str(e)}"
            }

    def delete_permission(self, role: str, path: str, service: str, method: str) -> Dict[str, Any]:
        """
        Xóa permission
        
        Args:
            role: Role của user
            path: Đường dẫn route
            service: Tên service
            method: HTTP method
            
        Returns:
            Dictionary chứa kết quả
        """
        try:
            # Check if permission exists
            existing = self.permission_service.check_permission(role, path, service, method)
            if not existing:
                return {
                    "success": False,
                    "error": f"Permission not found for role '{role}' on {method} {service}/{path}"
                }
            
            # Delete permission using existing permission service
            success = self.permission_service.remove_permission(role, path, service, method)
            
            if success:
                return {
                    "success": True,
                    "message": f"Permission deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to delete permission from database"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete permission: {str(e)}"
            }

    def check_permission(self, role: str, path: str, service: str, method: str) -> Dict[str, Any]:
        """
        Kiểm tra permission
        
        Args:
            role: Role của user
            path: Đường dẫn route
            service: Tên service
            method: HTTP method
            
        Returns:
            Dictionary chứa kết quả
        """
        try:
            has_permission = self.permission_service.check_permission(role, path, service, method)
            
            return {
                "success": True,
                "has_permission": has_permission
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to check permission: {str(e)}"
            }

    def get_role_permissions(self, role: str) -> Dict[str, Any]:
        """
        Lấy tất cả permissions của một role
        
        Args:
            role: Role cần lấy permissions
            
        Returns:
            Dictionary chứa kết quả
        """
        try:
            permissions = self.permission_service.get_role_permissions(role)
            
            return {
                "success": True,
                "permissions": permissions,
                "role": role,
                "count": len(permissions)
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get role permissions: {str(e)}"
            }