from flask import jsonify

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

    def create_game_room(self, student_id, difficulty, class_id):
        try:
            session_id = str(uuid.uuid4())
            #atk = atk[0] if isinstance(atk, (list, tuple)) else atk
            stats = self.user_service.get_user_stats_only(student_id)
            atk = stats["atk"]
            hp = stats["hp"]

            if atk is None or hp is None:
                raise ValueError("Stats not found")
            
            print("DEBUG:", atk, type(atk), hp, type(hp))

            if atk is None or hp is None:
                raise ValueError("Stats not found")
            monster = self.monster_service.create_monster_based_on_difficulty(
                student_id, difficulty, hp, atk
            )
            logic = game_logic_handler(
                hp, atk,
                monster.monster_hp,
                monster.monster_atk,
                difficulty
            )
            room = self.game_room(
                session_id, student_id, logic,
                difficulty, monster, monster.money_win
            )
            room.status = 0
            self.game_room_list[session_id] = room
            self.student_id_to_session_id[student_id] = session_id
            return jsonify({
                "session_id": session_id,
                "student_id": student_id,
                "class_id": class_id,
                "difficulty": difficulty,
                "status": room.status,
                "player_stats": {
                    "hp": hp,
                    "atk": atk
                },
                "monster_stats": {
                    "hp": monster.monster_hp,
                    "atk": monster.monster_atk,
                    "money_win": monster.money_win
                }
            })

        except Exception as e:
            return jsonify({"error": f"Internal error in game_room_controller: {str(e)}"}), 500
    def get_game_room_state(self,student_id):
        session_id = self.student_id_to_session_id.get(student_id)
        room = self.game_room_list.get(session_id)
        return room.status if room else None

    def get_question(self,session_id,class_id):
        room = self.game_room_list.get(session_id).game_logic_handler
        if room:
            return room.get_question(class_id)
        return None

    def check_answer(self,session_id,answer,question_id):
        room = self.game_room_list.get(session_id).game_logic_handler
        if room:
            result = room.check_answer(answer,question_id)
            if result["status"] == "win":
                self.game_room_list[session_id].status = 1
                Timer(30 * 60, self.trigger_game_room_deletion, args=[session_id]).start()
                return jsonify(result)
            elif result["status"] == "lose":
                self.game_room_list[session_id].status = 2
                Timer(30 * 60, self.trigger_game_room_deletion, args=[session_id]).start()
                return jsonify(result)
            else:
                return jsonify(result)
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

