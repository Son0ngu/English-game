from typing import List, Dict
from ..models.course import Course, Lesson, Topic
from ..data.course_repository import CourseRepository, LessonRepository, TopicRepository

class CourseService:
    def __init__(self,
                 course_repo: CourseRepository,
                 lesson_repo: LessonRepository,
                 topic_repo: TopicRepository):
        self.course_repo = course_repo
        self.lesson_repo = lesson_repo
        self.topic_repo = topic_repo

    def create_course(self, data: Dict) -> Course:
        course = Course(
            name=data['name'],
            description=data.get('description', ''),
            creator_id=data['creator_id']
        )
        return self.course_repo.create_course(course)

    def get_all_courses(self) -> List[Dict]:
        return [c.to_dict() for c in self.course_repo.get_all_courses()]

    def create_lesson(self, data: Dict) -> Lesson:
        lesson = Lesson(
            title=data['title'],
            course_id=data['course_id']
        )
        return self.lesson_repo.create_lesson(lesson)

    def get_lessons_by_course(self, course_id: int) -> List[Dict]:
        return [l.to_dict() for l in self.lesson_repo.get_lessons_by_course(course_id)]

    def create_topic(self, data: Dict) -> Topic:
        topic = Topic(
            title=data['title'],
            lesson_id=data['lesson_id'],
            content=data.get('content', ''),
            topic_type=data.get('topic_type', 'normal')
        )
        return self.topic_repo.create_topic(topic)

    def get_topics_by_lesson(self, lesson_id: int) -> List[Dict]:
        return [t.to_dict() for t in self.topic_repo.get_topics_by_lesson(lesson_id)]

    def check_internal(self) -> dict:
        return {
            "status": "healthy",
            "details": "CourseService is operational"
        }
