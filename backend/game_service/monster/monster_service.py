import game_service.monster.monster as monster
class monster_service:
    def __init__(self):
        pass

    def create_monster_based_on_difficulty(self,student_id,student_difficulty,student_hp,student_atk):
        print("stop monster service")
        print(type(student_atk), type(student_hp), type(student_difficulty)) 
        try:
            new_monster = monster.monster()
            if student_difficulty == "easy":
                student_atk = int(student_atk)
                student_hp = int(student_hp)    

                print("student_atk:", student_atk)
                print("student_hp:", student_hp)

                new_monster.monster_hp = student_atk * 7
                new_monster.monster_atk = int(student_hp / 6)
                new_monster.money_win = 10
            elif student_difficulty == "medium":
                new_monster.monster_hp = student_atk * 10
                new_monster.monster_atk = int(student_hp / 5)
                new_monster.money_win = 20
            elif student_difficulty == "hard":
                new_monster.monster_hp = student_atk * 12
                new_monster.monster_atk = int(student_hp / 4)
                new_monster.money_win = 50
            elif student_difficulty == "very hard":
                new_monster.monster_hp = student_atk * 15
                new_monster.monster_atk = int(student_hp / 3)
                new_monster.money_win = 150
            print(new_monster.monster_hp)
            print(new_monster.monster_atk)
            print(new_monster.money_win)
            return new_monster
        except Exception as e:
            print("💥 Monster service error:", e)
            raise