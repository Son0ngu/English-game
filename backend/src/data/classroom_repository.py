from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.classroom import Classroom, StudentClassLink, DashboardData

class ClassroomRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_classroom(self, classroom: Classroom) -> Classroom:
        self.session.add(classroom)
        self.session.commit()
        return classroom

    def get_class_by_code(self, code: str) -> Optional[Classroom]:
        return self.session.query(Classroom).filter_by(code=code).first()

    def get_class_by_id(self, class_id: int) -> Optional[Classroom]:
        return self.session.query(Classroom).filter_by(id=class_id).first()


class StudentClassLinkRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_student_to_class(self, student_id: int, class_id: int):
        link = StudentClassLink(student_id=student_id, class_id=class_id)
        self.session.add(link)
        self.session.commit()

    def is_student_in_class(self, student_id: int, class_id: int) -> bool:
        link = self.session.query(StudentClassLink).filter_by(
            student_id=student_id, class_id=class_id
        ).first()
        return link is not None

    def get_students_in_class(self, class_id: int) -> List[int]:
        links = self.session.query(StudentClassLink).filter_by(class_id=class_id).all()
        return [link.student_id for link in links]


class DashboardRepository:
    def __init__(self, session: Session):
        self.session = session

    def update_dashboard(self, data: DashboardData):
        existing = self.session.query(DashboardData).filter_by(
            student_id=data.student_id, class_id=data.class_id
        ).first()
        if existing:
            existing.total_score = data.total_score
            existing.highest_score = data.highest_score
        else:
            self.session.add(data)
        self.session.commit()

    def get_dashboard_for_class(self, class_id: int) -> List[DashboardData]:
        return self.session.query(DashboardData).filter_by(class_id=class_id).order_by(
            DashboardData.total_score.desc()
        ).all()
