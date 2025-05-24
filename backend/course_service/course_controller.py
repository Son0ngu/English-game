from flask import jsonify, request
from course_service import CourseService
from course_service.course_model import TOPIC_TYPES

class CourseController:
    def __init__(self, service: CourseService):
        self.service = service

    def get_course(self):
        return jsonify({"course": self.service.get_course()}), 200

    def create_lesson(self, data):
        if not data or 'title' not in data:
            return jsonify({"error": "Missing lesson title"}), 400
        lesson = self.service.add_lesson(data['title'])
        return jsonify({"success": True, "lesson": lesson.to_dict()}), 201

    def get_lessons(self):
        return jsonify({"lessons": self.service.get_lessons()}), 200

    def create_topic(self, lesson_id, data):
        if not data or 'title' not in data:
            return jsonify({"error": "Missing topic title"}), 400

        topic_type = data.get('topic_type', 'normal')
        if topic_type not in TOPIC_TYPES:
            return jsonify({"error": f"Invalid topic_type: {topic_type}"}), 400

        content = data.get('content', '')
        try:
            topic = self.service.add_topic(lesson_id, data['title'], content, topic_type)
            return jsonify({"success": True, "topic": topic.to_dict()}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def get_topics(self, lesson_id):
        return jsonify({"topics": self.service.get_topics(lesson_id)}), 200

    def create_question(self, lesson_id, topic_id, data):
        required_fields = ['text', 'choices', 'correct_index']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing question fields"}), 400

        try:
            text = data['text']
            choices = data['choices']
            correct_index = data['correct_index']
            q_type = data.get('type', 'unknown')
            difficulty = data.get('difficulty', 'medium')

            question = self.service.add_question(
                lesson_id, topic_id,
                text=text,
                choices=choices,
                correct_index=correct_index,
                q_type=q_type  # mới thêm
            )
            question.difficulty = difficulty  # nếu bạn muốn lưu độ khó trong course
            return jsonify({"success": True, "question": question.to_dict()}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def get_questions(self, lesson_id, topic_id):
        return jsonify({"questions": self.service.get_questions(lesson_id, topic_id)}), 200

    def check_health(self):
        return jsonify(self.service.check_health()), 200
