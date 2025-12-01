from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=False)

    # One-to-many relationship with Lesson
    lessons = relationship('Lesson', back_populates='course')


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))

    # One-to-many relationship with Topic
    topics = relationship('Topic', back_populates='lesson')
    course = relationship('Course', back_populates='lessons')


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    content = Column(Text)
    topic_type = Column(String(20))  # e.g., 'normal', 'mid_boss', 'final_boss'

    lesson = relationship('Lesson', back_populates='topics')
