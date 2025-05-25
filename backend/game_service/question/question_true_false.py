from game_service.question.question import Question
from flask import jsonify
class question_true_false(Question):
    def __init__(self, difficulty, question, answer):
        super().__init__(difficulty, question,answer)

    def check_answer(self, answer):
        return answer == self.answer

    def get_choices(self):
        return ["True", "False"]

    def get_question(self):
        return jsonify({
            "question": self.question,
            "answer": "",
            "type": "true_false"
        })