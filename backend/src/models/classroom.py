from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Classroom(Base):
    __tablename__ = 'classroom'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)


class StudentClassLink(Base):
    __tablename__ = 'student_class_link'

    student_id = Column(Integer, ForeignKey('user_profiles.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classroom.id'), primary_key=True)


class DashboardData(Base):
    __tablename__ = 'dashboard_data'

    student_id = Column(Integer, ForeignKey('user_profiles.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classroom.id'), primary_key=True)
    total_score = Column(Float, default=0.0)
    highest_score = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint('student_id', 'class_id', name='_student_class_uc'),
    )
