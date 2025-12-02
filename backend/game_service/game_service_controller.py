from game_service.gameroom.game_room_controller import game_room_controller
class game_service_controller:
    def __init__(self):
        self.game_room_controller = game_room_controller()

    def create_game_room(self, student_id,difficulty):
        return self.game_room_controller.create_game_room(student_id,difficulty)

    def get_game_room_state(self, session_id):
        return self.game_room_controller.get_game_room_state(session_id)

    def get_question(self, session_id):
        return self.game_room_controller.get_question(session_id)

    def check_answer(self, session_id, answer):
        return self.game_room_controller.check_answer(session_id, answer)