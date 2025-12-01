import random
import string
from typing import Dict, List
from ..models.classroom import Classroom, DashboardData
from ..models.user import StudentProfile
from ..data.classroom_repository import (
    ClassroomRepository,
    StudentClassLinkRepository,
    DashboardRepository
)
from ..services.user_service import UserProfileService
from ..game_service.gameroom.gameroom_service import game_service  # Dashboard

class ClassroomService:
    def __init__(self,
                 class_repo: ClassroomRepository,
                 link_repo: StudentClassLinkRepository,
                 dashboard_repo: DashboardRepository,
                 user_service: UserProfileService):
        self.class_repo = class_repo
        self.link_repo = link_repo
        self.dashboard_repo = dashboard_repo
        self.user_service = user_service

    def _generate_class_code(self, length: int = 6) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_class(self, data: Dict) -> str:
        code = self._generate_class_code()
        classroom = Classroom(
            name=data['name'],
            teacher_id=data['teacher_id'],
            code=code
        )
        self.class_repo.create_classroom(classroom)
        return code

    def join_class(self, student_id: int, code: str) -> bool:
        classroom = self.class_repo.get_class_by_code(code)
        if not classroom:
            return False
        if self.link_repo.is_student_in_class(student_id, classroom.id):
            return True  # đã tham gia
        self.link_repo.add_student_to_class(student_id, classroom.id)
        return True

    def get_class_students(self, class_id: int) -> List[StudentProfile]:
        student_ids = self.link_repo.get_students_in_class(class_id)
        return [self.user_service.get_user(sid) for sid in student_ids if sid is not None]

    def get_student_dashboard(self, class_id: int) -> List[DashboardData]:
        return self.dashboard_repo.get_dashboard_for_class(class_id)

    def update_class_dashboard(self, class_id: int):
        student_ids = self.link_repo.get_students_in_class(class_id)
        for sid in student_ids:
            result = game_service().get_results(sid)  # giả định API trả về dict
            data = DashboardData(
                student_id=sid,
                class_id=class_id,
                total_score=result.get('total_score', 0.0),
                highest_score=result.get('highest_score', 0.0)
            )
            self.dashboard_repo.update_dashboard(data)

    def check_internal(self):
        return {
            "status": "healthy",
            "details": "Classroom service running normally"
        }
