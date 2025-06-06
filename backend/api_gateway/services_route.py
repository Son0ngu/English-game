from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, create_access_token, jwt_required, verify_jwt_in_request
from flask import request

from auth_service.auth_service_controller import auth_service_controller
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
                {
                    "status": "healthy",
                    "uptime_seconds": 123456,
                    "repository_status": "connected"
                }
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
                classroom_service = ClassroomService()
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
            verify_jwt_in_request()
            user_id = get_jwt_identity()
                  
            if user_id:
                return str(user_id)  
            
            return None
        except Exception as e:
            print(f"Error getting user_id from JWT: {e}")
            return None

    def handle_user_service(self, destination, data, method):
        """Điều hướng user service - LOẠI BỎ progress endpoints cũ"""
        if not self.user_controller:
            return jsonify({"error": "User service not available"}), 503
        
        try:
            if destination == 'health' and method == 'GET':
                return self.user_controller.check_health()
            
            
            elif destination == 'get' and method == 'POST':
                try:
                    user_id = self._get_user_id_from_jwt()
                    if not user_id:
                        return jsonify({"error": "Authentication required - Please login first"}), 401
                    return self.user_controller.get_user(user_id)
                except Exception as e:
                    return jsonify({"error": f"JWT Error: {str(e)}"}), 401
                
            elif destination == 'update' and method == 'POST':
                try:
                    user_id = self._get_user_id_from_jwt()
                    if not user_id:
                        return jsonify({"error": "Authentication required - Please login first"}), 401
                    return self.user_controller.update_user(user_id, data)
                except Exception as e:
                    return jsonify({"error": f"JWT Error: {str(e)}"}), 401
            
            elif destination == 'delete' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.delete_user(user_id)
            
            elif destination == 'stats-only' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.user_controller.get_user_stats_only(user_id)
            
            # ❌ XÓA HOÀN TOÀN: Các progress endpoints cũ 
            elif destination in ['progress/update', 'progress/get']:
                return jsonify({
                    "message": "Progress endpoints moved to /progress service",
                    "deprecated": True,
                    "redirect": {
                        "progress/update": "POST /progress/complete-map",
                        "progress/get": "POST /progress/user/maps"
                    }
                }), 410  # Gone
        
            elif destination == 'get/admin' and method == 'POST':
                jwt_role = get_jwt().get("role")
                if jwt_role != "admin":
                    return jsonify({"error": "Admin access required"}), 403
                user_id = data.get('user_id')
                if not user_id:
                    return jsonify({"error": "user_id required in JSON"}), 400
                return self.user_controller.get_user(user_id)
          
            elif destination == 'students' and method == 'POST':
                print('post')
                from flask import request
                limit = request.args.get('limit', 100, type=int)
                offset = request.args.get('offset', 0, type=int)
                print(data)
                return self.user_controller.get_all_students(limit, offset)
                
            elif destination == 'teachers' and method == 'GET':
                from flask import request
                limit = request.args.get('limit', 100, type=int)
                offset = request.args.get('offset', 0, type=int)
                return self.user_controller.get_all_teachers(limit, offset)
                
            elif destination == 'stats' and method == 'GET':
                return self.user_controller.get_user_stats()
            
            else:
                return jsonify({"error": f"User endpoint '{destination}' not found"}), 404
        except Exception as e:
            return jsonify({"error": f"User service error: {str(e)}"}), 500

    def handle_admin_service(self, destination, data, method):
        """Admin service routing - An toàn và chuẩn hóa"""
        if not self.admin_controller:
            return jsonify({"error": "Admin service not available"}), 503
        
        try:
            # Handle từng route riêng biệt
            if destination == 'health' and method == 'POST':
                service_name = data.get('service') if data else None
                return self.admin_controller.check_health(service_name)
            
            elif destination == 'services' and method == 'POST':
                print('calling admin services')
                return self.admin_controller.list_services()
            
            elif destination == 'system-stats' and method == 'POST':
                return self.admin_controller.get_system_stats()
            
            elif destination == 'users' and method == 'POST':
                role = data.get('role') if data else None
                print('calling admin users with role: ', role)
                return self.admin_controller.list_users(role)
            
            elif destination == 'users/add' and method == 'POST':
                print('running add specialized user: ', data)
                # if not data:
                #     return jsonify({"error": "Request body required"}), 400
                return self.admin_controller.add_specialized_user(data)
            
            elif destination == 'users/change-role' and method == 'POST':
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                return self.admin_controller.change_user_role(data)
            
            # Permission endpoints
            elif destination == 'permissions/add' and method == 'POST':
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                return self.admin_controller.add_permission(data)
            
            elif destination == 'permissions/list' and method == 'POST':
                return self.admin_controller.list_permissions(data or {})
            
            elif destination == 'permissions/delete' and method == 'POST':
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                return self.admin_controller.delete_permission(data)
            
            elif destination == 'permissions/check' and method == 'POST':
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                return self.admin_controller.check_permission(data)
            
            elif destination == 'permissions/role' and method == 'POST':
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                return self.admin_controller.get_role_permissions(data)
            
            else:
                available_endpoints = [
                    "POST /admin/health", "POST /admin/services", "POST /admin/system-stats",
                    "POST /admin/users", "POST /admin/users/add", "POST /admin/users/change-role",
                    "POST /admin/permissions/add", "POST /admin/permissions/list",
                    "POST /admin/permissions/delete", "POST /admin/permissions/check", 
                    "POST /admin/permissions/role"
                ]
                return jsonify({
                    "error": f"Admin endpoint '{destination}' not found",
                    "available_endpoints": available_endpoints
                }), 404
                
        except Exception as e:
            return jsonify({"error": f"Admin service error: {str(e)}"}), 500

    def handle_progress_service(self, destination, data, method):
        """Điều hướng progress service - Enhanced với endpoints mới"""
        if not self.progress_controller:
            return jsonify({"error": "Progress service not available"}), 503
        
        try:
            if destination == 'health' and method == 'GET':
                return self.progress_controller.check_health()

            elif destination == 'complete-map' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                data['user_id'] = user_id
                return self.progress_controller.complete_map(data)
            
            elif destination == 'user/maps' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.progress_controller.get_user_map_progress(user_id)
            
            # ✅ THÊM: User progress summary
            elif destination == 'user/summary' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.progress_controller.get_user_progress_summary(user_id)
            
            elif destination == 'leaderboard' and method == 'POST':
                return self.progress_controller.get_map_leaderboard(data)
            
            # ✅ THÊM: Map statistics  
            elif destination == 'map/statistics' and method == 'POST':
                return self.progress_controller.get_map_statistics(data)
            
            else:
                return jsonify({
                    "error": f"Progress endpoint '{destination}' not found",
                    "available_endpoints": [
                        "GET /progress/health",
                        "POST /progress/complete-map",
                        "POST /progress/user/maps", 
                        "POST /progress/user/summary",
                        "POST /progress/leaderboard",
                        "POST /progress/map/statistics"
                    ]
                }), 404
            
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
        """Điều hướng item service - CHỈ hỗ trợ sword system"""
        if not self.item_controller:
            return jsonify({"error": "Item service not available"}), 503
        
        try:
            if destination == 'health' and method == 'GET':
                return self.item_controller.check_health()
        
            elif destination == 'user/sword' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.item_controller.get_user_sword(str(user_id))
            
            elif destination == 'sword/upgrade' and method == 'POST':
                user_id = self._get_user_id_from_jwt()
                if not user_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.item_controller.upgrade_sword(str(user_id))
            
        except Exception as e:
            return jsonify({"error": f"Item service error: {str(e)}"}), 500
    @jwt_required()
    def handle_game_service(self, destination, data, method):
        try:
            if destination == 'health' and method == 'GET':
                return jsonify({"status": "healthy", "service": "game"}), 200

            elif destination == 'newroom' and method == 'POST':
                print("Reached game/newroom handler")
                if not self.game_service:
                    return jsonify({"error": "Game service not available"}), 503

                student_id = get_jwt_identity()
                difficulty = data.get('difficulty')
                class_id = data.get('class_id')

                if not student_id or not difficulty or not class_id:
                    return jsonify({"error": "Missing parameters"}), 400

                try:
                    response = self.game_service.create_game_room(student_id, difficulty, class_id)

                    if response is None:
                        return jsonify({"error": "Game service returned nothing"}), 500

                    if isinstance(response, tuple):
                        return response
                    elif isinstance(response, dict):
                        return jsonify(response), 200
                    return response
                except Exception as e:
                    return jsonify({"error": f"Game service crash: {str(e)}"}), 500

            # 🔄 CHUYỂN: Check answer từ JSON
            elif destination == "check_answer" and method == "POST":
                session_id = data.get('session_id')
                answer = data.get('answer')
                question_id = data.get('question_id')
                if not session_id or not answer:
                    return jsonify({"error": "session_id and answer required in JSON"}), 400
                return self.game_service.check_answer(session_id, answer,question_id)

            # 🔄 CHUYỂN: Get question từ JSON
            elif destination == "get_question" and method == 'POST':
                session_id = data.get('session_id')
                class_id = data.get('class_id')
                if not session_id:
                    return jsonify({"error": "session_id required in JSON"}), 400
                return self.game_service.get_question(session_id,class_id)
            
            else:
                return jsonify({"error": "Game endpoint not implemented"}), 501
        except Exception as e:
            return jsonify({"error": f"Game service error: {str(e)}"}), 500

    @jwt_required()
    def classroom_service(self, destination, data, method):
        if not self.classroom_controller:
            return jsonify({"error": "Classroom service not available"}), 503
        try:
            if destination == "health" and method == "GET":
                return self.classroom_controller.check_health()
            elif destination == "create" and method == "POST":
                return self.classroom_controller.create_class(data)
            elif destination == "classes" and method == "POST":
                return self.classroom_controller.get_teachers_classes()
            elif destination == "join" and method == "POST":
                return self.classroom_controller.join_class(data)
            elif destination == "students" and method == "POST":
                class_id = data.get("class_id") if data else None
                print("Student", class_id)
                return self.classroom_controller.get_students(class_id)
            elif destination == "dashboard" and method == "POST":
                class_id = data.get("class_id")
                if not class_id:
                    return jsonify({"error": "class_id required in JSON"}), 400
                return self.classroom_controller.get_dashboard(class_id)
            elif destination == "add_question" and method == "POST":
                return self.classroom_controller.create_question()
            elif destination == "student/classes" and method == "POST":
                student_id = self._get_user_id_from_jwt()
                if not student_id:
                    return jsonify({"error": "Authentication required"}), 401
                return self.classroom_controller.get_student_classes()
            elif destination == "kick" and method == "POST":
                return self.classroom_controller.kick_student(data)
            elif destination == "questions" and method == "POST":
                return self.classroom_controller.get_questions_by_criteria()
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
                    access_token = create_access_token(identity=id,additional_claims=additional_claims)
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
                    access_token = create_access_token(identity=id, additional_claims=additional_claims)
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