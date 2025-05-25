from classroom_service.classroom_model import Classroom, DashboardEntry
from userProfile_service.user.user_service import UserProfileService
from game_service.gameroom.gameroom_service import game_service
import uuid

class ClassroomService:
    def __init__(self, user_service: UserProfileService):
        self.classrooms = {}  # class_id -> Classroom
        self.student_class_links = {}  # class_id -> list of student_ids
        self.dashboard_data = []  # List of DashboardEntry
        self.user_service = user_service
        self.game = game_service()

    def create_class(self, name: str, teacher_id: str):
        class_id = str(uuid.uuid4())[:8]
        code = str(uuid.uuid4())[:6].upper()
        classroom = Classroom(id=class_id, name=name, code=code, teacher_id=teacher_id)
        self.classrooms[class_id] = classroom
        return classroom

    def get_class_by_code(self, code: str):
        for classroom in self.classrooms.values():
            if classroom.code == code:
                return classroom
        return None

    def join_class_by_code(self, student_id: str, class_code: str) -> bool:
        classroom = self.get_class_by_code(class_code)
        if not classroom:
            return False
        if classroom.id not in self.student_class_links:
            self.student_class_links[classroom.id] = []
        if student_id not in self.student_class_links[classroom.id]:
            self.student_class_links[classroom.id].append(student_id)
        return True

    def get_class_students(self, class_id: str):
        student_ids = self.student_class_links.get(class_id, [])
        return [self.user_service.get_user(sid) for sid in student_ids if self.user_service.get_user(sid)]

    def update_dashboard(self, entry: DashboardEntry):
        for i, existing in enumerate(self.dashboard_data):
            if existing.student_id == entry.student_id and existing.class_id == entry.class_id:
                self.dashboard_data[i] = entry
                return
        self.dashboard_data.append(entry)

    def get_dashboard_for_class(self, class_id: str):
        entries = [e for e in self.dashboard_data if e.class_id == class_id]
        return sorted(entries, key=lambda x: x.total_score, reverse=True)

    def get_class_dashboard(self, class_id: str):
        student_ids = self.student_class_links.get(class_id, [])
        for sid in student_ids:
            score_data = self.game.get_results(sid)
            if score_data:
                entry = DashboardEntry(
                    student_id=sid,
                    class_id=class_id,
                    total_score=score_data.total_score,
                    highest_score=score_data.highest_score
                )
                self.update_dashboard(entry)
        return [e.to_dict() for e in self.get_dashboard_for_class(class_id)]

    def get_student_classes(self, student_id: str):
        result = []
        for class_id, student_ids in self.student_class_links.items():
            if student_id in student_ids:
                classroom = self.classrooms.get(class_id)
                if classroom:
                    result.append(classroom.to_dict())
        return result

    def check_internal(self):
        return {"status": "healthy", "details": "Classroom service running"}
