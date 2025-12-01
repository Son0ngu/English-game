from typing import List
import uuid

class TopicType:
    NORMAL = "normal"
    MID_BOSS = "mid_boss"
    FINAL_BOSS = "final_boss"

TOPIC_TYPES = {TopicType.NORMAL, TopicType.MID_BOSS, TopicType.FINAL_BOSS}

class Course:
    def __init__(self, name: str = "Game-Based Learning Course", creator_id: str = "system"):
        self.id = "default_course"
        self.name = name
        self.creator_id = creator_id
        self.lessons: List['Lesson'] = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "creator_id": self.creator_id,
            "lessons": [l.to_dict() for l in self.lessons]
        }

class Lesson:
    def __init__(self, title: str):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.topics: List['Topic'] = []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "topics": [t.to_dict() for t in self.topics]
        }

class Topic:
    def __init__(self, title: str, content: str = '', topic_type: str = TopicType.NORMAL):
        if topic_type not in TOPIC_TYPES:
            raise ValueError(f"Invalid topic_type: {topic_type}")
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.topic_type = topic_type
        self.questions: List['Question'] = []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "topic_type": self.topic_type,
            "questions": [q.to_dict() for q in self.questions]
        }

class Question:
    def __init__(self, text: str, difficulty: str, choices: List[str], correct_index: int, q_type: str = "unknown"):
        self.id = str(uuid.uuid4())[:8]
        self.question = text
        self.difficulty = difficulty
        self.choices = choices
        self.correct_index = correct_index
        self.answer = choices[correct_index]
        self.type = q_type

    def get_choices(self):
        return self.choices

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "difficulty": self.difficulty,
            "question": self.question,
            "choices": self.get_choices(),
            "answer": self.answer
        }