from auth_service.login_and_register_service.auth_service_database_interface import auth_service_database_interface

class login_service:
    def __init__(self):
        self.auth_service_database_interface = auth_service_database_interface()
        pass
    def login(self, username, password):
        if self.auth_service_database_interface.login(username, password):
            return True
        return False