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
                #  CHỈ kiểm tra connection, KHÔNG gọi full health check
                if hasattr(service, 'user_repository'):
                    # User service - test connection only
                    conn_status = service.user_repository.test_connection()
                    health_status[service_name] = {
                        "status": "healthy" if conn_status else "degraded",
                        "connection": "ok" if conn_status else "failed"
                    }
                elif hasattr(service, 'item_repository'):
                    # Item service - test connection only  
                    conn_status = service.item_repository.test_connection()
                    health_status[service_name] = {
                        "status": "healthy" if conn_status else "degraded",
                        "connection": "ok" if conn_status else "failed"
                    }
                else:
                    # Other services - basic check
                    health_status[service_name] = {
                        "status": "healthy",
                        "connection": "unknown"
                    }

                if health_status[service_name].get('status') != 'healthy':
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
            "timestamp": int(time.time())
        }

    def get_service_list(self) -> List[str]:
        """
        Lấy danh sách các service đã đăng ký

        Returns:
            Danh sách tên các service
        """
        return list(self.services.keys())

    def get_user_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê người dùng với error handling"""
        try:
            #  Enhanced error handling
            students = []
            teachers = []
            
            try:
                students = self.user_service.get_all_students(limit=1000)
            except Exception as e:
                print(f"Error getting students: {e}")
                students = []
            
            try:
                teachers = self.user_service.get_all_teachers(limit=1000)
            except Exception as e:
                print(f"Error getting teachers: {e}")
                teachers = []

            return {
                "total_students": len(students),
                "total_teachers": len(teachers),
                "total_users": len(students) + len(teachers),
                "last_updated": int(time.time()),
                "status": "healthy" if (students or teachers) else "degraded"
            }
        except Exception as e:
            print(f"Error in get_user_statistics: {e}")
            return {
                "total_students": 0,
                "total_teachers": 0,
                "total_users": 0,
                "error": str(e),
                "status": "error"
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

    
    def add_permission(self, role, path, service, method):
        """Thêm permission - chuẩn hóa params"""
        return self.permission_service.add_permission(role, path, service, method)

    def delete_permission(self, role, path, service, method):
        """Xóa permission"""
        return self.permission_service.delete_permission(role, path, service, method)

    def list_permissions(self, role=None, service=None):
        """List permissions với filters"""
        return self.permission_service.list_permissions(role, service)

    def check_permission(self, role, path, service, method):
        """Check permission"""
        return self.permission_service.check_permission(role, path, service, method)

    def get_role_permissions(self, role):
        """Get all permissions cho một role"""
        return self.permission_service.get_role_permissions(role)

    # User management
    def add_specialized_user(self, username: str, password: str, role: str) -> Dict[str, Any]:
        """Thêm user với role đặc biệt (teacher hoặc admin)"""
        try:
            # ✅ Validate role
            if role not in ['teacher', 'admin']:
                return {
                    "success": False,
                    "error": f"Invalid role '{role}'. Must be teacher or admin"
                }

            print(f"AdminService: Adding user {username} with role {role}")
            
            # ✅ Gọi signup service để tạo user với role đúng
            result = self.signup.add_specialized_user(username, password, role)
            
            if result:  # result là True/False
                print(f"AdminService: Successfully added {role} {username}")
                return {
                    "success": True,
                    "message": f"User '{username}' with role '{role}' added successfully",
                    "user": {
                        "username": username,
                        "role": role,
                        "created_at": int(time.time())
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to add user - user may already exist"
                }
        except Exception as e:
            print(f"Error in AdminService.add_specialized_user: {e}")
            return {
                "success": False,
                "error": f"Failed to add user: {str(e)}"
            }

    def change_user_role(self, user_id, new_role):
        """Thay đổi role của user"""
        return self.user_service.change_user_role(user_id, new_role)