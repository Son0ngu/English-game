from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
import dotenv

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
    
    # Simple configuration
    app.config['DEBUG'] = True
    
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
    
    # Initialize database interfaces for dependency injection
    try:
        # Test database connections on startup
        user_db = UserProfileDatabaseInterface()
        item_db = ItemDatabaseInterface()
        
        # Store in app context for potential access
        app.user_db = user_db
        app.item_db = item_db
        
    except Exception as e:
        # Continue without database - services will handle their own connections
        pass
    
    # Register API Gateway service
    from api_gateway.gateway_service import gateway_service
    app.gateway_service = gateway_service(app)
    
    # Optional: Configure dependency injection if flask_injector is available
    try:
        from flask_injector import FlaskInjector
        from injector import Binder, singleton
        
        def configure_di(binder: Binder):
            """Configure dependency injection bindings"""
            try:
                binder.bind(UserProfileDatabaseInterface, to=UserProfileDatabaseInterface(), scope=singleton)
                binder.bind(ItemDatabaseInterface, to=ItemDatabaseInterface(), scope=singleton)
            except Exception as e:
                pass
        
        FlaskInjector(app=app, config=configure_di)
        
    except ImportError:
        pass
    except Exception as e:
        pass
    
    # Add API Gateway catchall route (override default routing)
    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    @app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def gateway_request(path):
        return app.gateway_service.new_request(path)
    
    return app

# Make the file directly runnable
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)