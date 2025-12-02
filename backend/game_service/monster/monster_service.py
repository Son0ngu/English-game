import game_service.monster.monster as monster
class monster_service:
    def __init__(self):
        pass

    def create_monster_based_on_difficulty(self,student_id,student_difficulty,student_hp,student_atk):
        new_monster = monster.monster()
        if student_difficulty == 1:
            new_monster.monster_hp = student_hp * 1.05
            new_monster.monster_atk = student_atk * 1.05
            new_monster.money_win = 10

        elif student_difficulty == 2:
            new_monster.monster_hp = student_hp * 1.5
            new_monster.monster_atk = student_atk * 1.5
            new_monster.money_win = 20

        elif student_difficulty == 3:
            new_monster.monster_hp = student_hp * 2.2
            new_monster.monster_atk = student_atk * 2.2
            new_monster.money_win = 50

        elif student_difficulty == 4:
            new_monster.monster_hp = student_hp * 10
            new_monster.monster_atk = student_atk * 10
            new_monster.money_win = 150

        return new_monster