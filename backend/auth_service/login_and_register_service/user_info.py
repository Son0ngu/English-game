class user_info:
    def __init__(self, username,password):
        self.username = username
        self.password = password
        
    def add_user_id_only(self, user_id, role="student"):
        """Add user với role được chỉ định"""
        return self.user_profile_service.add_user_with_role(user_id, role)