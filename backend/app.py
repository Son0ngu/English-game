from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder, singleton
import os
from datetime import timedelta
import dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Import database interface trực tiếp
from userProfile_service.database_interface import DatabaseInterface, UserProfileDatabaseInterface, ItemDatabaseInterface

# Load environment variables from .env file
dotenv.load_dotenv()

def create_app(config_object=None):
    app = Flask(__name__)
    
    # Apply configuration if provided
    if config_object:
        app.config.from_object(config_object)
    
    # Configure CORS
    CORS(app)
    
    # JWT Configurations
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_COOKIE_SECURE'] = True
    app.config['JWT_COOKIE_SAMESITE'] = 'LAX'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
    jwt = JWTManager(app)
    
    # Register API Gateway service
    from api_gateway.gateway_service import gateway_service
    app.gateway_service = gateway_service(app)
    
    # Configure dependency injection
    FlaskInjector(app=app, modules=[configure])
    
    # Add API Gateway catchall route
    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    @app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def gateway_request(path):
        return app.gateway_service.new_request(path)
    
    # Database teardown handler không cần vì DatabaseInterface đã tự đóng kết nối
    
    return app

def configure(binder: Binder):
    # Đảm bảo thư mục data tồn tại
    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Sử dụng database_interface thay vì tạo mới DatabaseConfig
    db_path = os.path.join(data_dir, "english_game.db")
    database_interface = DatabaseInterface(db_path)
    user_db_interface = UserProfileDatabaseInterface(db_path)
    item_db_interface = ItemDatabaseInterface(db_path)
    
    # Bind database interfaces
    binder.bind(DatabaseInterface, to=database_interface, scope=singleton)
    binder.bind(UserProfileDatabaseInterface, to=user_db_interface, scope=singleton)
    binder.bind(ItemDatabaseInterface, to=item_db_interface, scope=singleton)
    
    # Import repositories từ userProfile_service
    from userProfile_service.user_repository import UserRepository
    from userProfile_service.item_repository import ItemRepository
    
    # Import permission repository từ src nếu cần
    try:
        from src.data.permission_repository import PermissionRepository
        permissions_file = os.path.join(data_dir, "permissions.json")
        permission_repository = PermissionRepository({"permissions_file": permissions_file})
        binder.bind(PermissionRepository, to=permission_repository, scope=singleton)
    except ImportError:
        # Tạo một mock PermissionRepository nếu không tìm thấy
        class PermissionRepository:
            def check_permission(self, *args, **kwargs): return True
        permission_repository = PermissionRepository()
    
    # Tạo các repository
    user_repository = UserRepository()  # Sẽ tự động sử dụng UserProfileDatabaseInterface
    item_repository = ItemRepository()  # Sẽ tự động sử dụng ItemDatabaseInterface
    
    # Bind repositories
    binder.bind(UserRepository, to=user_repository, scope=singleton)
    binder.bind(ItemRepository, to=item_repository, scope=singleton)
    
    # Tương tự import services từ userProfile_service thay vì src
    from userProfile_service.user_service import UserProfileService
    from userProfile_service.item_service import ItemService
    
    # Import các service khác nếu có
    try:
        from src.services.permission_service import PermissionService
        from src.services.admin_service import AdminService
        from src.services.progress_service import ProgressService
        permission_service = PermissionService(permission_repository)
        admin_service = AdminService(user_repository)
        progress_service = ProgressService(user_repository, admin_service)
    except ImportError:
        # Tạo các mock service nếu không tìm thấy
        class BaseService:
            def check_internal(self): return {"status": "healthy"}
        
        class PermissionService(BaseService): pass
        class AdminService(BaseService):
            def __init__(self, user_repo):
                self.user_repo = user_repo
                self.services = {}
            def register_service(self, name, service):
                self.services[name] = service
        class ProgressService(BaseService): pass
        
        permission_service = PermissionService()
        admin_service = AdminService(user_repository)
        progress_service = ProgressService()
    
    # Initialize user and item services
    user_service = UserProfileService()
    item_service = ItemService()
    
    # Try to import course service if available
    try:
        from src.services.course_service import CourseService
        from src.services.difficulty_evaluator import DifficultyEvaluator
        course_service = CourseService()
        difficulty_evaluator = DifficultyEvaluator()
    except ImportError:
        # Mock implementations if not available
        class BaseService:
            def check_internal(self): return {"status": "not_implemented"}
        class CourseService(BaseService): pass
        class DifficultyEvaluator(BaseService): pass
        course_service = CourseService()
        difficulty_evaluator = DifficultyEvaluator()
    
    # Register services for health check
    admin_service.register_service('users', user_service)
    admin_service.register_service('permissions', permission_service)
    admin_service.register_service('items', item_service)
    admin_service.register_service('progress', progress_service)
    admin_service.register_service('admin', admin_service)
    admin_service.register_service('courses', course_service)
    admin_service.register_service('difficulty', difficulty_evaluator)
    
    # Bind all services
    binder.bind(UserProfileService, to=user_service, scope=singleton)
    binder.bind(PermissionService, to=permission_service, scope=singleton)
    binder.bind(AdminService, to=admin_service, scope=singleton)
    binder.bind(CourseService, to=course_service, scope=singleton)
    binder.bind(DifficultyEvaluator, to=difficulty_evaluator, scope=singleton)
    binder.bind(ItemService, to=item_service, scope=singleton)
    binder.bind(ProgressService, to=progress_service, scope=singleton)

# Make the file directly runnable
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)