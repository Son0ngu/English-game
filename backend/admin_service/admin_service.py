import time
from typing import Dict, List, Any, Optional
from auth_service.login_and_register_service.signup_service import signup_service as signup
from auth_service.role_permission_service.permission_service import permission_service as permission_service
class AdminService:
    """
    Dịch vụ quản trị hệ thống.
    Lớp này cung cấp các chức năng quản trị như kiểm tra sức khỏe dịch vụ, 
    quản lý người dùng và thu thập số liệu thống kê hệ thống.
    
    Tích hợp chức năng ServiceRegistry để đăng ký và quản lý các dịch vụ.
    """
    def __init__(self, user_service):  # Loại bỏ type hint để tránh import
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

    def add_permission(self,roles, path, service, method):
        self.permission_service.add_permission_role(roles, path, service, method)

    def change_permission(self,roles, path, service, method):
        self.permission_service.change_permission_to_existing_path(roles, path, service, method)