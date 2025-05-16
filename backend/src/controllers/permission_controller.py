from flask import Blueprint, request, jsonify
from injector import inject
from ..services.permission_service import PermissionService
from ..controllers.response_utils import mongo_response, error_response

# Tạo blueprint cho các routes liên quan đến quyền
permission_bp = Blueprint('permissions', __name__, url_prefix='/api/permissions')

@permission_bp.route('/check/<role>/<permission>', methods=['GET'])
@inject
def check_permission(permission_service: PermissionService, role: str, permission: str):
    """Kiểm tra quyền cho một role cụ thể"""
    has_permission = permission_service.check_permission(role, permission)
    return mongo_response({
        "role": role,
        "permission": permission,
        "has_permission": has_permission
    })

@permission_bp.route('/roles', methods=['GET'])
@inject
def get_all_roles(permission_service: PermissionService):
    """Lấy danh sách tất cả roles và quyền"""
    return mongo_response(permission_service.role_permissions)

@permission_bp.route('/role/<role>', methods=['GET'])
@inject
def get_role_permissions(permission_service: PermissionService, role: str):
    """Lấy danh sách quyền của một role cụ thể"""
    if role in permission_service.role_permissions:
        return mongo_response({
            "role": role,
            "permissions": permission_service.role_permissions[role]
        })
    return error_response(f"Role '{role}' not found", 404)

@permission_bp.route('/role/<role>/<permission>', methods=['POST'])
@inject
def add_role_permission(permission_service: PermissionService, role: str, permission: str):
    """Thêm quyền cho một role"""
    success = permission_service.add_permission(role, permission)
    if success:
        return mongo_response({
            "success": True,
            "message": f"Permission '{permission}' added to role '{role}'"
        }, 201)
    return error_response("Failed to add permission", 400)

@permission_bp.route('/role/<role>/<permission>', methods=['DELETE'])
@inject
def delete_role_permission(permission_service: PermissionService, role: str, permission: str):
    """Xóa quyền khỏi một role"""
    success = permission_service.delete_permission(role, permission)
    if success:
        return mongo_response({
            "success": True,
            "message": f"Permission '{permission}' removed from role '{role}'"
        })
    return error_response(f"Permission '{permission}' not found in role '{role}'", 404)

@permission_bp.route('/temp', methods=['POST'])
@inject
def add_temp_permission(permission_service: PermissionService):
    """Thêm quyền tạm thời"""
    data = request.json
    if not data or 'role' not in data or 'permission' not in data or 'duration' not in data:
        return error_response("Missing required fields", 400)
    
    success = permission_service.add_temp_permission(
        data['role'], data['permission'], data['duration']
    )
    
    if success:
        return mongo_response({
            "success": True,
            "message": f"Temporary permission '{data['permission']}' added to role '{data['role']}'"
        }, 201)
    return error_response("Failed to add temporary permission", 400)

@permission_bp.route('/health', methods=['GET'])
@inject
def check_health(permission_service: PermissionService):
    """Kiểm tra trạng thái của permission service"""
    health_data = permission_service.check_internal()
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return mongo_response(health_data, status_code)