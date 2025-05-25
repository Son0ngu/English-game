import uuid
import random
from typing import List, Optional
from classroom_model import Classroom, Topic, Question, DashboardEntry
from userProfile_service.user.user_service import UserProfileService as UserProfileService
from game_service.gameroom.gameroom_service import game_service

class ClassroomService:
    def __init__(self):
        self.classrooms = {}
        self.student_class_links = {}
        self.dashboard_data: List[DashboardEntry] = []
        self.user_service = UserProfileService
        self.game = game_service()

    def create_class(self, name: str, teacher_id: str) -> Classroom:
        class_id = str(uuid.uuid4())[:8]
        code = str(uuid.uuid4())[:6].upper()
        classroom = Classroom(id=class_id, name=name, code=code, teacher_id=teacher_id)
        self.classrooms[class_id] = classroom
        return classroom

    def get_class_by_code(self, code: str):
        return next((c for c in self.classrooms.values() if c.code == code), None)

    def join_class_by_code(self, student_id: str, class_code: str) -> bool:
        classroom = self.get_class_by_code(class_code)
        if not classroom:
            return False
        self.student_class_links.setdefault(classroom.id, []).append(student_id)
        return True

    def get_class_students(self, class_id: str):
        student_ids = self.student_class_links.get(class_id, [])
        return [self.user_service.get_user(sid) for sid in student_ids if self.user_service.get_user(sid)]

    def add_topic(self, class_id: str, title: str, content: str = '') -> Topic:
        classroom = self.classrooms.get(class_id)
        if not classroom:
            raise ValueError("Class not found")
        topic = Topic(title=title, content=content)
        classroom.topics.append(topic)
        return topic

    def add_question(self, class_id: str, topic_id: str, text: str, choices: List[str], correct_index: int, q_type: str, difficulty: str) -> Question:
        classroom = self.classrooms.get(class_id)
        if not classroom:
            raise ValueError("Class not found")
        for topic in classroom.topics:
            if topic.id == topic_id:
                question = Question(text, difficulty, choices, correct_index, q_type)
                topic.questions.append(question)
                return question
        raise ValueError("Topic not found")

    def get_questions_by_criteria(self, class_id: str, difficulty: Optional[str], q_type: Optional[str]) -> List[dict]:
        classroom = self.classrooms.get(class_id)
        if not classroom:
            return []
        filtered = [
            q for topic in classroom.topics for q in topic.questions
            if (difficulty is None or q.difficulty == difficulty) and
               (q_type is None or q.type == q_type)
        ]
        return [q.to_dict() for q in filtered]

    def get_class_dashboard(self, class_id: str):
        student_ids = self.student_class_links.get(class_id, [])
        for sid in student_ids:
            score_data = self.game.get_results(sid)
            if score_data:
                entry = DashboardEntry(sid, class_id, score_data.total_score, score_data.highest_score)
                self.update_dashboard(entry)
        return [e.to_dict() for e in self.get_dashboard_for_class(class_id)]

    def update_dashboard(self, entry: DashboardEntry):
        for i, e in enumerate(self.dashboard_data):
            if e.student_id == entry.student_id and e.class_id == entry.class_id:
                self.dashboard_data[i] = entry
                return
        self.dashboard_data.append(entry)

    def get_dashboard_for_class(self, class_id: str):
        return sorted([e for e in self.dashboard_data if e.class_id == class_id], key=lambda x: x.total_score, reverse=True)

    def get_student_classes(self, student_id: str):
        return [c.to_dict() for cid, c in self.classrooms.items() if student_id in self.student_class_links.get(cid, [])]

    def check_internal(self):
        return {"status": "healthy", "details": "Classroom service running"}