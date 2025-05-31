from auth_service.login_and_register_service.auth_service_database_interface import auth_service_database_interface
from user_profile_service.user.user_service import UserProfileService as user
import uuid

class signup_service:
    def __init__(self):
        self.auth_service_database_interface = auth_service_database_interface()
        self.user = user()

    def sign_up(self, username, password):
        if not self.auth_service_database_interface.check_if_user_exist(username):

            user_id = str(uuid.uuid4())
            self.user.add_user_id_only(user_id)
            # admin va teacher se dc add o admin panel
            self.auth_service_database_interface.add_user(user_id, username, password,role="student")
            return True
        else:
            print("User already exists (signup_service.sign_up)")
            return False

    def add_specialized_user(self,username,password,role):
        if not self.auth_service_database_interface.check_if_user_exist(username):
            user_id = str(uuid.uuid4())
            self.user.add_user_id_only(user_id)
            self.auth_service_database_interface.add_user(user_id, username, password,role=role)
            return True
        else:
            print("User already exists (signup_service.add_specialized_user)")
            return False