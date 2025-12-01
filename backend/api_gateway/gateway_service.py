from flask import Flask, request, jsonify
from api_gateway.services_route import services_route
import requests
class gateway_service:
    def __init__(self, app):
        self.app = app
        self.services_route = services_route()
        self.service_list=["admin", "auth", "classroom", "course", "game", "progress", "user","feedback"]
    def new_request(self,path):
        # Extract original request data
        method = request.method
        headers = dict(request.headers)
        data = request.get_json() or {}
        full_path = "/" + path
        service_requested = full_path.split("/")[1]
        try:
            destination = full_path.split("/")[2]
        except:
            destination = ""

        # Check if the service requested is in the list of services
        if service_requested in self.service_list:
            if service_requested == "admin":
                return self.services_route.admin_service(destination, data,method)
            if service_requested == "auth":
                return self.services_route.auth_service(destination, data,method)
            if service_requested == "classroom":
                return self.services_route.classroom_service(destination, data,method)
            if service_requested == "course":
                return self.services_route.course_service(destination, data,method)
            if service_requested == "game":
                return self.services_route.game_service(destination, data,method)
            if service_requested == "progress":
                return self.services_route.progress_service(destination, data,method)
            if service_requested == "user":
                return self.services_route.user_service(destination, data,method)
            if service_requested == "feedback":
                return self.services_route.feedback_service(destination, data,method)


            else:
                return jsonify({"error": "Requested not found"}), 404
        else:
            return jsonify({"error": "Requested not found"}), 404

