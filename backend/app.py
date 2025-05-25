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
    FlaskInjector(app=app)
    
    # Add API Gateway catchall route
    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    @app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def gateway_request(path):
        return app.gateway_service.new_request(path)
    
    # Database teardown handler không cần vì DatabaseInterface đã tự đóng kết nối
    
    return app


# Make the file directly runnable
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)