import time
from typing import Dict, List, Any, Optional
from .user_service import UserProfileService
from ..models.user import TeacherProfile

class AdminService:
    """
    Dịch vụ quản trị hệ thống.
    Lớp này cung cấp các chức năng quản trị như kiểm tra sức khỏe dịch vụ, 
    quản lý người dùng và thu thập số liệu thống kê hệ thống.
    
    Tích hợp chức năng ServiceRegistry để đăng ký và quản lý các dịch vụ.
    """
    def __init__(self, user_service=None):
        """
        Khởi tạo dịch vụ quản trị.
        
        Tham số:
            user_service: Dịch vụ quản lý người dùng (tùy chọn)
            
        Thuộc tính:
            _startup_time: Thời điểm khởi động dịch vụ
            _last_error: Lưu trữ lỗi gần nhất để theo dõi trạng thái
            _stats: Thống kê sử dụng dịch vụ (số lần kiểm tra dịch vụ, hành động quản lý người dùng)
            services: Danh sách các dịch vụ đã đăng ký để kiểm tra sức khỏe
        """
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"service_checks": 0, "user_management_actions": 0, "service_registrations": 0}
        self.user_service = user_service
        self.services = {}  # Registry for services
        
        # Đăng ký user_service nếu có
        if user_service:
            self.register("users", user_service)
            
    def register(self, name: str, service) -> Any:
        """
        Đăng ký một dịch vụ để theo dõi và kiểm tra sức khỏe.
        
        Tham số:
            name: Tên định danh của dịch vụ
            service: Đối tượng dịch vụ cần đăng ký
            
        Trả về:
            service: Đối tượng service đã đăng ký (để hỗ trợ method chaining)
            
        Chức năng:
            Thêm dịch vụ vào danh sách services để có thể kiểm tra sức khỏe sau này
        """
        self.services[name] = service
        self._stats["service_registrations"] += 1
        return service
        
    # Giữ lại phương thức register_service để tương thích ngược với code cũ
    def register_service(self, name: str, service) -> None:
        """
        Đăng ký một dịch vụ (alias của register để tương thích ngược).
        """
        return self.register(name, service)
        
    def check_service(self, service_name: str = None) -> dict:
        """
        Kiểm tra trạng thái hoạt động của các dịch vụ đã đăng ký.
        
        Tham số:
            service_name: Tên của dịch vụ cụ thể cần kiểm tra (nếu None sẽ kiểm tra tất cả)
            
        Trả về:
            Dictionary chứa kết quả kiểm tra cho từng dịch vụ
        """
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
    
    # Giữ lại phương thức check_service_availability để tương thích ngược
    def check_service_availability(self, service_name: str = None) -> dict:
        """
        Kiểm tra trạng thái hoạt động (alias của check_service để tương thích ngược).
        """
        return self.check_service(service_name)
    
    def get_users(self, role: str = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách người dùng, có thể lọc theo vai trò.
        
        Tham số:
            role: Vai trò của người dùng cần lọc ('student', 'teacher')
            
        Trả về:
            Danh sách thông tin người dùng dạng dictionary
        """
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
        """
        Thay đổi vai trò của người dùng.
        
        Tham số:
            user_id: ID của người dùng cần thay đổi vai trò
            new_role: Vai trò mới ('student', 'teacher', v.v.)
            
        Trả về:
            True nếu thành công, False nếu thất bại
        """
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
        """
        Lấy thống kê tổng quan về hệ thống.
        
        Trả về:
            Dictionary chứa thống kê hệ thống như thời gian hoạt động,
            danh sách dịch vụ đã đăng ký, và thống kê người dùng nếu có
        """
        try:
            stats = {
                "uptime": time.time() - self._startup_time,
                "registered_services": list(self.services.keys()),
                "service_stats": self._stats
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
        """
        Kiểm tra sức khỏe nội bộ của dịch vụ quản trị.
        
        Trả về:
            Dictionary chứa thông tin sức khỏe dịch vụ
        """
        return {
            "status": "healthy" if not self._last_error else "degraded",
            "uptime": time.time() - self._startup_time,
            "stats": self._stats,
            "registered_services_count": len(self.services),
            "last_error": str(self._last_error) if self._last_error else None,
            "details": "Admin service running normally"
        }