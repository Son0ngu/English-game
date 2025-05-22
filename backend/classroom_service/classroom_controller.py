from flask import jsonify
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

    def check_health(self):
        return jsonify(self.service.check_internal()), 200