from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from auth_service.auth_service_controller import auth_service_controller
from game_service.gameroom.game_room_controller import game_room_controller
class services_route:
    def __init__(self):
        self.game_room_controller = game_room_controller()
        self.auth_service_controller = auth_service_controller()
        pass
    @jwt_required()
    def admin_service(self,destination, data, method):
        pass
    def auth_service(self,destination, data, method):
        if destination == 'login' and method == 'POST':
            if data.get('username') and data.get('password'):
                username = data.get('username')
                password = data.get('password')
                if self.auth_service_controller.login(username, password):
                    id = self.auth_service_controller.get_id_from_username(username)
                    role = self.auth_service_controller.get_role_from_id(id)
                    additional_claims = {"role": role}
                    access_token = create_access_token(identity=username,additional_claims=additional_claims)
                    print("Crafted access token:", access_token," (service_route)")
                    return {"access_token": access_token}, 200
                else:
                    print("Invalid credentials (service_route)")
                    return {"error": "Invalid credentials"}, 401
            return None

        # Get role from JWT
        # claims = get_jwt()
        # claims.get("role")

        if destination == "signup" and method == 'POST':
            if data.get('username') and data.get('password'):
                username = data.get('username')
                password = data.get('password')
                if self.auth_service_controller.sign_up(username, password):
                    print("User created successfully (service_route)")
                    return {"message": "User created successfully"}, 200
                else:
                    print("User already exists (service_route)")
                    return {"error": "User already exists"}, 400
            return None

        if destination == "add_permission" and method == 'POST':
            jwt_role = get_jwt().get("role")
            role = data.get("role")
            path = data.get("path")
            service = data.get("service")
            method = data.get("method")
            if jwt_role =="admin":
                self.auth_service_controller.add_permission(role, path, service, method)
                print("Permission added successfully (service_route)")
                return {"message": "Permission added successfully"}, 200
        return None

    @jwt_required()
    def classroom_service(self,destination, data, method):
        pass

    @jwt_required()
    def course_service(self,destination, data, method):
        pass

    @jwt_required()
    def game_service(self,destination, data, method):
        if destination == 'newroom' and method=='POST':
            user_id = get_jwt_identity()
            return self.game_room_controller.create_game_room(user_id)
        return None

    @jwt_required()
    def progress_service(self,destination, data, method):
        pass

    @jwt_required()
    def user_service(self,destination, data, method):
        pass

    @jwt_required()
    def feedback_service(self,destination, data, method):
        pass
