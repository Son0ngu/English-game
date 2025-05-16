from flask import Blueprint, request
from injector import inject
from ..services.user_service import UserProfileService
from ..controllers.response_utils import mongo_response, error_response

# Create blueprint for user routes
user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/login', methods=['POST'])
@inject
def login(user_service: UserProfileService):
    """Authenticate a user"""
    data = request.json
    
    if not data or 'username' not in data or 'password' not in data:
        return error_response("Missing username or password", 400)
    
    result = user_service.authenticate(data['username'], data['password'])
    
    if result.get('success'):
        return mongo_response(result, 200)
    else:
        return error_response(result.get('error', 'Authentication failed'), 401)

@user_bp.route('/register', methods=['POST'])
@inject
def register(user_service: UserProfileService):
    """Register a new user"""
    data = request.json
    
    if not data or 'username' not in data or 'password' not in data:
        return error_response("Missing required fields", 400)
    
    user_type = data.get('user_type', 'student')
    result = user_service.create_user(data, user_type)
    
    if result.get('success'):
        return mongo_response(result, 201)
    else:
        return error_response(result.get('error', 'Registration failed'), 400)

@user_bp.route('/<user_id>', methods=['GET'])
@inject
def get_user(user_service: UserProfileService, user_id):
    """Get user details"""
    user_data = user_service.get_user(user_id)
    
    if user_data:
        return mongo_response(user_data, 200)
    else:
        return error_response("User not found", 404)

@user_bp.route('/<user_id>', methods=['PUT'])
@inject
def update_user(user_service: UserProfileService, user_id):
    """Update user profile"""
    data = request.json
    
    if not data:
        return error_response("No update data provided", 400)
    
    result = user_service.update_profile(user_id, data)
    
    if result.get('success'):
        return mongo_response(result, 200)
    else:
        return error_response(result.get('error', 'Update failed'), 404 if "not found" in result.get('error', '') else 400)

@user_bp.route('/<user_id>', methods=['DELETE'])
@inject
def delete_user(user_service: UserProfileService, user_id):
    """Delete a user"""
    result = user_service.delete_user(user_id)
    
    if result.get('success'):
        return mongo_response(result, 200)
    else:
        return error_response(result.get('error', 'Deletion failed'), 404 if "not found" in result.get('error', '') else 400)

@user_bp.route('/students', methods=['GET'])
@inject
def get_all_students(user_service: UserProfileService):
    """Get all students"""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    students = user_service.get_all_students(limit, offset)
    return mongo_response({"students": students}, 200)

@user_bp.route('/teachers', methods=['GET'])
@inject
def get_all_teachers(user_service: UserProfileService):
    """Get all teachers"""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    teachers = user_service.get_all_teachers(limit, offset)
    return mongo_response({"teachers": teachers}, 200)

@user_bp.route('/<user_id>/progress', methods=['GET'])
@inject
def get_progress(user_service: UserProfileService, user_id):
    """Get a student's learning progress"""
    result = user_service.get_student_progress(user_id)
    
    if result.get('success'):
        return mongo_response(result, 200)
    else:
        return error_response(result.get('error', 'Progress retrieval failed'), 404 if "not found" in result.get('error', '') else 400)

@user_bp.route('/<user_id>/progress', methods=['POST'])
@inject
def update_progress(user_service: UserProfileService, user_id):
    """Update a student's progress"""
    data = request.json
    
    if not data or 'lesson_id' not in data or 'points' not in data:
        return error_response("Missing required fields", 400)
    
    result = user_service.update_progress(
        user_id, 
        data['lesson_id'], 
        data['points']
    )
    
    if result.get('success'):
        return mongo_response(result, 200)
    else:
        return error_response(result.get('error', 'Progress update failed'), 404 if "not found" in result.get('error', '') else 400)

@user_bp.route('/<user_id>/items', methods=['POST'])
@inject
def buy_item(user_service: UserProfileService, user_id):
    """Buy an item for a student"""
    data = request.json
    
    if not data or 'item' not in data or 'cost' not in data:
        return error_response("Missing required fields", 400)
    
    result = user_service.buy_item_for_student(
        user_id, 
        data['item'], 
        data['cost']
    )
    
    if result.get('success'):
        return mongo_response(result, 200)
    else:
        return error_response(result.get('error', 'Item purchase failed'), 400)

@user_bp.route('/health', methods=['GET'])
@inject
def check_health(user_service: UserProfileService):
    """Check health of user service"""
    health_data = user_service.check_internal()
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return mongo_response(health_data, status_code)