import game_service.monster.monster as monster
import user
class monster_service:
    def __init__(self):
        self.monster = monster.monster()

    def create_monster_based_on_difficulty(self,student_id):
        student_difficulty = user.get_student_difficulty(student_id)
        student_hp = user.get_hp(student_id)
        student_atk = user.get_atk(student_id)

        if student_difficulty == "easy":
            self.monster.monster_hp = student_hp * 1.05
            self.monster.monster_atk = student_atk * 1.05
            self.monster.money_win = 10

        elif student_difficulty == "medium":
            self.monster.monster_hp = student_hp * 1.5
            self.monster.monster_atk = student_atk * 1.5
            self.monster.money_win = 20

        elif student_difficulty == "hard":
            self.monster.monster_hp = student_hp * 2.2
            self.monster.monster_atk = student_atk * 2.2
            self.monster.money_win = 50

        elif student_difficulty == "give_me_god_of_war":
            self.monster.monster_hp = student_hp * 10
            self.monster.monster_atk = student_atk * 10
            self.monster.money_win = 150

        return self.monster