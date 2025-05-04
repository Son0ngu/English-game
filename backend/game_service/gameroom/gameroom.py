import user
class gameroom:
    def __init__(self,student_id):
        self.student_id=student_id
        self.difficulty=user.get_student_difficulty(student_id)
        self.hp = user.get_hp(student_id)
        self.atk=user.get_atk(student_id)
        self.monster_hp=""
        self.monster_atk=""
        self.session_id=""
        self.status=0

