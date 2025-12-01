from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder, singleton
import os
from datetime import timedelta
import dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from backend.src.config.database import DatabaseConfig
from api_gateway.gateway_service import gateway_service

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
    app.gateway_service = gateway_service(app)
    
    # Configure dependency injection
    FlaskInjector(app=app, modules=[configure])
    
    # Add API Gateway catchall route
    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    @app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def gateway_request(path):
        return app.gateway_service.new_request(path)
    
    # Database teardown handler
    @app.teardown_appcontext
    def close_connection(exception):
        try:
            database_config = app.injector.get(DatabaseConfig)
            if database_config:
                database_config.close()
        except Exception as e:
            app.logger.error(f"Error closing database: {e}")
    
    return app

def configure(binder: Binder):
    # Database setup
    from backend.src.config.database import DatabaseConfig
    from backend.src.data.user_repository import UserRepository
    from backend.src.data.permission_repository import PermissionRepository
    from backend.src.data.item_repository import ItemRepository
    
    # Create configuration
    db_config = {
        "sqlite_path": os.path.join(os.getcwd(), "data", "english_game.db"),
        "permissions_file": os.path.join(os.getcwd(), "data", "permissions.json")
    }
    
    # Create configs and repositories
    database_config = DatabaseConfig(db_config)
    connection = database_config.get_connection()
    
    user_repository = UserRepository(database_config.db_type, connection)
    permission_repository = PermissionRepository(db_config)
    item_repository = ItemRepository(database_config.db_type, connection)
    
    # Bind repositories
    binder.bind(DatabaseConfig, to=database_config, scope=singleton)
    binder.bind(UserRepository, to=user_repository, scope=singleton)
    binder.bind(PermissionRepository, to=permission_repository, scope=singleton)
    binder.bind(ItemRepository, to=item_repository, scope=singleton)
    
    # Import services
    from backend.src.services.user_service import UserProfileService
    from backend.src.services.permission_service import PermissionService
    from backend.src.services.admin_service import AdminService
    from backend.src.services.item_service import ItemService
    from backend.src.services.progress_service import ProgressService
    
    # Create services for missing ones if needed
    try:
        from backend.src.services.course_service import CourseService
        from backend.src.services.difficulty_evaluator import DifficultyEvaluator
        course_service_available = True
        difficulty_evaluator_available = True
    except ImportError:
        # Create minimal implementations if missing
        from backend.src.services.base_service import BaseService
        class CourseService(BaseService):
            def check_internal(self): return {"status": "not_implemented"}
        class DifficultyEvaluator(BaseService):
            def check_internal(self): return {"status": "not_implemented"}
        course_service_available = False
        difficulty_evaluator_available = False
    
    # Initialize services
    user_service = UserProfileService(user_repository)
    permission_service = PermissionService(permission_repository)
    admin_service = AdminService(user_service)
    item_service = ItemService(item_repository)
    progress_service = ProgressService(user_service, admin_service)
    
    # Initialize optional services
    course_service = CourseService()
    difficulty_evaluator = DifficultyEvaluator()
    
    # Register services for health check
    admin_service.register_service('users', user_service)
    admin_service.register_service('permissions', permission_service)
    admin_service.register_service('items', item_service)
    admin_service.register_service('progress', progress_service)
    admin_service.register_service('admin', admin_service)
    
    # Register optional services
    if course_service_available:
        admin_service.register_service('courses', course_service)
    if difficulty_evaluator_available:
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
    from flask import Flask
    from api_gateway.gateway_service import gateway_service

    app = Flask(__name__)

    # Initialize API Gateway
    api = gateway_service(app)

    app.run(debug=True)