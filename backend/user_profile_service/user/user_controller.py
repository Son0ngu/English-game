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
        """Cập nhật tiến độ học tập với auto weapon upgrade"""
        try:
            lesson_id = data.get('lesson_id', 'unknown')
            points = data.get('points', 0)
            
            if points <= 0:
                return jsonify({"error": "Points must be positive"}), 400
            
            # Update progress với weapon upgrade
            result = self.user_service.update_progress_with_weapon_upgrade(user_id, lesson_id, points)
            
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