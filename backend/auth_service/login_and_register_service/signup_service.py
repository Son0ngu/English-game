from auth_service.login_and_register_service.auth_service_database_interface import auth_service_database_interface

class signup_service:
    def __init__(self):
        self.auth_service_database_interface = auth_service_database_interface()

    def sign_up(self, username, password):
        if not self.auth_service_database_interface.check_if_user_exist(username):
            user_id = user.new_id()
            # admin va teacher se dc add o admin panel
            self.auth_service_database_interface.add_user(user_id, username, password,role="student")
            return True
        else:
            print("User already exists (signup_service.sign_up)")
            return False