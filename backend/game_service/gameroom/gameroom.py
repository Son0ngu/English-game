from user_profile_service.user.user_service import UserProfileService as userService
from game_service.monster.monster_service import monster_service
class gameroom:
    def __init__(self,session_id,student_id,game_logic_handler,difficulty,monster,money_win):
        self.user_service = userService()
        self.student_id=student_id
        self.money_win= money_win
        self.session_id= session_id
        self.difficulty = difficulty
        self.monster = monster
        self.status=0
        self.game_logic_handler = game_logic_handler

        # status 0: playing
        # status 1: win
        # status 2: lose

