from game_service.gameroom.gameroom import gameroom
class game_service:
    def __init__(self):
        self.game_room = None
        self.game_room_list = {}

    def create_game_room(self,student_id):
        self.game_room_list[student_id] = gameroom(student_id)

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
