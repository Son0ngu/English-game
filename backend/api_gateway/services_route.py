from flask import jsonify

import game_service.gameroom.game_room_controller as game_room_controller
# Import các controller
from progressandfeedback.progress_controller import ProgressController
from progressandfeedback.feedback_controller import FeedbackController
from admin_service.admin_controller import AdminController
from userProfile_service.user_controller import UserController
from userProfile_service.item_controller import ItemController  
from classroom_service.classroom_controller import ClassroomController
from classroom_service.classroom_service import ClassroomService
from userProfile_service.user_service import UserProfileService 
from course_service.course_controller import CourseController
from course_service.course_service import CourseService

# Import các service
from progressandfeedback.progress_service.progress_service import ProgressService
from userProfile_service.user_service import UserProfileService
from userProfile_service.item_service import ItemService  # Thêm dòng này
from progressandfeedback.progress_service.admin_service import AdminService

class services_route:
    def __init__(self):
        self.game_room_controller = game_room_controller()
        self.auth_service_controller = auth_service_controller()
        user_service = UserProfileService()
        item_service = ItemService() 
        admin_service = AdminService(user_service)
        progress_service = ProgressService(user_service, admin_service)
        classroom_service = ClassroomService(user_service)
        course_service = CourseService()

        admin_service.register("user", user_service)
        admin_service.register("item", item_service)  
        admin_service.register("progress", progress_service)

        self.admin_controller = AdminController(admin_service)
        self.progress_controller = ProgressController(progress_service)
        self.feedback_controller = FeedbackController(progress_service)
        self.user_controller = UserController(user_service)
        self.item_controller = ItemController(item_service)  # Thêm dòng này
        self.classroom_controller = ClassroomController(classroom_service)
        self.course_controller = CourseController(course_service)

    def admin_service(self, destination, data, method):
        """
        Điều hướng yêu cầu admin service đến admin controller
        """
        # Kiểm tra sức khỏe của các dịch vụ
        if destination == 'health' and method == 'GET':
            service_name = data.get('service')  # Từ query params
            return self.admin_controller.check_health(service_name)
            
        # Liệt kê các dịch vụ đã đăng ký
        elif destination == 'services' and method == 'GET':
            return self.admin_controller.list_services()
            
        # Lấy thống kê hệ thống
        elif destination == 'system-stats' and method == 'GET':
            return self.admin_controller.get_system_stats()
            
        # Lấy danh sách người dùng
        elif destination == 'users' and method == 'GET':
            role = data.get('role')  # Từ query params
            return self.admin_controller.list_users(role)
            
        # Thay đổi vai trò người dùng
        elif destination == 'users/change-role' and method == 'PUT':
            return self.admin_controller.change_user_role(data)
            
        # Endpoint không tồn tại
        return jsonify({"error": "Admin endpoint không tồn tại"}), 404
        
    def classroom_service(self, destination, data, method):
        pass
    def auth_service(self,destination, data, method):
        if destination == 'login' and method == 'POST':
            if data.get('username') and data.get('password'):
                username = data.get('username')
                password = data.get('password')
                if self.auth_service_controller.login(username, password):
                    id = self.auth_service_controller.get_id_from_username(username)
                    role = self.auth_service_controller.get_role_from_id(id)
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
                if self.auth_service_controller.sign_up(username, password):
                    print("User created successfully (service_route)")
                    return {"message": "User created successfully"}, 200
                else:
                    print("User already exists (service_route)")
                    return {"error": "User already exists"}, 400
            return None

        if destination == "add_permission" and method == 'POST':
            jwt_role = get_jwt().get("role")
            user_id = get_jwt_identity()
            role = data.get("role")
            path = data.get("path")
            service = data.get("service")
            method = data.get("method")
            if jwt_role =="admin":
                self.auth_service_controller.add_permission(role, path, service, method)
                print("Permission added successfully (service_route)")
                return {"message": "Permission added successfully"}, 200

        
    def game_service(self, destination, data, method):
        if destination == 'newroom' and method=='POST':
            student_id = data.get('student_id')
            if student_id:
                self.game_room_controller.create_game_room(student_id)
                return jsonify({"message": "Game room created successfully"}), 200
            else:
                print("Student ID is required")
                return jsonify({"error": "Error"}), 400
        return None

    def progress_service(self, destination, data, method):
       
        # Handle different progress endpoints
        if destination == 'record' and method == 'POST':
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
            
        elif destination == 'health' and method == 'GET':
            return self.progress_controller.check_health()
            
        # Endpoint not found
        return jsonify({"error": "Progress endpoint not found"}), 404
        
    def feedback_service(self, destination, data, method):
        """
        Route feedback service requests to the feedback controller
        """
        # Generate feedback for an activity result
        if destination == 'generate' and method == 'POST':
            return self.feedback_controller.generate_feedback(data)
            
        # Get all feedback for a user
        elif destination.startswith('user/') and method == 'GET':
            user_id = destination.split('/')[-1]
            return self.feedback_controller.get_user_feedback(user_id)
            
        # Get specific feedback by ID
        elif method == 'GET':
            # Use the destination as the feedback ID
            feedback_id = destination
            return self.feedback_controller.get_feedback_by_id(feedback_id)
            
        # Endpoint not found
        return jsonify({"error": "Feedback endpoint not found"}), 404
        
    def user_service(self, destination, data, method):
        """
        Điều hướng yêu cầu user service đến user controller
        """
        # Xử lý login và register
        if destination == 'login' and method == 'POST':
            return self.user_controller.login(data)
            
        elif destination == 'register' and method == 'POST':
            return self.user_controller.register(data)
            
        # Xử lý thông tin người dùng
        elif method == 'GET' and destination.isdigit():
            # Route cho /user/{id}
            return self.user_controller.get_user(int(destination))
            
        elif method == 'PUT' and destination.isdigit():
            # Route cho /user/{id} - update
            return self.user_controller.update_user(int(destination), data)
            
        elif method == 'DELETE' and destination.isdigit():
            # Route cho /user/{id} - delete 
            return self.user_controller.delete_user(int(destination))
            
        # Xử lý danh sách người dùng
        elif destination == 'students' and method == 'GET':
            limit = data.get('limit', 100)
            offset = data.get('offset', 0)
            return self.user_controller.get_all_students(limit, offset)
            
        elif destination == 'teachers' and method == 'GET':
            limit = data.get('limit', 100)
            offset = data.get('offset', 0)
            return self.user_controller.get_all_teachers(limit, offset)
            
        # Xử lý tiến độ học tập
        elif destination.startswith('progress/') and method == 'GET':
            user_id = int(destination.split('/')[-1])
            return self.user_controller.get_progress(user_id)
            
        elif destination.startswith('progress/') and method == 'POST':
            user_id = int(destination.split('/')[-1])
            return self.user_controller.update_progress(user_id, data)
            
        # Xử lý mua vật phẩm
        elif destination.startswith('items/') and method == 'POST':
            user_id = int(destination.split('/')[-1])
            return self.user_controller.buy_item(user_id, data)
            
        # Kiểm tra sức khỏe dịch vụ
        elif destination == 'health' and method == 'GET':
            return self.user_controller.check_health()
            
        # Endpoint không tồn tại
        return jsonify({"error": "User endpoint không tồn tại"}), 404

    def item_service(self, destination, data, method):
        """
        Điều hướng yêu cầu item service đến item controller
        """
        # Lấy danh sách vật phẩm mẫu
        if destination == 'catalog' and method == 'GET':
            return self.item_controller.get_all_items()
            
        # Lấy thông tin một vật phẩm cụ thể
        elif method == 'GET' and not destination.startswith('user/'):
            # Xử lý như là item_id
            return self.item_controller.get_item(destination)
            
        # Lấy vật phẩm của người dùng 
        elif destination.startswith('user/') and method == 'GET':
            user_id = destination.split('/')[-1]
            return self.item_controller.get_user_items(user_id)
            
        # Mua vật phẩm
        elif destination == 'purchase' and method == 'POST':
            return self.item_controller.purchase_item(data)
            
        # Nâng cấp vật phẩm
        elif destination == 'upgrade' and method == 'POST':
            return self.item_controller.upgrade_item(data)
            
        # Kiểm tra sức khỏe dịch vụ
        elif destination == 'health' and method == 'GET':
            return self.item_controller.check_health()
            
        # Endpoint không tồn tại
        return jsonify({"error": "Item endpoint không tồn tại"}), 404

    def classroom_service(self, destination, data, method):
        if destination == "" and method == "POST":
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
        elif destination == "health" and method == "GET":
            return self.classroom_controller.check_health()
        return jsonify({"error": "Classroom endpoint không tồn tại"}), 404

    def course_service(self, destination, data, method):
        if destination == "" and method == "POST":
            return self.course_controller.create_course(data)

        elif destination == "" and method == "GET":
            return self.course_controller.get_courses()

        elif destination.endswith("/lesson") and method == "POST":
            course_id = destination.split("/")[0]
            return self.course_controller.create_lesson(course_id, data)

        elif destination.endswith("/lesson") and method == "GET":
            course_id = destination.split("/")[0]
            return self.course_controller.get_lessons(course_id)

        elif "/lesson/" in destination and destination.endswith("/topic") and method == "POST":
            parts = destination.split("/")
            course_id = parts[0]
            lesson_id = parts[2]
            return self.course_controller.create_topic(course_id, lesson_id, data)

        elif "/lesson/" in destination and destination.endswith("/topic") and method == "GET":
            parts = destination.split("/")
            course_id = parts[0]
            lesson_id = parts[2]
            return self.course_controller.get_topics(course_id, lesson_id)

        elif "/lesson/" in destination and "/topic/" in destination and destination.endswith(
                "/question") and method == "POST":
            parts = destination.split("/")
            lesson_id = parts[1]
            topic_id = parts[3]
            return self.course_controller.create_question(lesson_id, topic_id, data)

        elif "/lesson/" in destination and "/topic/" in destination and destination.endswith(
                "/question") and method == "GET":
            parts = destination.split("/")
            lesson_id = parts[1]
            topic_id = parts[3]
            return self.course_controller.get_questions(lesson_id, topic_id)

        elif destination == "health" and method == "GET":
            return self.course_controller.check_health()

        return jsonify({"error": "Course endpoint không tồn tại"}), 404

