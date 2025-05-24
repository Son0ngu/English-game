from typing import List, Dict
from course_model import Course, Lesson, Topic, Question

class CourseService:
    def __init__(self):
        self.course = Course()

    def get_course(self) -> Dict:
        return self.course.to_dict()

    def add_lesson(self, title: str) -> Lesson:
        lesson = Lesson(title=title)
        self.course.lessons.append(lesson)
        return lesson

    def get_lessons(self) -> List[Dict]:
        return [lesson.to_dict() for lesson in self.course.lessons]

    def add_topic(self, lesson_id: str, title: str, content: str = '', topic_type: str = 'normal') -> Topic:
        lesson = self._find_lesson(lesson_id)
        if not lesson:
            raise ValueError("Lesson not found")
        topic = Topic(title=title, content=content, topic_type=topic_type)
        lesson.topics.append(topic)
        return topic

    def get_topics(self, lesson_id: str) -> List[Dict]:
        lesson = self._find_lesson(lesson_id)
        if not lesson:
            return []
        return [topic.to_dict() for topic in lesson.topics]

    def add_question(self, lesson_id: str, topic_id: str, text: str, choices: List[str], correct_index: int,
                     q_type: str = "unknown") -> Question:
        topic = self._find_topic(lesson_id, topic_id)
        if not topic:
            raise ValueError("Topic not found")
        question = Question(text=text, difficulty="medium", choices=choices, correct_index=correct_index, q_type=q_type)
        topic.questions.append(question)
        return question

    def get_questions(self, lesson_id: str, topic_id: str) -> List[Dict]:
        topic = self._find_topic(lesson_id, topic_id)
        if not topic:
            return []
        return [question.to_dict() for question in topic.questions]

    def check_health(self):
        return {"status": "healthy", "details": "Game-based course service is running"}

    #Test
    def _find_lesson(self, lesson_id: str) -> Lesson:
        for lesson in self.course.lessons:
            if lesson.id == lesson_id:
                return lesson
        return None

    def _find_topic(self, lesson_id: str, topic_id: str) -> Topic:
        lesson = self._find_lesson(lesson_id)
        if not lesson:
            return None
        for topic in lesson.topics:
            if topic.id == topic_id:
                return topic
        return None
