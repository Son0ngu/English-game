from flask import jsonify
from .user_service import UserProfileService  # Import từ cùng thư mục
import time

class UserController:
    def __init__(self, user_service: UserProfileService):
        """
        Khởi tạo UserController với UserProfileService
        
        Parameters:
            user_service: Dịch vụ quản lý hồ sơ người dùng
        """
        self.user_service = user_service

    def check_health(self):
        """Kiểm tra trạng thái dịch vụ"""
        try:
            health_data = self.user_service.check_internal()
            status_code = 200 if health_data['status'] == 'healthy' else 503
            return jsonify(health_data), status_code
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 503

    def get_user(self, user_id):
        """Lấy thông tin người dùng"""
        try:
            user_data = self.user_service.get_user(user_id)
            
            if user_data:
                return jsonify(user_data), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Get user error: {str(e)}"}), 500

    def update_user(self, user_id, data):
        """Cập nhật thông tin người dùng"""
        try:
            if not data:
                return jsonify({"error": "No data provided for update"}), 400
            
            result = self.user_service.update_profile(user_id, data)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({"error": result.get('error', 'Update failed')}), 400
        except Exception as e:
            return jsonify({"error": f"Update user error: {str(e)}"}), 500

    def update_progress(self, user_id, data):
        """Cập nhật tiến độ học tập của học sinh"""
        try:
            lesson_id = data.get('lesson_id', 'unknown')
            points = data.get('points', 0)
            
            if points <= 0:
                return jsonify({"error": "Points must be positive"}), 400
            
            result = self.user_service.update_progress(user_id, lesson_id, points)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({"error": result.get('error', 'Progress update failed')}), 400
        except Exception as e:
            return jsonify({"error": f"Progress update error: {str(e)}"}), 500

    def get_student_progress(self, user_id):
        """Lấy tiến độ học tập của học sinh"""
        try:
            result = self.user_service.get_student_progress(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({"error": result.get('error', 'Failed to get progress')}), 404
        except Exception as e:
            return jsonify({"error": f"Get progress error: {str(e)}"}), 500

    def update_student_money(self, user_id, data):
        """Cập nhật tiền của học sinh"""
        try:
            amount = data.get('amount', 0)
            operation = data.get('operation', 'add')
            
            if amount < 0:
                return jsonify({"error": "Amount must be non-negative"}), 400
            
            result = self.user_service.update_student_money(user_id, amount, operation)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                status_code = 402 if "Insufficient funds" in result.get('error', '') else 400
                return jsonify(result), status_code
        except Exception as e:
            return jsonify({"error": f"Money update error: {str(e)}"}), 500

    def update_student_stats(self, user_id, data):
        """Cập nhật stats game của học sinh (HP, ATK)"""
        try:
            hp = data.get('hp')
            atk = data.get('atk')
            
            if hp is None and atk is None:
                return jsonify({"error": "Must provide hp or atk to update"}), 400
            
            result = self.user_service.update_student_stats(user_id, hp, atk)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({"error": result.get('error', 'Stats update failed')}), 400
        except Exception as e:
            return jsonify({"error": f"Stats update error: {str(e)}"}), 500

    def get_all_students(self, limit=100, offset=0):
        """Lấy danh sách học sinh"""
        try:
            students = self.user_service.get_all_students(limit, offset)
            return jsonify({"students": students, "count": len(students)}), 200
        except Exception as e:
            return jsonify({"error": f"Get students error: {str(e)}"}), 500

    def get_all_teachers(self, limit=100, offset=0):
        """Lấy danh sách giáo viên"""
        try:
            teachers = self.user_service.get_all_teachers(limit, offset)
            return jsonify({"teachers": teachers, "count": len(teachers)}), 200
        except Exception as e:
            return jsonify({"error": f"Get teachers error: {str(e)}"}), 500

    def delete_user(self, user_id):
        """Xóa người dùng"""
        try:
            result = self.user_service.delete_user(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({"error": result.get('error', 'Delete failed')}), 404
        except Exception as e:
            return jsonify({"error": f"Delete user error: {str(e)}"}), 500

    def get_user_stats(self):
        """Lấy thống kê người dùng"""
        try:
            result = self.user_service.get_user_count()
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify({"error": result.get('error', 'Failed to get stats')}), 500
        except Exception as e:
            return jsonify({"error": f"Get stats error: {str(e)}"}), 500

    def handle_user_service(self, destination, data, method):
        """Điều hướng user service - bỏ user creation"""
        if not self.user_controller:
            return jsonify({"error": "User service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.user_controller.check_health()
            
            # User read/update/delete operations (NO CREATE)
            elif method == 'GET' and destination.isdigit():
                return self.user_controller.get_user(int(destination))
            elif method == 'PUT' and destination.isdigit():
                return self.user_controller.update_user(int(destination), data)
            elif method == 'DELETE' and destination.isdigit():
                return self.user_controller.delete_user(int(destination))
            
            # Progress management
            elif destination.endswith('/progress') and method == 'POST':
                user_id = int(destination.split('/')[0])
                return self.user_controller.update_progress(user_id, data)
            elif destination.endswith('/progress') and method == 'GET':
                user_id = int(destination.split('/')[0])
                return self.user_controller.get_student_progress(user_id)
            
            # Money management
            elif destination.endswith('/money') and method == 'POST':
                user_id = int(destination.split('/')[0])
                return self.user_controller.update_student_money(user_id, data)
            
            # Stats management
            elif destination.endswith('/stats') and method == 'POST':
                user_id = int(destination.split('/')[0])
                return self.user_controller.update_student_stats(user_id, data)
            
            # List users
            elif destination == 'students' and method == 'GET':
                limit = data.get('limit', 100) if data else 100
                offset = data.get('offset', 0) if data else 0
                return self.user_controller.get_all_students(limit, offset)
            elif destination == 'teachers' and method == 'GET':
                limit = data.get('limit', 100) if data else 100
                offset = data.get('offset', 0) if data else 0
                return self.user_controller.get_all_teachers(limit, offset)
            elif destination == 'stats' and method == 'GET':
                return self.user_controller.get_user_stats()
            
            else:
                return jsonify({"error": f"User endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"User service error: {str(e)}"}), 500