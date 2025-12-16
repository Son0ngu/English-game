from flask import jsonify

import game_service.question.question
from game_service.question.question_fill_in_the_blank import question_fill_in_the_blank
from game_service.question.question_multiple_choice import question_multiple_choice
from game_service.question.question_true_false import question_true_false
from game_service.question.question4 import question4
from classroom_service.classroom_service import ClassroomService as classroom_service

class game_resource_interface:
    def __init__(self):
        self.classroom_service = classroom_service()
        pass

    def get_question(self,class_id, difficulty,qtype):
        QUESTION_TYPES = {
            1: "multiple_choice",
            2: "fill_in_the_blank",
            3: "true_false",
            4: "single_choice"
        }
        qtype_str = QUESTION_TYPES.get(qtype)
        question = self.classroom_service.get_questions_by_criteria(class_id,difficulty,qtype_str)
        print(question)
        print("stopstopstopstop")
        return jsonify(question)

    # Question type:
    # 1: Multiple choice: difficulty, question, ans1, ans2, ans3, ans4, right_answer[array]
    # 2: True/False: difficulty, question, answer
    # 3: Fill in the blank: difficulty, question, answer
    # 4: Single choice: difficulty, question, ans1, ans2, ans3, ans4, right_answer

    # Difficulty:
    # 1: Easy
    # 2: Medium
    # 3: Hard
    # 4: Give me god of Eng

