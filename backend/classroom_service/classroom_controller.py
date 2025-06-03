import traceback

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from classroom_service.classroom_db import get_db_connection
from classroom_service.classroom_service import ClassroomService

DIFFICULTY_MAP = {
    1: "easy",
    2: "medium",
    3: "hard",
    4: "expert"
}

QUESTION_TYPE_MAP = {
    1: "multiple",
    2: "true_false",
    3: "fill_blank",
    4: "single"
}

class ClassroomController:
    def __init__(self, service: ClassroomService):
        self.service = service

    @jwt_required()
    def create_class(self, data):
        if not data or 'name' not in data:
            return jsonify({"error": "Missing class name"}), 400

        teacher_id = get_jwt_identity()
        new_cls_obj = self.service.create_class(data['name'], teacher_id)
        return jsonify({"success": True, "classroom": new_cls_obj.to_dict()}), 201

    @jwt_required()
    def join_class(self, data):
        if not data or 'class_code' not in data:
            return jsonify({"error": "Missing class_code"}), 400

        student_id = get_jwt_identity()
        success = self.service.join_class_by_code(student_id, data['class_code'])
        if not success:
            return jsonify({"error": "Invalid class code"}), 404
        return jsonify({"success": True}), 200

    @jwt_required()
    def get_students(self, class_id):
        print("class_id: ", class_id)
        if not class_id:
            return jsonify({"error": "class_id required"}), 400

        try:
            print("class_id for db: ", class_id)
            student_list = self.service.get_class_students(class_id)
            print("DEBUG get_class_students returned:", student_list)
            return jsonify({"students": student_list}), 200
        except Exception as e:
            print("ERROR in get_students:", e)
            traceback.print_exc()
            return jsonify({"error": f"Internal error: {str(e)}"}), 500

    @jwt_required()
    def get_teachers_classes(self):
        teacher_id = get_jwt_identity()
        classes = self.service.get_classes_by_teacher(teacher_id)
        print(classes)
        return jsonify(classes), 200

    @jwt_required()
    def create_question(self):
        data = request.get_json()
        required_fields = ["class_id", "text", "q_type", "difficulty", "choices", "correct_index"]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            question = self.service.create_question(
                class_id=data["class_id"],
                text=data["text"],
                q_type=data["q_type"],
                difficulty=data["difficulty"],
                choices=data["choices"],
                correct_index=int(data["correct_index"])
            )
            return jsonify({"success": True, "question": question.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": f"Failed to create question: {str(e)}"}), 500

    @jwt_required()
    def get_questions_by_criteria(self):
        class_id = request.args.get("class_id")
        if not class_id:
            return jsonify({"error": "class_id required"}), 400

        diff_code = request.args.get("difficulty")
        type_code = request.args.get("type")
        limit    = request.args.get("limit")
        try:
            difficulty = DIFFICULTY_MAP.get(int(diff_code)) if diff_code else None
            q_type     = QUESTION_TYPE_MAP.get(int(type_code)) if type_code else None
            num        = int(limit) if limit else None
        except:
            return jsonify({"error": "Invalid difficulty/type/limit"}), 400

        questions = self.service.get_questions_by_criteria(class_id, difficulty, q_type, num)
        return jsonify({"questions": questions}), 200

    @jwt_required()
    def get_student_classes(self):
        student_id = get_jwt_identity()
        classes = self.service.get_student_classes(student_id)
        return jsonify({"classes": classes}), 200

    @jwt_required()
    def get_dashboard(self, class_id):
        print("Dashboard", class_id)
        if not class_id:
            return jsonify({"error": "class_id required"}), 400

        dashboard = self.service.get_class_dashboard(class_id)
        return jsonify({"dashboard": dashboard}), 200

    @jwt_required()
    def kick_student(self, data):
        if not data or "class_id" not in data or "student_id" not in data:
            return jsonify({"error": "class_id và student_id cần thiết"}), 400

        class_id = data["class_id"]
        student_id = data["student_id"]
        teacher_id = get_jwt_identity()

        cls = self.service.get_class_by_code(class_id)
        from classroom_service.classroom_model import Classroom
        conn = self.service.get_class_by_code(class_id)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id FROM classes WHERE id = ?;", (class_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return jsonify({"error": "Class không tồn tại"}), 404

        if row["teacher_id"] != teacher_id:
            return jsonify({"error": "Chỉ teacher tạo lớp mới có quyền"}), 403

        success = self.service.remove_student_from_class(class_id, student_id)
        if not success:
            return jsonify({"error": "Không thể xóa học sinh hoặc lỗi hệ thống"}), 500

        return jsonify({"success": True}), 200

    @jwt_required()
    def check_health(self):
        return jsonify(self.service.check_internal()), 200
