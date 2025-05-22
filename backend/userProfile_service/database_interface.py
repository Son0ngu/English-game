import sqlite3
import os
import json
from typing import Dict, List, Any, Optional, Tuple
import uuid
import time

class DatabaseInterface:
    def __init__(self, db_path="userprofile.db"):
        """
        Khởi tạo kết nối với database SQLite
        
        Args:
            db_path: Đường dẫn đến file database
        """
        # Kiểm tra thư mục hiện tại cho đường dẫn tương đối
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        # Kiểm tra các bảng đã tồn tại chưa
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profiles'")
        table_exists = self.cursor.fetchone() is not None
        
        # Nếu chưa, tạo bảng từ file SQL
        if not table_exists:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sql_file_path = os.path.join(script_dir, 'userTable.sql')
            
            with open(sql_file_path, 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()
        
        self.cursor.close()
        self.connection.close()
        print("Database initialized")
    
    def _get_connection(self):
        """Tạo kết nối mới đến database"""
        return sqlite3.connect(self.db_path)


class UserProfileDatabaseInterface(DatabaseInterface):
    """Interface cho các thao tác với user_profiles trong database"""
    
    def save_user(self, user_data: Dict[str, Any]) -> int:
        """
        Lưu thông tin người dùng vào database
        
        Args:
            user_data: Dictionary chứa thông tin người dùng
            
        Returns:
            ID của người dùng đã lưu
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Kiểm tra người dùng đã tồn tại chưa
            user_id = user_data.get('id')
            if user_id:
                cursor.execute("SELECT id FROM user_profiles WHERE id = ?", (user_id,))
                exists = cursor.fetchone() is not None
            else:
                exists = False
            
            if exists:
                # Cập nhật thông tin cơ bản
                cursor.execute("""
                    UPDATE user_profiles 
                    SET email = ?, role = ?, last_login = ? 
                    WHERE id = ?
                """, (
                    user_data.get('email'),
                    user_data.get('role'),
                    user_data.get('last_login'),
                    user_id
                ))
            else:
                # Thêm người dùng mới
                cursor.execute("""
                    INSERT INTO user_profiles (email, role, created_at, last_login)
                    VALUES (?, ?, ?, ?)
                """, (
                    user_data.get('email'),
                    user_data.get('role'),
                    user_data.get('created_at'),
                    user_data.get('last_login')
                ))
                user_id = cursor.lastrowid
            
            # Xác định loại người dùng để lưu chi tiết
            role = user_data.get('role', 'student')
            
            if role == 'student':
                # Kiểm tra profile học sinh đã tồn tại chưa
                cursor.execute("SELECT id FROM student_profiles WHERE id = ?", (user_id,))
                student_exists = cursor.fetchone() is not None
                
                if student_exists:
                    # Cập nhật profile học sinh
                    cursor.execute("""
                        UPDATE student_profiles 
                        SET language_level = ?, points = ?, money = ?, hp = ?, atk = ?, items = ? 
                        WHERE id = ?
                    """, (
                        user_data.get('language_level', 1),
                        user_data.get('points', 0),
                        user_data.get('money', 100),
                        user_data.get('hp', 100),
                        user_data.get('atk', 10),
                        json.dumps(user_data.get('items', [])),
                        user_id
                    ))
                else:
                    # Thêm profile học sinh mới
                    cursor.execute("""
                        INSERT INTO student_profiles (id, language_level, points, money, hp, atk, items)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        user_data.get('language_level', 1),
                        user_data.get('points', 0),
                        user_data.get('money', 100),
                        user_data.get('hp', 100),
                        user_data.get('atk', 10),
                        json.dumps(user_data.get('items', []))
                    ))
            elif role == 'teacher':
                # Kiểm tra profile giáo viên đã tồn tại chưa
                cursor.execute("SELECT id FROM teacher_profiles WHERE id = ?", (user_id,))
                teacher_exists = cursor.fetchone() is not None
                
                if teacher_exists:
                    # Cập nhật profile giáo viên
                    cursor.execute("""
                        UPDATE teacher_profiles 
                        SET subjects = ?
                        WHERE id = ?
                    """, (
                        json.dumps(user_data.get('subjects', [])),
                        user_id
                    ))
                else:
                    # Thêm profile giáo viên mới
                    cursor.execute("""
                        INSERT INTO teacher_profiles (id, subjects)
                        VALUES (?, ?)
                    """, (
                        user_id,
                        json.dumps(user_data.get('subjects', []))
                    ))
            
            connection.commit()
            return user_id
            
        except Exception as e:
            connection.rollback()
            print(f"Error saving user: {str(e)}")
            raise e
        finally:
            cursor.close()
            connection.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin người dùng theo ID
        
        Args:
            user_id: ID của người dùng
            
        Returns:
            Dictionary chứa thông tin người dùng hoặc None
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Lấy thông tin cơ bản
            cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return None
                
            # Chuyển đổi từ tuple sang dictionary
            user_dict = {
                'id': user_data[0],
                'email': user_data[1],
                'role': user_data[2],
                'created_at': user_data[3],
                'last_login': user_data[4]
            }
            
            # Lấy thông tin theo loại người dùng
            role = user_dict['role']
            
            if role == 'student':
                cursor.execute("SELECT * FROM student_profiles WHERE id = ?", (user_id,))
                student_data = cursor.fetchone()
                
                if student_data:
                    user_dict.update({
                        'language_level': student_data[1],
                        'points': student_data[2],
                        'money': student_data[3],
                        'hp': student_data[4],
                        'atk': student_data[5],
                        'items': json.loads(student_data[6] or '[]')
                    })
            elif role == 'teacher':
                cursor.execute("SELECT * FROM teacher_profiles WHERE id = ?", (user_id,))
                teacher_data = cursor.fetchone()
                
                if teacher_data:
                    user_dict.update({
                        'subjects': json.loads(teacher_data[1] or '[]')
                    })
            
            return user_dict
            
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    def get_students(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Lấy danh sách học sinh
        
        Args:
            limit: Số lượng kết quả tối đa
            offset: Vị trí bắt đầu
            
        Returns:
            Danh sách các học sinh dưới dạng dictionary
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Lấy danh sách ID học sinh
            cursor.execute("""
                SELECT up.id
                FROM user_profiles up
                JOIN student_profiles sp ON up.id = sp.id
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            student_ids = [row[0] for row in cursor.fetchall()]
            students = []
            
            # Lấy thông tin chi tiết cho từng học sinh
            for student_id in student_ids:
                student = self.get_user_by_id(student_id)
                if student:
                    students.append(student)
            
            return students
            
        except Exception as e:
            print(f"Error getting students: {str(e)}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    def get_teachers(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Lấy danh sách giáo viên
        
        Args:
            limit: Số lượng kết quả tối đa
            offset: Vị trí bắt đầu
            
        Returns:
            Danh sách các giáo viên dưới dạng dictionary
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Lấy danh sách ID giáo viên
            cursor.execute("""
                SELECT up.id
                FROM user_profiles up
                JOIN teacher_profiles tp ON up.id = tp.id
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            teacher_ids = [row[0] for row in cursor.fetchall()]
            teachers = []
            
            # Lấy thông tin chi tiết cho từng giáo viên
            for teacher_id in teacher_ids:
                teacher = self.get_user_by_id(teacher_id)
                if teacher:
                    teachers.append(teacher)
            
            return teachers
            
        except Exception as e:
            print(f"Error getting teachers: {str(e)}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    def delete_user(self, user_id: int) -> bool:
        """
        Xóa người dùng theo ID
        
        Args:
            user_id: ID của người dùng cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Kiểm tra loại người dùng
            cursor.execute("SELECT role FROM user_profiles WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return False
                
            role = user_data[0]
            
            # Xóa profile theo loại
            if role == 'student':
                cursor.execute("DELETE FROM student_profiles WHERE id = ?", (user_id,))
            elif role == 'teacher':
                cursor.execute("DELETE FROM teacher_profiles WHERE id = ?", (user_id,))
            
            # Xóa thông tin cơ bản
            cursor.execute("DELETE FROM user_profiles WHERE id = ?", (user_id,))
            
            connection.commit()
            return True
            
        except Exception as e:
            connection.rollback()
            print(f"Error deleting user: {str(e)}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    def count_users(self) -> Dict[str, int]:
        """
        Đếm số lượng người dùng theo loại
        
        Returns:
            Dictionary chứa số lượng người dùng theo loại
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Đếm tổng số học sinh
            cursor.execute("SELECT COUNT(*) FROM student_profiles")
            student_count = cursor.fetchone()[0]
            
            # Đếm tổng số giáo viên
            cursor.execute("SELECT COUNT(*) FROM teacher_profiles")
            teacher_count = cursor.fetchone()[0]
            
            # Đếm tổng số người dùng
            cursor.execute("SELECT COUNT(*) FROM user_profiles")
            total_count = cursor.fetchone()[0]
            
            return {
                "students": student_count,
                "teachers": teacher_count,
                "other": total_count - student_count - teacher_count,
                "total": total_count
            }
            
        except Exception as e:
            print(f"Error counting users: {str(e)}")
            return {"students": 0, "teachers": 0, "other": 0, "total": 0}
        finally:
            cursor.close()
            connection.close()


class ItemDatabaseInterface(DatabaseInterface):
    """Interface cho các thao tác với items trong database"""
    
    def save_item(self, item_data: Dict[str, Any]) -> str:
        """
        Lưu thông tin item vào database
        
        Args:
            item_data: Dictionary chứa thông tin item
            
        Returns:
            ID của item đã lưu
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            # Kiểm tra item đã tồn tại chưa
            item_id = item_data.get('id')
            if not item_id:
                item_id = str(uuid.uuid4())[:8]
                item_data['id'] = item_id
                
            cursor.execute("SELECT id FROM items WHERE id = ?", (item_id,))
            exists = cursor.fetchone() is not None
            
            if exists:
                # Cập nhật item
                cursor.execute("""
                    UPDATE items 
                    SET name = ?, description = ?, price = ?, effect = ?, 
                        type = ?, level = ?, max_level = ?, owner_id = ?, is_template = ?
                    WHERE id = ?
                """, (
                    item_data.get('name'),
                    item_data.get('description'),
                    item_data.get('price', 0),
                    item_data.get('effect', 0),
                    item_data.get('type'),
                    item_data.get('level', 1),
                    item_data.get('max_level', 1),
                    item_data.get('owner_id'),
                    1 if item_data.get('is_template', False) else 0,
                    item_id
                ))
            else:
                # Thêm item mới
                created_at = item_data.get('created_at', int(time.time()))
                cursor.execute("""
                    INSERT INTO items (id, name, description, price, effect, type, level, max_level, created_at, owner_id, is_template)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item_id,
                    item_data.get('name'),
                    item_data.get('description'),
                    item_data.get('price', 0),
                    item_data.get('effect', 0),
                    item_data.get('type'),
                    item_data.get('level', 1),
                    item_data.get('max_level', 1),
                    created_at,
                    item_data.get('owner_id'),
                    1 if item_data.get('is_template', False) else 0
                ))
            
            connection.commit()
            return item_id
            
        except Exception as e:
            connection.rollback()
            print(f"Error saving item: {str(e)}")
            raise e
        finally:
            cursor.close()
            connection.close()
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin item theo ID
        
        Args:
            item_id: ID của item
            
        Returns:
            Dictionary chứa thông tin item hoặc None
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
            item_data = cursor.fetchone()
            
            if not item_data:
                return None
                
            # Tạo dictionary cho item
            item_dict = {
                'id': item_data[0],
                'name': item_data[1],
                'description': item_data[2],
                'price': item_data[3],
                'effect': item_data[4],
                'type': item_data[5],
                'level': item_data[6],
                'max_level': item_data[7],
                'created_at': item_data[8],
                'owner_id': item_data[9],
                'is_template': bool(item_data[10]),
                'can_upgrade': item_data[6] < item_data[7]  # level < max_level
            }
            
            return item_dict
            
        except Exception as e:
            print(f"Error getting item: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    def get_templates(self) -> List[Dict[str, Any]]:
        """
        Lấy tất cả các item mẫu (template)
        
        Returns:
            Danh sách các item template
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT * FROM items WHERE is_template = 1")
            items_data = cursor.fetchall()
            
            result = []
            for item_data in items_data:
                item_dict = {
                    'id': item_data[0],
                    'name': item_data[1],
                    'description': item_data[2],
                    'price': item_data[3],
                    'effect': item_data[4],
                    'type': item_data[5],
                    'level': item_data[6],
                    'max_level': item_data[7],
                    'created_at': item_data[8],
                    'owner_id': item_data[9],
                    'is_template': bool(item_data[10]),
                    'can_upgrade': item_data[6] < item_data[7]  # level < max_level
                }
                result.append(item_dict)
            
            return result
            
        except Exception as e:
            print(f"Error getting templates: {str(e)}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    def get_items_by_owner(self, owner_id: str) -> List[Dict[str, Any]]:
        """
        Lấy tất cả các item của một người dùng
        
        Args:
            owner_id: ID của người dùng sở hữu
            
        Returns:
            Danh sách các item thuộc sở hữu của người dùng
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT * FROM items WHERE owner_id = ?", (owner_id,))
            items_data = cursor.fetchall()
            
            result = []
            for item_data in items_data:
                item_dict = {
                    'id': item_data[0],
                    'name': item_data[1],
                    'description': item_data[2],
                    'price': item_data[3],
                    'effect': item_data[4],
                    'type': item_data[5],
                    'level': item_data[6],
                    'max_level': item_data[7],
                    'created_at': item_data[8],
                    'owner_id': item_data[9],
                    'is_template': bool(item_data[10]),
                    'can_upgrade': item_data[6] < item_data[7]  # level < max_level
                }
                result.append(item_dict)
            
            return result
            
        except Exception as e:
            print(f"Error getting owner items: {str(e)}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    def delete_item(self, item_id: str) -> bool:
        """
        Xóa item theo ID
        
        Args:
            item_id: ID của item cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            print(f"Error deleting item: {str(e)}")
            return False
        finally:
            cursor.close()
            connection.close()