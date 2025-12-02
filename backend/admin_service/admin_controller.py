from flask import jsonify
import psutil
import time

class AdminController:
    def __init__(self, admin_service):
        """
        Khởi tạo AdminController với AdminService
        
        Parameters:
            admin_service: Dịch vụ quản lý admin
        """
        self.admin_service = admin_service

    def check_health(self, service_name=None):
        """Kiểm tra sức khỏe hệ thống hoặc service cụ thể"""
        try:
            if service_name:
                # Kiểm tra service cụ thể
                services = self.admin_service.services
                if service_name in services:
                    service = services[service_name]
                    if hasattr(service, 'check_internal'):
                        health = service.check_internal()
                    else:
                        health = {"status": "unknown", "details": "No health check available"}
                    return jsonify({"service": service_name, "health": health}), 200
                else:
                    return jsonify({"error": f"Service '{service_name}' not found"}), 404
            else:
                # Kiểm tra toàn bộ hệ thống
                health = self.admin_service.get_system_health()
                status_code = 200 if health['overall_status'] == 'healthy' else 503
                return jsonify(health), status_code
                
        except Exception as e:
            return jsonify({"error": f"Health check failed: {str(e)}"}), 500

    def list_services(self):
        """Lấy danh sách các service"""
        try:
            services = self.admin_service.get_service_list()
            return jsonify({"services": services, "count": len(services)}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to list services: {str(e)}"}), 500

    def get_system_stats(self):
        """Lấy thống kê hệ thống"""
        try:
            user_stats = self.admin_service.get_user_statistics()
            health_stats = self.admin_service.get_system_health()
            
            return jsonify({
                "user_statistics": user_stats,
                "service_health": health_stats,
                "timestamp": int(time.time())
            }), 200
        except Exception as e:
            return jsonify({"error": f"Failed to get system stats: {str(e)}"}), 500

    def list_users(self, role=None):
        """Lấy danh sách người dùng theo role"""
        try:
            if role == 'student':
                users = self.admin_service.user_service.get_all_students()
            elif role == 'teacher':
                users = self.admin_service.user_service.get_all_teachers()
            else:
                # Lấy tất cả người dùng
                students = self.admin_service.user_service.get_all_students()
                teachers = self.admin_service.user_service.get_all_teachers()
                users = students + teachers
                
            return jsonify({"users": users, "count": len(users), "role": role}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to list users: {str(e)}"}), 500

    def add_specialized_user(self, data):
        """Thêm user mới với role cụ thể (teacher hoặc admin)"""
        try:
            # Lấy data từ JSON
            username = data.get('username')
            password = data.get('password')
            role = data.get('role')
            
            # Validate input
            if not username or not password or not role:
                return jsonify({
                    "success": False,
                    "error": "username, password, and role are required"
                }), 400
            
            # Validate role
            if role not in ['teacher', 'admin']:
                return jsonify({
                    "success": False,
                    "error": "role must be 'teacher' or 'admin'"
                }), 400
            
            # Add user through admin service
            result = self.admin_service.add_specialized_user(username, password, role)
            
            if result.get('success'):
                return jsonify({
                    "success": True,
                    "message": f"User '{username}' with role '{role}' added successfully",
                    "user": result.get('user', {})
                }), 201
            else:
                return jsonify({
                    "success": False,
                    "error": result.get('error', 'Failed to add user')
                }), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to add user: {str(e)}"
            }), 500

    def change_user_role(self, data):
        """Thay đổi role của user hiện tại"""
        try:
            user_id = data.get('user_id')
            new_role = data.get('new_role')
            
            if not user_id or not new_role:
                return jsonify({
                    "success": False,
                    "error": "user_id and new_role are required"
                }), 400
            
            # Validate role
            if new_role not in ['student', 'teacher', 'admin']:
                return jsonify({
                    "success": False,
                    "error": "new_role must be 'student', 'teacher', or 'admin'"
                }), 400
            
            result = self.admin_service.change_user_role(user_id, new_role)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to change user role: {str(e)}"
            }), 500

    def add_permission(self, data):
        """Thêm permission mới cho role"""
        try:
            # Lấy data từ JSON
            role = data.get('role')
            path = data.get('path')
            service = data.get('service')
            method = data.get('method')
            
            # Validate input
            if not all([role, path, service, method]):
                return jsonify({
                    "success": False,
                    "error": "role, path, service, and method are required"
                }), 400
            
            # Validate role
            if role not in ['student', 'teacher', 'admin']:
                return jsonify({
                    "success": False,
                    "error": "role must be 'student', 'teacher', or 'admin'"
                }), 400
            
            # Validate method
            if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE']:
                return jsonify({
                    "success": False,
                    "error": "method must be 'GET', 'POST', 'PUT', or 'DELETE'"
                }), 400
            
            # Add permission through admin service
            result = self.admin_service.add_permission(role, path, service, method.upper())
            
            if result.get('success'):
                return jsonify({
                    "success": True,
                    "message": f"Permission added for role '{role}' on {method.upper()} {service}/{path}",
                    "permission": result.get('permission', {})
                }), 201
            else:
                return jsonify({
                    "success": False,
                    "error": result.get('error', 'Failed to add permission')
                }), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to add permission: {str(e)}"
            }), 500

    def list_permissions(self, data):
        """Lấy danh sách permissions với filter optional"""
        try:
            role = data.get('role') if data else None
            service = data.get('service') if data else None
            
            result = self.admin_service.list_permissions(role, service)
            
            if result.get('success'):
                return jsonify({
                    "success": True,
                    "permissions": result.get('permissions', []),
                    "count": len(result.get('permissions', [])),
                    "filters": {
                        "role": role,
                        "service": service
                    }
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": result.get('error', 'Failed to list permissions')
                }), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to list permissions: {str(e)}"
            }), 500

    def delete_permission(self, data):
        """Xóa permission"""
        try:
            role = data.get('role')
            path = data.get('path')
            service = data.get('service')
            method = data.get('method')
            
            if not all([role, path, service, method]):
                return jsonify({
                    "success": False,
                    "error": "role, path, service, and method are required to delete permission"
                }), 400
            
            result = self.admin_service.delete_permission(role, path, service, method.upper())
            
            if result.get('success'):
                return jsonify({
                    "success": True,
                    "message": f"Permission removed for role '{role}' on {method.upper()} {service}/{path}"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": result.get('error', 'Failed to delete permission')
                }), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to delete permission: {str(e)}"
            }), 500

    def check_permission(self, data):
        """Kiểm tra permission cho một route cụ thể"""
        try:
            role = data.get('role')
            path = data.get('path')
            service = data.get('service')
            method = data.get('method')
            
            if not all([role, path, service, method]):
                return jsonify({
                    "success": False,
                    "error": "role, path, service, and method are required"
                }), 400
            
            result = self.admin_service.check_permission(role, path, service, method.upper())
            
            return jsonify({
                "success": True,
                "has_permission": result.get('has_permission', False),
                "check_details": {
                    "role": role,
                    "path": path,
                    "service": service,
                    "method": method.upper()
                }
            }), 200
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to check permission: {str(e)}"
            }), 500

    def get_role_permissions(self, data):
        """Lấy tất cả permissions của một role"""
        try:
            role = data.get('role')
            
            if not role:
                return jsonify({
                    "success": False,
                    "error": "role is required"
                }), 400
            
            result = self.admin_service.get_role_permissions(role)
            
            if result.get('success'):
                return jsonify({
                    "success": True,
                    "role": role,
                    "permissions": result.get('permissions', []),
                    "count": len(result.get('permissions', []))
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": result.get('error', 'Failed to get role permissions')
                }), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get role permissions: {str(e)}"
            }), 500