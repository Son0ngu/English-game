from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.course import Course, Lesson, Topic

class CourseRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_course(self, course: Course) -> Course:
        self.session.add(course)
        self.session.commit()
        return course

    def get_course(self, course_id: int) -> Optional[Course]:
        return self.session.query(Course).filter_by(id=course_id).first()

    def get_all_courses(self) -> List[Course]:
        return self.session.query(Course).all()

    def delete_course(self, course_id: int):
        course = self.get_course(course_id)
        if course:
            self.session.delete(course)
            self.session.commit()


class LessonRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_lesson(self, lesson: Lesson) -> Lesson:
        self.session.add(lesson)
        self.session.commit()
        return lesson

    def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        return self.session.query(Lesson).filter_by(id=lesson_id).first()

    def get_lessons_by_course(self, course_id: int) -> List[Lesson]:
        return self.session.query(Lesson).filter_by(course_id=course_id).all()

    def delete_lesson(self, lesson_id: int):
        lesson = self.get_lesson(lesson_id)
        if lesson:
            self.session.delete(lesson)
            self.session.commit()


class TopicRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_topic(self, topic: Topic) -> Topic:
        self.session.add(topic)
        self.session.commit()
        return topic

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        return self.session.query(Topic).filter_by(id=topic_id).first()

    def get_topics_by_lesson(self, lesson_id: int) -> List[Topic]:
        return self.session.query(Topic).filter_by(lesson_id=lesson_id).all()

    def delete_topic(self, topic_id: int):
        topic = self.get_topic(topic_id)
        if topic:
            self.session.delete(topic)
            self.session.commit()
