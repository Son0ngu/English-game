import game_service.question.question
from game_service.question.question_fill_in_the_blank import question_fill_in_the_blank
from game_service.question.question_multiple_choice import question_multiple_choice
from game_service.question.question_true_false import question_true_false
from game_service.question.question4 import question4
import question_service as question_service

class game_resource_interface:
    def __init__(self):
        pass

    def get_question(self, difficulty,qtype):
        question = question_service.get_question(difficulty,qtype)
        return question

    # Question type:
    # 1: Multiple choice: difficulty, question, ans1, ans2, ans3, ans4, right_answer[array]
    # 2: True/False: difficulty, question, answer
    # 3: Fill in the blank: difficulty, question, answer
    # 4: Single choice: difficulty, question, ans1, ans2, ans3, ans4, right_answer
    def add_question(self, question,difficulty,qtype,ans1,ans2,ans3,ans4,right_answer,answer):
        if qtype == 1:
            question = question_multiple_choice(difficulty, question, ans1, ans2, ans3, ans4, right_answer)
            question_service.add_question(question)
        elif qtype == 2:
            question = question_true_false(difficulty, question, answer)
            question_service.add_question(question)
        elif qtype == 3:
            question = question_fill_in_the_blank(difficulty, question, answer)
            question_service.add_question(question)
        elif qtype == 4:
            question = question4(difficulty, question, ans1, ans2, ans3, ans4, right_answer)
            question_service.add_question(question)