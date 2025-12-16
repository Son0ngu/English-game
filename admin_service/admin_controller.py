from flask import jsonify
import psutil
import time

class AdminController:
    
    def __init__(self, admin_service):
        self.admin_service = admin_service

    def _standard_response(self, success=True, data=None, message=None, error=None, status_code=200):
        """Chuẩn hóa response format"""
        response = {
            "success": success,
            "timestamp": int(time.time())
        }
        
        if data is not None:
            response["data"] = data
        if message:
            response["message"] = message
        if error:
            response["error"] = error
            
        return jsonify(response), status_code

    def check_health(self, service_name=None):
        """Health check với response chuẩn"""
        try:
            if service_name:
                services = self.admin_service.services
                if service_name in services:
                    service = services[service_name]
                    health = service.check_internal() if hasattr(service, 'check_internal') else {"status": "unknown"}
                    return self._standard_response(data={"service": service_name, "health": health})
                else:
                    return self._standard_response(False, error=f"Service '{service_name}' not found", status_code=404)
            else:
                health = self.admin_service.get_system_health()
                status_code = 200 if health['overall_status'] == 'healthy' else 503
                return self._standard_response(data=health, status_code=status_code)
                
        except Exception as e:
            return self._standard_response(False, error=f"Health check failed: {str(e)}", status_code=500)

    def list_services(self):
        """Lấy danh sách các service - Chuẩn hóa response"""
        try:
            services = self.admin_service.get_service_list()
            return self._standard_response(data={
                "services": services,
                "count": len(services)
            })
        except Exception as e:
            return self._standard_response(False, error=f"Failed to list services: {str(e)}", status_code=500)

    def get_system_stats(self):
        """System stats - Tránh loop bằng cách không gọi health check"""
        try:
            # CHỈ lấy user statistics, KHÔNG gọi health
            user_stats = self.admin_service.get_user_statistics()
            
            # Lấy service count trực tiếp
            service_info = {
                "registered_services": len(self.admin_service.services),
                "service_names": list(self.admin_service.services.keys())
            }
            
            return self._standard_response(data={
                "user_statistics": user_stats,
                "service_info": service_info,
                "timestamp": int(time.time())
            })
            
        except Exception as e:
            return self._standard_response(False, error=f"Failed to get system stats: {str(e)}", status_code=500)

    def list_users(self, role):
        """Lấy danh sách người dùng theo role - Chuẩn hóa response"""
        try:
            if role == 'student':
                users = self.admin_service.user_service.get_all_students()
            elif role == 'teacher':
                users = self.admin_service.user_service.get_all_teachers()
            elif role == 'None' or role == 'all':
                students = self.admin_service.user_service.get_all_students()
                teachers = self.admin_service.user_service.get_all_teachers()
                users = students + teachers
            
            #  Sử dụng standard response format
            return self._standard_response(data={
                "users": users,
                "count": len(users),
                "filter": role
            })
            
        except Exception as e:
            return self._standard_response(False, error=f"Failed to list users: {str(e)}", status_code=500)

    def add_specialized_user(self, data):
        print('gọi hàm add_specialized_user', data)
        """Thêm user mới với validation enhanced"""
        try:
            #  Enhanced validation
            required_fields = ['username', 'password', 'role']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return self._standard_response(
                    False, 
                    error=f"Missing required fields: {', '.join(missing_fields)}", 
                    status_code=400
                )
            
            username = data.get('username').strip()
            password = data.get('password')
            role = data.get('role').lower()
            
            # Validate username format
            if len(username) < 3:
                return self._standard_response(False, error="Username must be at least 3 characters", status_code=400)
            
            # Validate password strength
            if len(password) < 6:
                return self._standard_response(False, error="Password must be at least 6 characters", status_code=400)
            
            # Validate role
            if role not in ['teacher', 'admin']:
                return self._standard_response(False, error="Role must be 'teacher' or 'admin'", status_code=400)
            
            result = self.admin_service.add_specialized_user(username, password, role)
            
            if result.get('success'):
                return self._standard_response(data={
                    "message": f"User '{username}' with role '{role}' added successfully",
                    "user": result.get('user', {})
                }, status_code=201)
            else:
                return self._standard_response(False, error=result.get('error', 'Failed to add user'), status_code=400)
            
        except Exception as e:
            return self._standard_response(False, error=f"Failed to add user: {str(e)}", status_code=500)

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