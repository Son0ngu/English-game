import random
from classroom_service.classroom_service import ClassroomService
from flask import jsonify
from game_service.question.question import QuestionAbstract

from game_service.question.game_resource_interface import game_resource_interface

class game_logic_handler:
    def __init__(self,player_hp, player_atk, monster_hp, monster_atk,difficulty):
        self.hp= player_hp
        self.atk= player_atk
        self.monster_hp= monster_hp
        self.monster_atk= monster_atk
        self.difficulty= difficulty
        self.game_resource_interface = game_resource_interface()
        self.question = None # Placeholder for the question object
        self.classroom_service = ClassroomService()

    def get_question(self,class_id):
        question_type = random.randint(1, 4)
        question = self.game_resource_interface.get_question(class_id,self.difficulty, question_type)
        print(question)
        print("stopstopstop")
        return question

    def check_answer(self, answer,question_id):
        print("debug2")
        difficulty,question,answer_true = self.classroom_service.get_question_by_id_minimal(question_id)
        print("debug")
        print("dap an dung la:" ,answer_true)
        print("Monster HP:", self.monster_hp)
        print("Attack Dmg:", self.monster_atk)
        print("Player HP:", self.hp)
        if answer_true == answer:
            print("Correct!")
            self.monster_hp -= self.atk
            if self.monster_hp <= 0:
                print("You win!")
                return {"status": "win"}
            return {
                "status": "correct",
                "monster_hp": self.monster_hp,
                "player_hp": self.hp
            }

        else:
            print("Wrong!")
            self.hp -= self.monster_atk
            if self.hp <= 0:
                print("You lose!")
                return {"status": "lose"}
            return {
                "status": "incorrect",
                "monster_hp": self.monster_hp,
                "player_hp": self.hp
            }








