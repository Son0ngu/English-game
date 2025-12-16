from auth_service.login_and_register_service.login_service import login_service
from auth_service.login_and_register_service.signup_service import signup_service
from auth_service.role_permission_service.permission_service import permission_service
from auth_service.login_and_register_service.auth_service_database_interface import auth_service_database_interface

class auth_service_controller:
    def __init__(self):
        self.login_service = login_service()
        self.signup_service = signup_service()
        self.permission_service = permission_service()
        self.auth_service_database_interface = auth_service_database_interface()
        pass

    def login(self, username, password):
        return self.login_service.login(username, password)

    def sign_up(self, username, password):
        return self.signup_service.sign_up(username, password)

    def get_id_from_username(self, username):
        return self.auth_service_database_interface.get_id_from_username(username)

    def get_role_from_id(self, user_id):
        return self.auth_service_database_interface.get_role_from_id(user_id)

    def check_permission(self, role,path,service,method):
        return self.permission_service.check_permission(role,path,service,method)

    def add_permission(self, role, path, service, method):
        return self.permission_service.add_permission(role, path, service, method)



