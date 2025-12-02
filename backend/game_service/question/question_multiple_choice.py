from game_service.question.question import QuestionAbstract
import array
from flask import jsonify

class question_multiple_choice(QuestionAbstract):
    def __init__(self, difficulty, question, ans1, ans2, ans3, ans4, answer:array):
        super().__init__(difficulty, question,answer)
        self.ans1 = ans1
        self.ans2 = ans2
        self.ans3 = ans3
        self.ans4 = ans4

    def check_answer(self, selected):
        return selected in self.answer

    def get_choices(self):
        return [self.ans1, self.ans2, self.ans3, self.ans4]

    def get_question(self):
        return jsonify({
            "question": self.question,
            "ans1": self.ans1,
            "ans2": self.ans2,
            "ans3": self.ans3,
            "ans4": self.ans4,
            "type": "multiple_choice"
        })
