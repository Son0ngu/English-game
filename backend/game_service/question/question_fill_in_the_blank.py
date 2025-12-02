from game_service.question.question import QuestionAbstract
import re
from flask import jsonify
def normalize(text):
    return re.sub(r'\W+', '', text.lower())

class question_fill_in_the_blank(QuestionAbstract):
    def __init__(self, difficulty, question,answer):
        super().__init__(difficulty, question,answer)

    def check_answer(self, answer):
        return normalize(answer) == normalize(self.answer)

    def get_choices(self):
        return ""

    def get_question(self):
        return jsonify({
            "question": self.question,
            "answer": "",
            "type": "fill_in_the_blank"
        })