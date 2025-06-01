from flask import jsonify
from game_service.gameroom.gameroom_service import game_service

class game_room_controller:
    def __init__(self):
        self.game_service = game_service()
        pass

    def create_game_room(self, student_id,difficulty):
        if student_id:
            response = self.game_service.create_game_room(student_id,difficulty)
            return jsonify(response), 200
        else:
            print("Student ID is required")
            return jsonify({"error": "Error"}), 400

    def get_game_room_state(self, session_id):
        return self.game_service.get_game_room_state(session_id)

    def get_question(self, session_id):
        return self.game_service.get_question(session_id)

    def check_answer(self, session_id, answer):
        return self.game_service.check_answer(session_id, answer)