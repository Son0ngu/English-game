from flask import jsonify
from course_service.course_service import CourseService

class CourseController:
    def __init__(self, service: CourseService):
        self.service = service

    def create_course(self, data):
        if not data or 'name' not in data or 'creator_id' not in data:
            return jsonify({"error": "Missing name or creator_id"}), 400
        course = self.service.create_course(data['name'], data['creator_id'])
        return jsonify({"success": True, "course": course.to_dict()}), 201

    def get_courses(self):
        return jsonify({"courses": self.service.get_all_courses()}), 200

    def create_lesson(self, course_id, data):
        if not data or 'title' not in data:
            return jsonify({"error": "Missing lesson title"}), 400
        try:
            lesson = self.service.add_lesson_to_course(course_id, data['title'])
            return jsonify({"success": True, "lesson": lesson.to_dict()}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def get_lessons(self, course_id):
        return jsonify({"lessons": self.service.get_lessons(course_id)}), 200

    def create_topic(self, course_id, lesson_id, data):
        if not data or 'title' not in data:
            return jsonify({"error": "Missing topic title"}), 400
        topic_type = data.get('topic_type', 'normal')
        content = data.get('content', '')
        try:
            topic = self.service.add_topic_to_lesson(lesson_id, course_id, data['title'], content, topic_type)
            return jsonify({"success": True, "topic": topic.to_dict()}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def get_topics(self, course_id, lesson_id):
        return jsonify({"topics": self.service.get_topics(course_id, lesson_id)}), 200

    def check_health(self):
        return jsonify(self.service.check_internal()), 200
