from abc import ABC, abstractmethod

class QuestionAbstract(ABC):
    def __init__(self, difficulty, question,answer):
        self.difficulty = difficulty
        self.question = question
        self.answer = answer

    @abstractmethod
    def check_answer(self, user_input):
        pass

    def get_choices(self):
        pass

    def get_question(self):
        pass