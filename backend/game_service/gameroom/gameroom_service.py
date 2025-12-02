from game_service.gameroom.game_logic_handler import game_logic_handler
from game_service.gameroom.gameroom import gameroom
from game_service.monster.monster_service import monster_service
from user_profile_service.user.user_service import UserProfileService as userService
import uuid
from threading import Timer
class game_service:
    def __init__(self):
        self.game_room = gameroom
        self.game_room_list = {}
        self.student_id_to_session_id = {}
        self.user_service = userService()
        self.monster_service = monster_service()

    def create_game_room(self,student_id,difficulty,class_id):
        session_id=uuid.uuid1()
        atk, hp = self.user_service.get_user_stats_only(student_id)
        monster = self.monster_service.create_monster_based_on_difficulty(student_id,difficulty,hp,atk)
        monster_hp = monster.monster_hp
        monster_atk = monster.monster_atk
        money_win = monster.money_win
        game_logic_handler_instance = game_logic_handler(hp, atk, monster_hp, monster_atk, difficulty)
        self.game_room_list[session_id] = self.game_room(session_id, student_id, game_logic_handler_instance,difficulty,monster,money_win)
        self.student_id_to_session_id[student_id]=session_id
        self.game_room_list[session_id].status = 0
        return {
            "session_id": session_id,
            "student_id": student_id,
            "class_id": class_id,
            "difficulty": difficulty,
            "status": self.game_room_list[session_id].status,
            "player_stats": {
                "hp": hp,
                "atk": atk
            },
            "monster_stats": {
                "hp": monster_hp,
                "atk": monster_atk,
                "money_win": money_win
            }
        }

    def get_game_room_state(self,student_id):
        session_id = self.student_id_to_session_id.get(student_id)
        room = self.game_room_list.get(session_id)
        return room.status if room else None

    def get_question(self,session_id):
        room = self.game_room_list.get(session_id).game_logic_handler
        if room:
            return room.get_question()
        return None

    def check_answer(self,session_id,answer):
        room = self.game_room_list.get(session_id).game_logic_handler
        if room:
            result = room.check_answer(answer)
            if result["status"] == "win":
                self.game_room_list[session_id].status = 1
                Timer(30 * 60, self.trigger_game_room_deletion, args=[session_id]).start()
                return result
            elif result["status"] == "lose":
                self.game_room_list[session_id].status = 2
                Timer(30 * 60, self.trigger_game_room_deletion, args=[session_id]).start()
                return result
            else:
                return result
        return None

    def trigger_game_room_deletion(self, session_id):
        if session_id in self.game_room_list:
            del self.game_room_list[session_id]
            for student_id, sid in list(self.student_id_to_session_id.items()):
                if sid == session_id:
                    del self.student_id_to_session_id[student_id]
                    print(f"Game room {session_id} has been deleted due to inactivity.")
                    break
        else:
            print(f"Game room {session_id} not found for deletion, might already removed")

