from flask import jsonify
from .user_service import UserProfileService

class UserController:
    def __init__(self, user_service: UserProfileService):
        """
        Khởi tạo UserController với UserProfileService
        
        Parameters:
            user_service: Dịch vụ quản lý hồ sơ người dùng
        """
        self.user_service = user_service

    def login(self, data):
        """Xác thực người dùng"""
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing username or password"}), 400
        
        result = self.user_service.authenticate(data['username'], data['password'])
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify({"error": result.get('error', 'Authentication failed')}), 401

    def register(self, data):
        """Đăng ký người dùng mới"""
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        user_type = data.get('user_type', 'student')
        result = self.user_service.create_user(data, user_type)
        
        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify({"error": result.get('error', 'Registration failed')}), 400

    def get_user(self, user_id):
        """Lấy thông tin người dùng"""
        user_data = self.user_service.get_user(user_id)
        
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404

    def update_user(self, user_id, data):
        """Cập nhật hồ sơ người dùng"""
        if not data:
            return jsonify({"error": "No update data provided"}), 400
        
        result = self.user_service.update_profile(user_id, data)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            error_msg = result.get('error', 'Update failed')
            status_code = 404 if "not found" in error_msg else 400
            return jsonify({"error": error_msg}), status_code

    def delete_user(self, user_id):
        """Xóa người dùng"""
        result = self.user_service.delete_user(user_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            error_msg = result.get('error', 'Deletion failed')
            status_code = 404 if "not found" in error_msg else 400
            return jsonify({"error": error_msg}), status_code

    def get_all_students(self, limit=100, offset=0):
        """Lấy danh sách học sinh"""
        students = self.user_service.get_all_students(limit, offset)
        return jsonify({"students": students}), 200

    def get_all_teachers(self, limit=100, offset=0):
        """Lấy danh sách giáo viên"""
        teachers = self.user_service.get_all_teachers(limit, offset)
        return jsonify({"teachers": teachers}), 200

    def get_progress(self, user_id):
        """Lấy tiến độ học tập của học sinh"""
        result = self.user_service.get_student_progress(user_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            error_msg = result.get('error', 'Progress retrieval failed')
            status_code = 404 if "not found" in error_msg else 400
            return jsonify({"error": error_msg}), status_code

    def update_progress(self, user_id, data):
        """Cập nhật tiến độ học tập"""
        if not data or 'lesson_id' not in data or 'points' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        result = self.user_service.update_progress(
            user_id, 
            data['lesson_id'], 
            data['points']
        )
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            error_msg = result.get('error', 'Progress update failed')
            status_code = 404 if "not found" in error_msg else 400
            return jsonify({"error": error_msg}), status_code

    def buy_item(self, user_id, data):
        """Mua vật phẩm cho học sinh"""
        if not data or 'item' not in data or 'cost' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        result = self.user_service.buy_item_for_student(
            user_id, 
            data['item'], 
            data['cost']
        )
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify({"error": result.get('error', 'Item purchase failed')}), 400

    def check_health(self):
        """Kiểm tra trạng thái dịch vụ"""
        health_data = self.user_service.check_internal()
        status_code = 200 if health_data['status'] == 'healthy' else 503
        return jsonify(health_data), status_code