import os
from datetime import timedelta
import dotenv
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_cors import CORS
from api_gateway.gateway_service import gateway_service

# Load environment variables from .env file
dotenv.load_dotenv()
app = Flask(__name__)
CORS(app)


# JWT Configurations
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['headers','cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'LAX'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
jwt = JWTManager(app)
# Service instances:
gateway_service = gateway_service(app)
@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

def request(path):
    return gateway_service.new_request(path)


if __name__ == '__main__':
    app.run()
