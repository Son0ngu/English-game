from flask import Blueprint, request, jsonify
from injector import inject
from ..services.classroom_service import ClassroomService

classroom_bp = Blueprint('classroom', __name__, url_prefix='/api/class')

@classroom_bp.route('', methods=['POST'])
@inject
def create_classroom(service: ClassroomService):
    data = request.json
    if not data or 'name' not in data or 'teacher_id' not in data:
        return jsonify({"error": "Missing name or teacher_id"}), 400

    code = service.create_class(data)
    return jsonify({"success": True, "class_code": code}), 201


@classroom_bp.route('/join', methods=['POST'])
@inject
def join_class(service: ClassroomService):
    data = request.json
    if not data or 'student_id' not in data or 'class_code' not in data:
        return jsonify({"error": "Missing student_id or class_code"}), 400

    success = service.join_class(data['student_id'], data['class_code'])
    if success:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Invalid class code"}), 404


@classroom_bp.route('/<int:class_id>/students', methods=['GET'])
@inject
def get_class_students(service: ClassroomService, class_id: int):
    students = service.get_students_in_class(class_id)
    return jsonify({"students": students}), 200


@classroom_bp.route('/<int:class_id>/dashboard', methods=['GET'])
@inject
def get_dashboard(service: ClassroomService, class_id: int):
    dashboard = service.get_student_dashboard(class_id)
    return jsonify({"dashboard": [d.__dict__ for d in dashboard]}), 200