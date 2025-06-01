import uuid
import json
from typing import List, Dict, Any, Optional

from classroom_service.classroom_model import Classroom, Classroom as ClassroomObj, Question
from classroom_service.classroom_db import get_db_connection
from user_profile_service.user.user_service import UserProfileService as UserService

class ClassroomService:
    def __init__(self):
        self.user_service = UserService()

    def create_class(self, name: str, teacher_id: str) -> ClassroomObj:
        class_id = str(uuid.uuid4())[:8]
        code     = str(uuid.uuid4())[:6].upper()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO classes (id, name, code, teacher_id) VALUES (?, ?, ?, ?);",
            (class_id, name, code, teacher_id)
        )
        conn.commit()
        conn.close()
        return ClassroomObj(id=class_id, name=name, code=code, teacher_id=teacher_id)

    def get_class_by_code(self, code: str) -> Optional[ClassroomObj]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes WHERE code = ?;", (code,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return Classroom.from_row(row)

    def join_class_by_code(self, student_id: str, class_code: str) -> bool:
        cls = self.get_class_by_code(class_code)
        if not cls:
            return False

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO student_class (class_id, student_id)
                VALUES (?, ?);
            """, (cls.id, student_id))
            conn.commit()
        except:
            conn.close()
            return False
        conn.close()
        return True

    def get_class_students(self, class_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT student_id FROM student_class WHERE class_id = ?;", (class_id,))
        rows = cursor.fetchall()
        conn.close()

        result = []
        for r in rows:
            sid = r["student_id"]
            user = self.user_service.get_user(sid)
            if user:
                result.append(user)
        return result

    def get_classes_by_teacher(self, teacher_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes WHERE teacher_id = ?;", (teacher_id,))
        rows = cursor.fetchall()
        conn.close()

        return [Classroom.from_row(r).to_dict() for r in rows]

    def create_question(
        self,
        class_id: str,
        text: str,
        q_type: str,
        difficulty: str,
        choices: List[str],
        correct_index: int
    ) -> Question:
        question_id = str(uuid.uuid4())[:8]
        choices_json = json.dumps(choices, ensure_ascii=False)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions
            (id, class_id, question, q_type, difficulty, choices, correct_index)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (question_id, class_id, text, q_type, difficulty, choices_json, correct_index))
        conn.commit()
        conn.close()

        return Question(
            id=question_id,
            text=text,
            difficulty=difficulty,
            choices=choices,
            correct_index=correct_index,
            q_type=q_type,
            class_id=class_id
        )

    def get_questions_by_criteria(
        self,
        class_id: str,
        difficulty: Optional[str],
        q_type: Optional[str],
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        base_sql = "SELECT * FROM questions WHERE class_id = ?"
        params = [class_id]

        if difficulty:
            base_sql += " AND difficulty = ?"
            params.append(difficulty)
        if q_type:
            base_sql += " AND q_type = ?"
            params.append(q_type)

        if limit:
            base_sql += f" ORDER BY RANDOM() LIMIT {limit}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(base_sql + ";", tuple(params))
        rows = cursor.fetchall()
        conn.close()

        return [Question.from_row(r).to_dict() for r in rows]

    def get_student_classes(self, student_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT class_id FROM student_class WHERE student_id = ?;", (student_id,))
        rows = cursor.fetchall()

        result = []
        for r in rows:
            cid = r["class_id"]
            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM classes WHERE id = ?;", (cid,))
            row_cls = cursor2.fetchone()
            if row_cls:
                result.append(Classroom.from_row(row_cls).to_dict())
            cursor2.close()

        conn.close()
        return result

    def get_class_dashboard(self, class_id: str) -> List[Dict[str, Any]]:
        try:
            from game_service.gameroom.gameroom_service import game_service
            game = game_service()
            entries = game.get_dashboard_for_class(class_id)
            return [e.to_dict() for e in entries]
        except Exception:
            return []

    def remove_student_from_class(self, class_id: str, student_id: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM student_class WHERE class_id = ? AND student_id = ?;",
                (class_id, student_id)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def check_internal(self) -> Dict[str, Any]:
        return {"status": "healthy", "details": "Classroom service running"}
