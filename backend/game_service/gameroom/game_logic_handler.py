import random

from flask import jsonify

from game_service.question.game_resource_interface import game_resource_interface

class game_logic_handler:
    def __init__(self,player_hp, player_atk, monster_hp, monster_atk,difficulty):
        self.hp= player_hp
        self.atk= player_atk
        self.monster_hp= monster_hp
        self.monster_atk= monster_atk
        self.difficulty= difficulty
        self.question = None

    def get_question(self,difficulty):
        question_type = random.randint(1, 4)
        self.question = game_resource_interface.get_question(difficulty, question_type)
        choices = self.question.get_choices()
        return choices

    def check_answer(self, answer):
        if self.question.check_answer(answer):
            print("Correct!")
            self.monster_hp -= self.atk
            if self.monster_hp <= 0:
                print("You win!")

        else:
            print("Wrong!")
            self.hp -= self.monster_atk
            if self.hp <= 0:
                print("You lose!")








