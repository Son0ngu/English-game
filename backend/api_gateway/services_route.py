from flask import jsonify

# Import các controller
import game_service.gameroom.game_room_controller as game_room_controller
from progressandfeedback.progress_controller import ProgressController
from progressandfeedback.feedback_controller import FeedbackController
from admin_service.admin_controller import AdminController
from userProfile_service.user.user_controller import UserController
from userProfile_service.item.item_controller import ItemController
from classroom_service.classroom_controller import ClassroomController
from classroom_service.classroom_service import ClassroomService

# Import các service
from progressandfeedback.progress_service.progress_service import ProgressService
from userProfile_service.user.user_service import UserProfileService
from userProfile_service.item.item_service import ItemService
from admin_service.admin_service import AdminService

class services_route:
    def __init__(self):
        try:
            # Khởi tạo các service
            self.game_room_controller = game_room_controller.game_room_controller()
            
            # Core services
            self.user_service_obj = UserProfileService()
            self.item_service_obj = ItemService()
            self.admin_service_obj = AdminService(self.user_service_obj)
            
            # Progress và feedback services
            try:
                progress_service = ProgressService(self.user_service_obj, self.admin_service_obj)
                self.progress_controller = ProgressController(progress_service)
                self.feedback_controller = FeedbackController(progress_service)
            except:
                # Fallback nếu import thất bại
                class MockProgressController:
                    def check_health(self):
                        return jsonify({"status": "healthy", "service": "progress"}), 200
                    def record_activity(self, data):
                        return jsonify({"error": "Progress service not implemented"}), 501
                    def get_user_progress(self, user_id):
                        return jsonify({"error": "Progress service not implemented"}), 501
                    def get_average_grade(self, user_id, difficulty):
                        return jsonify({"error": "Progress service not implemented"}), 501
                    def get_performance_by_difficulty(self, user_id):
                        return jsonify({"error": "Progress service not implemented"}), 501
                
                class MockFeedbackController:
                    def check_health(self):
                        return jsonify({"status": "healthy", "service": "feedback"}), 200
                    def generate_feedback(self, data):
                        return jsonify({"error": "Feedback service not implemented"}), 501
                    def get_user_feedback(self, user_id):
                        return jsonify({"error": "Feedback service not implemented"}), 501
                    def get_feedback_by_id(self, feedback_id):
                        return jsonify({"error": "Feedback service not implemented"}), 501
                
                self.progress_controller = MockProgressController()
                self.feedback_controller = MockFeedbackController()
            
            # Classroom service
            try:
                classroom_service = ClassroomService(self.user_service_obj)
                self.classroom_controller = ClassroomController(classroom_service)
            except:
                # Fallback
                class MockClassroomController:
                    def check_health(self):
                        return jsonify({"status": "healthy", "service": "classroom"}), 200
                    def create_class(self, data):
                        return jsonify({"error": "Classroom service not implemented"}), 501
                    def join_class(self, data):
                        return jsonify({"error": "Classroom service not implemented"}), 501
                    def get_students(self, class_id):
                        return jsonify({"error": "Classroom service not implemented"}), 501
                    def get_dashboard(self, class_id):
                        return jsonify({"error": "Classroom service not implemented"}), 501
                    def get_student_classes(self, student_id):
                        return jsonify({"error": "Classroom service not implemented"}), 501
                    def get_questions_by_criteria(self, class_id):
                        return jsonify({"error": "Classroom service not implemented"}), 501
                
                self.classroom_controller = MockClassroomController()
            
            # Đăng ký services với admin
            self.admin_service_obj.register_service("user", self.user_service_obj)
            self.admin_service_obj.register_service("item", self.item_service_obj)
            self.admin_service_obj.register_service("admin", self.admin_service_obj)
            
            # Khởi tạo controllers
            self.user_controller = UserController(self.user_service_obj)
            self.item_controller = ItemController(self.item_service_obj)
            self.admin_controller = AdminController(self.admin_service_obj)
            
        except Exception as e:
            # Tạo fallback controllers nếu có lỗi
            self.user_controller = None
            self.admin_controller = None
            self.progress_controller = None
            self.feedback_controller = None
            self.item_controller = None
            self.classroom_controller = None
            self.game_room_controller = None

    def handle_user_service(self, destination, data, method):
        """Điều hướng user service"""
        if not self.user_controller:
            return jsonify({"error": "User service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.user_controller.check_health()
            
            # User read/update/delete operations
            elif method == 'GET' and destination.isdigit():
                return self.user_controller.get_user(int(destination))
            elif method == 'PUT' and destination.isdigit():
                return self.user_controller.update_user(int(destination), data)
            elif method == 'DELETE' and destination.isdigit():
                return self.user_controller.delete_user(int(destination))
            
            # Get user stats (ATK & HP only)
            elif destination.endswith('/stats-only') and method == 'GET':
                user_id = int(destination.split('/')[0])
                return self.user_controller.get_user_stats_only(user_id)
            
            # Progress management với auto weapon upgrade
            elif destination.endswith('/progress') and method == 'POST':
                user_id = int(destination.split('/')[0])
                return self.user_controller.update_progress(user_id, data)
            elif destination.endswith('/progress') and method == 'GET':
                user_id = int(destination.split('/')[0])
                return self.user_controller.get_student_progress(user_id)
            
            # BỎ: Money management endpoints
            # elif destination.endswith('/money') and method == 'POST':
            
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

    def handle_admin_service(self, destination, data, method):
        """Điều hướng admin service"""
        if not self.admin_controller:
            return jsonify({"error": "Admin service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                service_name = data.get('service') if data else None
                return self.admin_controller.check_health(service_name)
            elif destination == 'services' and method == 'GET':
                return self.admin_controller.list_services()
            elif destination == 'system-stats' and method == 'GET':
                return self.admin_controller.get_system_stats()
            elif destination == 'users' and method == 'GET':
                role = data.get('role') if data else None
                return self.admin_controller.list_users(role)
            elif destination == 'users/change-role' and method == 'PUT':
                return self.admin_controller.change_user_role(data)
            else:
                return jsonify({"error": f"Admin endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Admin service error: {str(e)}"}), 500

    def handle_progress_service(self, destination, data, method):
        """Điều hướng progress service"""
        if not self.progress_controller:
            return jsonify({"error": "Progress service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.progress_controller.check_health()
            elif destination == 'record' and method == 'POST':
                return self.progress_controller.record_activity(data)
            elif destination.startswith('user/') and method == 'GET':
                user_id = destination.split('/')[-1]
                return self.progress_controller.get_user_progress(user_id)
            elif destination.startswith('grade/') and method == 'GET':
                path_parts = destination.split('/')
                if len(path_parts) < 3:
                    return jsonify({"error": "User ID and difficulty are required"}), 400
                user_id = path_parts[1]
                difficulty = path_parts[2]
                return self.progress_controller.get_average_grade(user_id, difficulty)
            elif destination.startswith('performance/') and method == 'GET':
                user_id = destination.split('/')[-1]
                return self.progress_controller.get_performance_by_difficulty(user_id)
            else:
                return jsonify({"error": f"Progress endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Progress service error: {str(e)}"}), 500

    def handle_feedback_service(self, destination, data, method):
        """Điều hướng feedback service"""
        if not self.feedback_controller:
            return jsonify({"error": "Feedback service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.feedback_controller.check_health()
            elif destination == 'generate' and method == 'POST':
                return self.feedback_controller.generate_feedback(data)
            elif destination.startswith('user/') and method == 'GET':
                user_id = destination.split('/')[-1]
                return self.feedback_controller.get_user_feedback(user_id)
            elif method == 'GET' and destination:
                feedback_id = destination
                return self.feedback_controller.get_feedback_by_id(feedback_id)
            else:
                return jsonify({"error": f"Feedback endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Feedback service error: {str(e)}"}), 500

    def handle_item_service(self, destination, data, method):
        """Điều hướng item service"""
        if not self.item_controller:
            return jsonify({"error": "Item service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.item_controller.check_health()
            
            # Get user weapons
            elif destination.startswith('user/') and method == 'GET':
                user_id = destination.split('/')[-1]
                if 'upgradeable' in destination:
                    return self.item_controller.get_upgradeable_items(user_id)
                elif 'available' in destination:
                    return self.item_controller.get_available_weapons(user_id)
                else:
                    return self.item_controller.get_user_items(user_id)
            
            # Select weapon from 3 options (NEW)
            elif destination == 'select' and method == 'POST':
                return self.item_controller.select_weapon(data)
            
            # Upgrade weapon (level up)
            elif destination == 'upgrade' and method == 'POST':
                return self.item_controller.upgrade_weapon(data)
            
            # Get weapon details
            elif method == 'GET' and destination:
                return self.item_controller.get_item(destination)
            
            else:
                return jsonify({"error": f"Item endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Item service error: {str(e)}"}), 500

    def game_service(self, destination, data, method):
        """Điều hướng game service"""
        try:
            if destination == 'newroom' and method == 'POST':
                if not self.game_room_controller:
                    return jsonify({"error": "Game service not available"}), 503
                    
                student_id = data.get('student_id')
                if student_id:
                    self.game_room_controller.create_game_room(student_id)
                    return jsonify({"message": "Game room created successfully"}), 200
                else:
                    return jsonify({"error": "Student ID is required"}), 400
            elif destination == 'health' and method == 'GET':
                return jsonify({"status": "healthy", "service": "game"}), 200
            else:
                return jsonify({"error": "Game endpoint not implemented"}), 501
        except Exception as e:
            return jsonify({"error": f"Game service error: {str(e)}"}), 500

    def classroom_service(self, destination, data, method):
        """Điều hướng classroom service"""
        if not self.classroom_controller:
            return jsonify({"error": "Classroom service not available"}), 503
            
        try:
            if destination == "health" and method == "GET":
                return self.classroom_controller.check_health()
            elif destination == "" and method == "POST":
                return self.classroom_controller.create_class(data)
            elif destination == "join" and method == "POST":
                return self.classroom_controller.join_class(data)
            elif destination.endswith("/students") and method == "GET":
                class_id = destination.split("/")[0]
                return self.classroom_controller.get_students(class_id)
            elif destination.endswith("/dashboard") and method == "GET":
                class_id = destination.split("/")[0]
                return self.classroom_controller.get_dashboard(class_id)
            elif destination.startswith("student/") and destination.endswith("/classes") and method == "GET":
                student_id = destination.split("/")[1]
                return self.classroom_controller.get_student_classes(student_id)
            elif destination.startswith("question/") and method == "GET":
                class_id = destination.split("/")[1]
                return self.classroom_controller.get_questions_by_criteria(class_id)
            else:
                return jsonify({"error": f"Classroom endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Classroom service error: {str(e)}"}), 500

    # Placeholder methods for services chưa implement
    def auth_service(self, destination, data, method):
        if destination == 'health' and method == 'GET':
            return jsonify({"status": "healthy", "service": "auth"}), 200
        return jsonify({"error": "Auth service not implemented"}), 501
    
    def course_service(self, destination, data, method):
        if destination == 'health' and method == 'GET':
            return jsonify({"status": "healthy", "service": "course"}), 200
        return jsonify({"error": "Course service not implemented"}), 501
