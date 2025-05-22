from typing import List, Optional
import uuid

class Course:
    def __init__(self, name: str, creator_id: str):
        self.id = str(uuid.uuid4())[:8]
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
    def __init__(self, title: str, content: str = '', topic_type: str = 'normal'):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.topic_type = topic_type  # normal, mid_boss, final_boss

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "topic_type": self.topic_type
        }
