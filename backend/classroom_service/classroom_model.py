from typing import List

class Classroom:
    def __init__(self, id: str, name: str, code: str, teacher_id: str):
        self.id = id
        self.name = name
        self.code = code
        self.teacher_id = teacher_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "teacher_id": self.teacher_id
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
