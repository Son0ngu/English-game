from flask import jsonify, request
from classroom_service.classroom_service import ClassroomService

class ClassroomController:
    def __init__(self, service: ClassroomService):
        self.service = service

    def create_class(self, data):
        if not data or 'name' not in data or 'teacher_id' not in data:
            return jsonify({"error": "Missing name or teacher_id"}), 400
        classroom = self.service.create_class(data['name'], data['teacher_id'])
        return jsonify({"success": True, "classroom": classroom.to_dict()}), 201

    def join_class(self, data):
        if not data or 'student_id' not in data or 'class_code' not in data:
            return jsonify({"error": "Missing student_id or class_code"}), 400
        success = self.service.join_class_by_code(data['student_id'], data['class_code'])
        if success:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Invalid class code"}), 404

    def get_students(self, class_id):
        students = self.service.get_class_students(class_id)
        return jsonify({"students": students}), 200

    def get_dashboard(self, class_id):
        dashboard = self.service.get_class_dashboard(class_id)
        return jsonify({"dashboard": dashboard}), 200

    def get_student_classes(self, student_id):
        classes = self.service.get_student_classes(student_id)
        return jsonify({"classes": classes, "student_id": student_id}), 200

    def add_topic(self, class_id, data):
        if not data or 'title' not in data:
            return jsonify({"error": "Missing topic title"}), 400
        topic = self.service.add_topic(class_id, data['title'], data.get('content', ''))
        return jsonify({"success": True, "topic": topic.to_dict()}), 201

    def add_question(self, class_id, topic_id, data):
        required = ['text', 'choices', 'correct_index', 'type', 'difficulty']
        if not data or not all(k in data for k in required):
            return jsonify({"error": "Missing question fields"}), 400
        try:
            q = self.service.add_question(
                class_id=class_id,
                topic_id=topic_id,
                text=data['text'],
                choices=data['choices'],
                correct_index=data['correct_index'],
                q_type=data['type'],
                difficulty=data['difficulty']
            )
            return jsonify({"success": True, "question": q.to_dict()}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def get_questions_by_criteria(self, class_id):
        difficulty = request.args.get("difficulty")
        q_type = request.args.get("type")
        result = self.service.get_questions_by_criteria(class_id, difficulty, q_type)
        return jsonify({"questions": result}), 200

    def check_health(self):
        return jsonify(self.service.check_internal()), 200