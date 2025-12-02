from flask import jsonify
from admin_service.admin_service import AdminService
import psutil
import time

class AdminController:
    def __init__(self, admin_service):  # Loại bỏ type hint
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
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            total_ram = memory.total  # Total RAM in bytes
            used_ram = memory.used  # Used RAM in bytes
            free_ram = memory.available  # Available RAM in bytes
            ram_usage_percent = memory.percent
            return jsonify({
                "user_statistics": user_stats,
                "service_health": health_stats,
                "timestamp": int(time.time()),
                "cpu_usage_percent": cpu,
                "ram": {
                    "total": total_ram,
                    "used": used_ram,
                    "free": free_ram,
                    "usage_percent": ram_usage_percent
                }
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

    def add_specialized_user(self, username, password, role):
        try:
            result = self.admin_service.add_specialized_user(username, password, role)
            if result:
                return jsonify({"success": True, "message": f"User {username} added successfully"}), 201
            else:
                return jsonify({"success": False, "error": "Failed to add user"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to add user: {str(e)}"}), 500