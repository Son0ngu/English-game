from flask import Blueprint, request, jsonify
from injector import inject
from ..services.admin_service import AdminService

# Create blueprint for admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/health', methods=['GET'])
@inject
def check_health(admin_service: AdminService):
    """Check health of all services"""
    service_name = request.args.get('service')
    health_data = admin_service.check_service_availability(service_name)
    
    # Get overall system status
    all_healthy = all(data.get('status') == 'healthy' 
                     for data in health_data.values())
    
    return jsonify({
        "overall_status": "healthy" if all_healthy else "degraded",
        "services": health_data,
        "timestamp": int(admin_service._startup_time)
    })

@admin_bp.route('/services', methods=['GET'])
@inject
def list_services(admin_service: AdminService):
    """List all registered services"""
    return jsonify({
        "services": list(admin_service.services.keys())
    })

# Additional admin endpoints can be added here
@admin_bp.route('/system-stats', methods=['GET'])
@inject
def get_system_stats(admin_service: AdminService):
    """Get system statistics"""
    return jsonify(admin_service.get_system_stats())

@admin_bp.route('/users', methods=['GET'])
@inject
def list_users(admin_service: AdminService):
    """Get all users"""
    return jsonify({"users": admin_service.list_users()})