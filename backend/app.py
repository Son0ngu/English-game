from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder, singleton
import os

from backend.src.config.database import DatabaseConfig


def create_app(config_object=None):
    app = Flask(__name__)
    
    if config_object:
        app.config.from_object(config_object)
    
    # Register blueprints - Fix import paths
    from backend.src.controllers.user_controller import user_bp
    from backend.src.controllers.admin_controller import admin_bp
    from backend.src.controllers.permission_controller import permission_bp
    from backend.src.controllers.item_controller import item_bp  # Add missing controller
    
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(permission_bp)
    app.register_blueprint(item_bp)  # Register the item blueprint
    
    # Configure dependency injection
    FlaskInjector(app=app, modules=[configure])
    
    # Thêm teardown handler
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
    # Database setup - Fix import paths
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
    
    # Create and bind services - FIX THESE IMPORTS
    from backend.src.services.user_service import UserProfileService
    from backend.src.services.permission_service import PermissionService
    from backend.src.services.admin_service import AdminService

    from backend.src.services.item_service import ItemService

    from backend.src.services.progress_service import ProgressService
    
    # Initialize services
    user_service = UserProfileService(user_repository)
    permission_service = PermissionService(permission_repository)
    admin_service = AdminService(user_service)


    item_service = ItemService(item_repository)
    progress_service = ProgressService(user_service, admin_service)
    
    # Register services for health check
    admin_service.register_service('users', user_service)
    admin_service.register_service('permissions', permission_service)
    admin_service.register_service('items', item_service)
    admin_service.register_service('progress', progress_service)
    admin_service.register_service('admin', admin_service)
    
    # Bind all services
    binder.bind(UserProfileService, to=user_service, scope=singleton)
    binder.bind(PermissionService, to=permission_service, scope=singleton)
    binder.bind(AdminService, to=admin_service, scope=singleton)
    binder.bind(ItemService, to=item_service, scope=singleton)
    binder.bind(ProgressService, to=progress_service, scope=singleton)



# Add this to make the file directly runnable
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)