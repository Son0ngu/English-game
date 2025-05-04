from flask import jsonify

import game_service.gameroom.game_room_controller
class services_route:
    def __init__(self):
        pass

    def admin_service(self,destination, data, method):
        pass
    def auth_service(self,destination, data, method):
        pass
    def classroom_service(self,destination, data, method):
        pass
    def course_service(self,destination, data, method):
        pass
    def game_service(self,destination, data, method):
        if destination == 'newroom' and method=='POST':
            student_id = data.get('student_id')
            if student_id:
                game_service.gameroom.game_room_controller.game_room_controller.create_game_room(student_id)
                return jsonify({"message": "Game room created successfully"}), 200
            else:
                return jsonify({"error": "Student ID is required"}), 400
        return None

    def progress_service(self,destination, data, method):
        pass
    def user_service(self,destination, data, method):
        pass
    def feedback_service(self,destination, data, method):
        pass
