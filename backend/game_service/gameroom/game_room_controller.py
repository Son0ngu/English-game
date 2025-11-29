from game_service.gameroom.gameroom_service import game_service
class game_room_controller:
    def __init__(self):
        pass        
    def create_game_room(self,student_id):
        game_service.create_game_room(student_id)