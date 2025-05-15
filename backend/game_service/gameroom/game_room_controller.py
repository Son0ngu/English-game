from game_service.gameroom.gameroom_service import game_service

class game_room_controller:
    def __init__(self):
        self.game_service = game_service
        pass

    def create_game_room(self, student_id):
        game_service.create_game_room(student_id)

    def get_game_room_state(self, student_id):
        return game_service.get_game_room_state(student_id)

    def get_question(self, student_id):
        return game_service.get_question(student_id)

    def check_answer(self, student_id, answer):
        return game_service.check_answer(student_id, answer)