import user
from game_service.monster.monster_service import monster_service
class gameroom:
    def __init__(self,session_id,student_id,game_logic_handler):
        self.monster_service = monster_service()
        self.student_id=student_id
        self.difficulty=user.get_student_difficulty(student_id)
        self.hp = user.get_hp(student_id)
        self.atk=user.get_atk(student_id)
        self.monster= self.monster_service.create_monster_based_on_difficulty(student_id)
        self.monster_hp= self.monster.monster_hp
        self.monster_atk= self.monster.monster_atk
        self.money_win= self.monster.money_win
        self.session_id= session_id
        self.status=0
        self.game_logic_handler = game_logic_handler(self.hp, self.atk, self.monster_hp, self.monster_atk,self.difficulty)

        # status 0: playing
        # status 1: win
        # status 2: lose

