from flask import Blueprint, request, jsonify
from injector import inject
from ..services.course_service import CourseService

course_bp = Blueprint('course', __name__, url_prefix='/api/course')

@course_bp.route('', methods=['POST'])
@inject
def create_course(service: CourseService):
    data = request.json
    if not data or 'name' not in data or 'creator_id' not in data:
        return jsonify({"error": "Missing name or creator_id"}), 400
    course = service.create_course(data)
    return jsonify({"success": True, "course": course.to_dict()}), 201


@course_bp.route('', methods=['GET'])
@inject
def get_courses(service: CourseService):
    courses = service.get_all_courses()
    return jsonify({"courses": courses}), 200


@course_bp.route('/<int:course_id>/lesson', methods=['POST'])
@inject
def create_lesson(service: CourseService, course_id: int):
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Missing lesson title"}), 400
    data['course_id'] = course_id
    lesson = service.create_lesson(data)
    return jsonify({"success": True, "lesson": lesson.to_dict()}), 201


@course_bp.route('/<int:course_id>/lesson', methods=['GET'])
@inject
def get_lessons(service: CourseService, course_id: int):
    lessons = service.get_lessons_by_course(course_id)
    return jsonify({"lessons": lessons}), 200


@course_bp.route('/lesson/<int:lesson_id>/topic', methods=['POST'])
@inject
def create_topic(service: CourseService, lesson_id: int):
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Missing topic title"}), 400
    data['lesson_id'] = lesson_id
    topic = service.create_topic(data)
    return jsonify({"success": True, "topic": topic.to_dict()}), 201


@course_bp.route('/lesson/<int:lesson_id>/topic', methods=['GET'])
@inject
def get_topics(service: CourseService, lesson_id: int):
    topics = service.get_topics_by_lesson(lesson_id)
    return jsonify({"topics": topics}), 200
