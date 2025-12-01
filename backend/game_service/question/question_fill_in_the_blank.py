from game_service.question.question import Question
import re
def normalize(text):
    return re.sub(r'\W+', '', text.lower())

class question_fill_in_the_blank(Question):
    def __init__(self, difficulty, question,answer):
        super().__init__(difficulty, question,answer)

    def check_answer(self, answer):
        return normalize(answer) == normalize(self.answer)

    def get_choices(self):
        return ""