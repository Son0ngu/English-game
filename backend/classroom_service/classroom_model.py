import uuid
import json
from typing import List, Optional, Dict, Any

from classroom_service.classroom_db import init_db, get_db_connection

init_db()


class Question:
    def __init__(
        self,
        id: str,
        text: str,
        difficulty: str,
        choices: List[str],
        correct_index: Optional[int],
        correct_answers: Optional[List[str]],
        q_type: str,
        class_id: str
    ):
        self.id = id
        self.question = text
        self.difficulty = difficulty
        self.choices = choices
        self.correct_index = correct_index
        self.correct_answers = correct_answers or []
        self.type = q_type
        self.class_id = class_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "difficulty": self.difficulty,
            "question": self.question,
            "choices": self.choices,
            "answer": (self.choices[self.correct_index]
                       if self.correct_index is not None else None),
            "correct_answers": self.correct_answers,
            "class_id": self.class_id
        }

    @staticmethod
    def from_row(row) -> "Question":
        return Question(
            id=row["id"],
            text=row["question"],
            difficulty=row["difficulty"],
            choices=json.loads(row["choices"]),
            correct_index=row["correct_index"],
            correct_answers=(json.loads(row["correct_answers"])
                             if row["correct_answers"] else []),
            q_type=row["q_type"],
            class_id=row["class_id"]
        )


class Classroom:
    def __init__(self, id: str, name: str, code: str, teacher_id: str):
        self.id = id
        self.name = name
        self.code = code
        self.teacher_id = teacher_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "teacher_id": self.teacher_id
        }

    @staticmethod
    def from_row(row) -> "Classroom":
        return Classroom(
            id=row["id"],
            name=row["name"],
            code=row["code"],
            teacher_id=row["teacher_id"]
        )
