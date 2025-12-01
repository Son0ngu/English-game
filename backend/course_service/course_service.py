from typing import List, Dict
from course_service.course_model import Course, Lesson, Topic

class CourseService:
    def __init__(self):
        self.courses: Dict[str, Course] = {}  # course_id -> Course

    def create_course(self, name: str, creator_id: str) -> Course:
        course = Course(name=name, creator_id=creator_id)
        self.courses[course.id] = course
        return course

    def get_all_courses(self) -> List[Dict]:
        return [c.to_dict() for c in self.courses.values()]

    def get_course_by_id(self, course_id: str) -> Course:
        return self.courses.get(course_id)

    def add_lesson_to_course(self, course_id: str, title: str) -> Lesson:
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        lesson = Lesson(title=title)
        course.lessons.append(lesson)
        return lesson

    def get_lessons(self, course_id: str) -> List[Dict]:
        course = self.get_course_by_id(course_id)
        return [l.to_dict() for l in course.lessons] if course else []

    def add_topic_to_lesson(self, lesson_id: str, course_id: str, title: str, content: str, topic_type: str = 'normal') -> Topic:
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        for lesson in course.lessons:
            if lesson.id == lesson_id:
                topic = Topic(title=title, content=content, topic_type=topic_type)
                lesson.topics.append(topic)
                return topic
        raise ValueError("Lesson not found")

    def get_topics(self, course_id: str, lesson_id: str) -> List[Dict]:
        course = self.get_course_by_id(course_id)
        if not course:
            return []
        for lesson in course.lessons:
            if lesson.id == lesson_id:
                return [t.to_dict() for t in lesson.topics]
        return []

    def check_internal(self):
        return {"status": "healthy", "details": "Course service running"}