from game_service.question.question import Question


class question4(Question):
    def __init__(self, difficulty, question, ans1, ans2, ans3, ans4, answer):
        super().__init__(difficulty, question, answer)
        self.ans1=ans1
        self.ans2=ans2
        self.ans3=ans3
        self.ans4=ans4
    def check_answer(self,answer):
        if answer==self.answer:
            return True
        else:
            return False

    def get_choices(self):
        return [self.ans1, self.ans2, self.ans3, self.ans4]