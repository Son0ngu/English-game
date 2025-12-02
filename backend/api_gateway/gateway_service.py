from flask import request, jsonify
from api_gateway.services_route import services_route

class gateway_service:
    def __init__(self, app):
        self.app = app
        self.services_route = services_route()
        self.service_list = ["admin", "auth", "classroom", "course", "game", "progress", "user", "feedback", "item"]
        
        # Không register routes ở đây vì app.py đã handle
        
    def new_request(self, path):
        """Process and route incoming requests to appropriate service"""
        # Extract original request data
        method = request.method
        headers = dict(request.headers)
        data = request.get_json() or {}
        
        # Add query params to data
        query_params = request.args.to_dict()
        if query_params:
            data.update(query_params)
        
        # Parse path
        full_path = "/" + path if path else "/"
        path_parts = full_path.split("/")[1:] if full_path != "/" else [""]
        service_requested = path_parts[0] if path_parts and path_parts[0] else ""
        
        try:
            destination = "/".join(path_parts[1:]) if len(path_parts) > 1 else ""
        except:
            destination = ""

        # Root endpoint
        if not service_requested:
            return jsonify({
                "message": "English Game API Gateway", 
                "services": self.service_list,
                "status": "running"
            }), 200

        # Check if the service requested is in the list of services
        if service_requested in self.service_list:
            try:
                if service_requested == "admin":
                    return self.services_route.handle_admin_service(destination, data, method)
                elif service_requested == "auth":
                    return self.services_route.authenticating_service(destination, data, method)
                elif service_requested == "classroom":
                    return self.services_route.classroom_service(destination, data, method)
                elif service_requested == "course":
                    return self.services_route.course_service(destination, data, method)
                elif service_requested == "game":
                    return self.services_route.game_service(destination, data, method)
                elif service_requested == "progress":
                    return self.services_route.handle_progress_service(destination, data, method)
                elif service_requested == "user":
                    return self.services_route.handle_user_service(destination, data, method)
                elif service_requested == "feedback":
                    return self.services_route.handle_feedback_service(destination, data, method)
                elif service_requested == "item":
                    return self.services_route.handle_item_service(destination, data, method)
                else:
                    return jsonify({"error": "Service method not implemented"}), 501
                    
            except Exception as e:
                return jsonify({"error": f"Internal server error: {str(e)}"}), 500
        else:
            return jsonify({
                "error": "Service not found", 
                "available_services": self.service_list,
                "requested": service_requested
            }), 404

