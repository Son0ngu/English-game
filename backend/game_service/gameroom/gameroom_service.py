from game_service.gameroom.game_logic_handler import game_logic_handler
from game_service.gameroom.gameroom import gameroom
class game_service:
    def __init__(self):
        self.gameroom = gameroom
        self.game_room_list = {}
        self.game_logic_handler = game_logic_handler

    def create_game_room(self,student_id):
        self.game_room_list[student_id] = self.gameroom(student_id,self.game_logic_handler)

    def  get_game_room_state(self,student_id):
        room = self.game_room_list.get(student_id)
        return room.status if room else None

    def get_question(self,student_id):
        room = self.game_room_list.get(student_id).game_logic_handler
        if room:
            return room.get_question(room.difficulty)
        return None

    def check_answer(self,student_id,answer):
        room = self.game_room_list.get(student_id).game_logic_handler
        if room:
            return room.check_answer(answer)
        return None
