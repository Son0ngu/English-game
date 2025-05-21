from flask import Flask, request, jsonify
from api_gateway.services_route import services_route

class gateway_service:
    def __init__(self, app):
        self.app = app
        self.services = services_route()
        self.service_list=["admin", "auth", "classroom", "course", "game", "progress", "user", "feedback", "item"]  # Thêm "item" vào danh sách
        self.register_routes()
        
    def register_routes(self):
        """Register the route handler with Flask"""
        @self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def handle_request(path):
            return self.new_request(path)
            
    def new_request(self, path):
        """Process and route incoming requests to appropriate service"""
        # Extract original request data
        method = request.method
        headers = dict(request.headers)
        data = request.get_json() if request.is_json else {}
        
        # Add query params to data
        query_params = request.args.to_dict()
        if query_params:
            data.update(query_params)
        
        # Parse the path to identify service and destination
        path_parts = path.split('/')
        service_requested = path_parts[0] if path_parts else ""
        destination = '/'.join(path_parts[1:]) if len(path_parts) > 1 else ""
        
        # Check if the service requested is in the list of services
        if service_requested in self.service_list:
            # Map service names to methods on the services_route instance
            service_methods = {
                "admin": self.services.admin_service,
                "auth": self.services.auth_service,
                "classroom": self.services.classroom_service,
                "course": self.services.course_service,
                "game": self.services.game_service,
                "progress": self.services.progress_service,
                "user": self.services.user_service,
                "feedback": self.services.feedback_service,
                "item": self.services.item_service  # Thêm xử lý item_service
            }
            
            # Call the appropriate service method
            method_to_call = service_methods.get(service_requested)
            if method_to_call:
                response = method_to_call(destination, data, method)
                if response:
                    return response
                
            return jsonify({"error": "Endpoint not implemented"}), 501
        else:
            return jsonify({"error": "Service not found"}), 404

