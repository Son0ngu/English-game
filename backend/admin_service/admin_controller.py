from flask import jsonify
from admin_service.admin_service import AdminService

class AdminController:
    def __init__(self, admin_service: AdminService):
        """
        Khởi tạo AdminController với AdminService.
        
        Parameters:
            admin_service: Dịch vụ quản trị dùng để kiểm tra sức khỏe và quản lý người dùng
        """
        self.admin_service = admin_service

    def check_health(self, service_name=None):
        """
        Kiểm tra sức khỏe của các dịch vụ đã đăng ký.
        
        Parameters:
            service_name: Tên dịch vụ cụ thể cần kiểm tra (nếu None, kiểm tra tất cả)
            
        Returns:
            Kết quả kiểm tra sức khỏe dạng JSON response với status code
        """
        health_data = self.admin_service.check_service_availability(service_name)
        
        # Xác định trạng thái tổng thể dựa trên trạng thái của từng dịch vụ
        all_healthy = all(data.get('status') == 'healthy' 
                         for data in health_data.values())
        
        return jsonify({
            "overall_status": "healthy" if all_healthy else "degraded",
            "services": health_data,
            "timestamp": int(self.admin_service._startup_time)
        }), 200

    def list_services(self):
        """
        Liệt kê tất cả các dịch vụ đã đăng ký.
        
        Returns:
            Danh sách các dịch vụ đã đăng ký dạng JSON response
        """
        return jsonify({
            "services": list(self.admin_service.services.keys())
        }), 200

    def get_system_stats(self):
        """
        Lấy thống kê tổng quan của hệ thống.
        
        Returns:
            Thống kê hệ thống dạng JSON response
        """
        return jsonify(self.admin_service.get_system_stats()), 200

    def list_users(self, role=None):
        """
        Lấy danh sách người dùng, có thể lọc theo vai trò.
        
        Parameters:
            role: Vai trò người dùng ('student', 'teacher')
            
        Returns:
            Danh sách người dùng dạng JSON response
        """
        users = self.admin_service.get_users(role)
        return jsonify({"users": users}), 200
        
    def change_user_role(self, data):
        """
        Thay đổi vai trò của người dùng.
        
        Parameters:
            data: Dictionary chứa user_id và new_role
            
        Returns:
            Kết quả thay đổi vai trò dạng JSON response
        """
        if 'user_id' not in data or 'new_role' not in data:
            return jsonify({"error": "user_id và new_role là bắt buộc"}), 400
            
        success = self.admin_service.change_user_role(data['user_id'], data['new_role'])
        
        if success:
            return jsonify({"message": "Đã cập nhật vai trò thành công"}), 200
        else:
            return jsonify({"error": "Không thể cập nhật vai trò"}), 500