import uuid
from typing import List

class Question:
    def __init__(self, text: str, difficulty: str, choices: List[str], correct_index: int, q_type: str):
        self.id = str(uuid.uuid4())[:8]
        self.question = text
        self.difficulty = difficulty
        self.choices = choices
        self.correct_index = correct_index
        self.answer = choices[correct_index] if choices else None
        self.type = q_type

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "difficulty": self.difficulty,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

class Topic:
    def __init__(self, title: str, content: str = ''):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.questions: List[Question] = []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "questions": [q.to_dict() for q in self.questions]
        }

class Classroom:
    def __init__(self, id: str, name: str, code: str, teacher_id: str):
        self.id = id
        self.name = name
        self.code = code
        self.teacher_id = teacher_id
        self.topics: List[Topic] = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "teacher_id": self.teacher_id,
            "topics": [t.to_dict() for t in self.topics]
        }

class DashboardEntry:
    def __init__(self, student_id: str, class_id: str, total_score: float = 0.0, highest_score: float = 0.0):
        self.student_id = student_id
        self.class_id = class_id
        self.total_score = total_score
        self.highest_score = highest_score

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "class_id": self.class_id,
            "total_score": self.total_score,
            "highest_score": self.highest_score
        }