from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, create_access_token
from flask import request

# Import các controller
from game_service.game_service_controller import game_service_controller
from progress_feedback.progress_service.progress_controller import ProgressController
from progress_feedback.progress_service.feedback_controller import FeedbackController
from admin_service.admin_controller import AdminController
from user_profile_service.user.user_controller import UserController
from user_profile_service.item.item_controller import ItemController
from classroom_service.classroom_controller import ClassroomController
from classroom_service.classroom_service import ClassroomService

# Import các service
from progress_feedback.progress_service.progress_service import ProgressService
from user_profile_service.user.user_service import UserProfileService
from user_profile_service.item.item_service import ItemService
from admin_service.admin_service import AdminService


class services_route:
    def __init__(self):
        try:
            # Khởi tạo các service
            self.game_service = game_service_controller()
            try:
                self.auth = auth_service_controller()
            except Exception as e:
                print("❌ ERROR while initializing self.auth:", str(e))
                self.auth = None
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

    def _get_user_id_from_jwt(self):
        """Helper method để lấy user_id từ JWT token"""
        try:
            username = get_jwt_identity()
            if not username:
                return None
            
            # Sử dụng auth service để convert username thành user_id
            if self.auth:
                return self.auth.get_id_from_username(username)
            return None
        except Exception as e:
            print(f"Error getting user_id from JWT: {e}")
            return None

    def handle_user_service(self, destination, data, method):
        """Điều hướng user service - Lấy user_id từ JWT"""
        if not self.user_controller:
            return jsonify({"error": "User service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.user_controller.check_health()
            
            # 🔄 CHUYỂN: Lấy user_id từ JWT
            elif destination == 'get' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.get_user(int(user_id))
                
            elif destination == 'update' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.update_user(int(user_id), data)
                
            elif destination == 'delete' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.delete_user(int(user_id))
            
            # 🔄 CHUYỂN: Stats từ JWT
            elif destination == 'stats-only' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.get_user_stats_only(int(user_id))
            
            # 🔄 CHUYỂN: Progress từ JWT
            elif destination == 'progress/update' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.update_progress(int(user_id), data)
                
            elif destination == 'progress/get' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.get_student_progress(int(user_id))
            
            # 🔄 CHUYỂN: Stats management từ JWT
            elif destination == 'stats/update' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.update_student_stats(int(user_id), data)
            
            # 🆕 Admin-only endpoints - lấy từ JSON data
            elif destination == 'get/admin' and method == 'POST':
                # Admin có thể get user khác
                jwt_role = get_jwt().get("role")
                if jwt_role != "admin":
                    return jsonify({"error": "Admin access required"}), 403
                user_id = data.get('user_id')
                if not user_id:
                    return jsonify({"error": "user_id required in JSON"}), 400
                return self.user_controller.get_user(int(user_id))
            
            # List users có thể giữ GET
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
        """Điều hướng admin service - TẤT CẢ từ JSON"""
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
            
            # 🔄 CHUYỂN: Change user role từ JSON
            elif destination == 'users/change-role' and method == 'POST':
                return self.admin_controller.change_user_role(data)
            
            # ✨ MỚI: Add specialized user từ JSON
            elif destination == 'users/add' and method == 'POST':
                return self.admin_controller.add_specialized_user(data)
            
            # 🎯 PERMISSION MANAGEMENT ENDPOINTS
            
            # Add permission
            elif destination == 'permissions/add' and method == 'POST':
                return self.admin_controller.add_permission(data)
            
            # List permissions (with optional filters)
            elif destination == 'permissions/list' and method == 'POST':
                return self.admin_controller.list_permissions(data)
            
            # Delete permission
            elif destination == 'permissions/delete' and method == 'POST':
                return self.admin_controller.delete_permission(data)
            
            # Check permission
            elif destination == 'permissions/check' and method == 'POST':
                return self.admin_controller.check_permission(data)
            
            # Get role permissions
            elif destination == 'permissions/role' and method == 'POST':
                return self.admin_controller.get_role_permissions(data)
            
            else:
                return jsonify({"error": f"Admin endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Admin service error: {str(e)}"}), 500

    def handle_progress_service(self, destination, data, method):
        """Điều hướng progress service - Lấy user_id từ JWT"""
        if not self.progress_controller:
            return jsonify({"error": "Progress service not available"}), 503
        
        try:
            if destination == 'health' and method == 'GET':
                return self.progress_controller.check_health()

            elif destination == 'record' and method == 'POST':
                return self.progress_controller.record_activity(data)
            
            # 🔄 CHUYỂN: Lấy user_id từ JWT
            elif destination == 'user/progress' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.progress_controller.get_user_progress(user_id)
            
            elif destination == 'user/grade' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                difficulty = data.get('difficulty')
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                if not difficulty:
                    return jsonify({"error": "difficulty required in JSON"}), 400
                return self.progress_controller.get_average_grade(user_id, difficulty)
            
            elif destination == 'user/performance' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.progress_controller.get_performance_by_difficulty(user_id)
            
            else:
                return jsonify({"error": f"Progress endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Progress service error: {str(e)}"}), 500

    def handle_feedback_service(self, destination, data, method):
        """Điều hướng feedback service - Lấy user_id từ JWT"""
        if not self.feedback_controller:
            return jsonify({"error": "Feedback service not available"}), 503
        
        try:
            if destination == 'health' and method == 'GET':
                return self.feedback_controller.check_health()
            elif destination == 'generate' and method == 'POST':
                return self.feedback_controller.generate_feedback(data)
            
            # 🔄 CHUYỂN: Lấy user_id từ JWT
            elif destination == 'user/feedback' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.feedback_controller.get_user_feedback(user_id)
            
            # Get feedback by ID - từ JSON data (có thể cần authorization check)
            elif destination == 'get' and method == 'POST':
                feedback_id = data.get('feedback_id')
                if not feedback_id:
                    return jsonify({"error": "feedback_id required in JSON"}), 400
                return self.feedback_controller.get_feedback_by_id(feedback_id)
            
            else:
                return jsonify({"error": f"Feedback endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Feedback service error: {str(e)}"}), 500

    def handle_item_service(self, destination, data, method):
        """Điều hướng item service - Lấy user_id từ JWT"""
        if not self.item_controller:
            return jsonify({"error": "Item service not available"}), 503
            
        try:
            if destination == 'health' and method == 'GET':
                return self.item_controller.check_health()
            
            # 🔄 CHUYỂN: Lấy user_id từ JWT
            elif destination == 'user/weapons' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.item_controller.get_user_items(str(user_id))
            
            elif destination == 'user/upgradeable' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.item_controller.get_upgradeable_items(str(user_id))
            
            elif destination == 'user/available' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.item_controller.get_available_weapons(str(user_id))
            
            # Get item details - từ JSON data (public)
            elif destination == 'get' and method == 'POST':
                item_id = data.get('item_id')
                if not item_id:
                    return jsonify({"error": "item_id required in JSON"}), 400
                return self.item_controller.get_item(item_id)
            
            # Select weapon - user_id từ JWT
            elif destination == 'select' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                data['user_id'] = int(user_id)  # Override user_id từ JWT
                return self.item_controller.select_weapon(data)
            
            # Upgrade weapon - user_id từ JWT
            elif destination == 'upgrade' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                data['user_id'] = int(user_id)  # Override user_id từ JWT
                return self.item_controller.upgrade_weapon(data)
            
            else:
                return jsonify({"error": f"Item endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Item service error: {str(e)}"}), 500

    def game_service(self, destination, data, method):
        """Điều hướng game service - TẤT CẢ từ JSON"""
        try:
            if destination == 'health' and method == 'GET':
                return jsonify({"status": "healthy", "service": "game"}), 200
                
            elif destination == 'newroom' and method == 'POST':
                if not self.game_service:
                    return jsonify({"error": "Game service not available"}), 503
                    
                student_id = get_jwt_identity()
                if student_id:
                    self.game_service.create_game_room(student_id)
                    return jsonify({"message": "Game room created successfully"}), 200
                else:
                    return jsonify({"error": "Student ID is required"}), 400

            # 🔄 CHUYỂN: Check answer từ JSON
            elif destination == "check_answer" and method == "POST":
                session_id = data.get('session_id')
                answer = data.get('answer')
                if not session_id or not answer:
                    return jsonify({"error": "session_id and answer required in JSON"}), 400
                return self.game_service.check_answer(session_id, answer)

            # 🔄 CHUYỂN: Get question từ JSON
            elif destination == "get_question" and method == 'POST':
                session_id = data.get('session_id')
                if not session_id:
                    return jsonify({"error": "session_id required in JSON"}), 400
                return self.game_service.get_question(session_id)
            
            else:
                return jsonify({"error": "Game endpoint not implemented"}), 501
        except Exception as e:
            return jsonify({"error": f"Game service error: {str(e)}"}), 500

    def classroom_service(self, destination, data, method):
        """Điều hướng classroom service - Lấy user_id từ JWT khi cần"""
        if not self.classroom_controller:
            return jsonify({"error": "Classroom service not available"}), 503
            
        try:
            if destination == "health" and method == "GET":
                return self.classroom_controller.check_health()
            elif destination == "create" and method == "POST":
                return self.classroom_controller.create_class(data)
            elif destination == "join" and method == "POST":
                return self.classroom_controller.join_class(data)
            
            # Class-based endpoints - từ JSON data
            elif destination == "students" and method == "POST":
                class_id = data.get('class_id')
                if not class_id:
                    return jsonify({"error": "class_id required in JSON"}), 400
                return self.classroom_controller.get_students(class_id)
            
            elif destination == "dashboard" and method == "POST":
                class_id = data.get('class_id')
                if not class_id:
                    return jsonify({"error": "class_id required in JSON"}), 400
                return self.classroom_controller.get_dashboard(class_id)
            
            # 🔄 CHUYỂN: Student classes từ JWT
            elif destination == "student/classes" and method == "POST":
                student_id = self._get_user_id_from_jwt()
                if not student_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.classroom_controller.get_student_classes(student_id)
            
            elif destination == "questions" and method == "POST":
                class_id = data.get('class_id')
                if not class_id:
                    return jsonify({"error": "class_id required in JSON"}), 400
                return self.classroom_controller.get_questions_by_criteria(class_id)
            
            else:
                return jsonify({"error": f"Classroom endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Classroom service error: {str(e)}"}), 500

    # Placeholder methods for services chưa implement
    def authenticating_service(self,destination, data, method):
        print(1)
        if destination == 'login' and method == 'POST':
            if data.get('username') and data.get('password'):
                username = data.get('username')
                password = data.get('password')
                if self.auth.login(username, password):
                    id = self.auth.get_id_from_username(username)
                    role = self.auth.get_role_from_id(id)
                    additional_claims = {"role": role}
                    access_token = create_access_token(identity=username,additional_claims=additional_claims)
                    print("Crafted access token:", access_token," (service_route)")
                    return {"access_token": access_token}, 200
                else:
                    print("Invalid credentials (service_route)")
                    return {"error": "Invalid credentials"}, 401
            return None

        # Get role from JWT
        # claims = get_jwt()
        # claims.get("role")

        if destination == "signup" and method == 'POST':
            if data.get('username') and data.get('password'):
                username = data.get('username')
                password = data.get('password')
                if self.auth.sign_up(username, password):
                    print("User created successfully (service_route)")
                    id = self.auth.get_id_from_username(username)
                    role = self.auth.get_role_from_id(id)
                    additional_claims = {"role": role}
                    access_token = create_access_token(identity=username, additional_claims=additional_claims)
                    print("Crafted access token:", access_token, " (service_route)")
                    return {"message": "User created successfully","access_token":access_token}, 200
                else:
                    print("User already exists (service_route)")
                    return {"error": "User already exists"}, 400
            return None

        if destination == "add_permission" and method == 'POST':
            jwt_role = get_jwt().get("role")
            role = data.get("role")
            path = data.get("path")
            service = data.get("service")
            method = data.get("method")
            if jwt_role =="admin":
                self.auth.add_permission(role, path, service, method)
                print("Permission added successfully (service_route)")
                return {"message": "Permission added successfully"}, 200
        return None
    
    def course_service(self, destination, data, method):
        if destination == 'health' and method == 'GET':
            return jsonify({"status": "healthy", "service": "course"}), 200
        return jsonify({"error": "Course service not implemented"}), 501
