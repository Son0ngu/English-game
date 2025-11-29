class game_service:
    def __init__(self):
        self.game_room = None
        self.game_room_list = []

    def create_game_room(self,student_id):
        self.game_room = game_room()
        self.game_room.student_id = student_id
        self.game_room_list.append(self.game_room)
        return self.game_room