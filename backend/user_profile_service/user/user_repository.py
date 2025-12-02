from typing import List, Optional, Dict, Any
from user_profile_service.user.user import UserProfile, StudentProfile, TeacherProfile
from user_profile_service.database_interface import UserProfileDatabaseInterface  # Import từ thư mục cha

class UserRepository:
    def __init__(self):
        """Khởi tạo repository với database interface"""
        self.db = UserProfileDatabaseInterface()
    
    def _dict_to_user(self, user_dict: Dict[str, Any]) -> Optional[UserProfile]:
        """Convert dictionary to User object"""
        if not user_dict:
            return None
        
        role = user_dict.get('role', 'student')
        
        if role == 'student':
            user = StudentProfile(
                id=user_dict.get('id'),
                email=user_dict.get('email'),
                role=role,
                created_at=user_dict.get('created_at'),
                last_login=user_dict.get('last_login')
            )
            user.language_level = user_dict.get('language_level', 1)
            user.points = user_dict.get('points', 0)
            user.money = user_dict.get('money', 100)
            user.hp = user_dict.get('hp', 100)
            user.atk = user_dict.get('atk', 10)
            
            #  THÊM: Map progression fields
            user.current_map = user_dict.get('current_map', 1)
            user.max_map_unlocked = user_dict.get('max_map_unlocked', 1)
            user._maps_completed = user_dict.get('maps_completed', '[]')
            
            # SỬA: Items handling với defensive programming
            items_data = user_dict.get('items', '[]')
            try:
                if isinstance(items_data, str):
                    user._items = items_data
                elif isinstance(items_data, list):
                    user._items = json.dumps(items_data)
                else:
                    user._items = '[]'
            except Exception as e:
                print(f"Warning: Could not process items for user {user_dict.get('id')}: {e}")
                user._items = '[]'
            
            return user
        
        elif role == 'teacher':
            user = TeacherProfile(
                id=user_dict.get('id'),
                email=user_dict.get('email'),
                role=role,
                created_at=user_dict.get('created_at'),
                last_login=user_dict.get('last_login')
            )
            # SỬA: Subjects handling với defensive programming
            subjects_data = user_dict.get('subjects', [])
            try:
                user.set_subjects(subjects_data)
            except Exception as e:
                print(f"Warning: Could not process subjects for teacher {user_dict.get('id')}: {e}")
                user._subjects = '[]'
        
            return user
        
        else:
            # Generic user profile
            user = UserProfile(
                id=user_dict.get('id'),
                email=user_dict.get('email'),
                role=role,
                created_at=user_dict.get('created_at'),
                last_login=user_dict.get('last_login')
            )
        
        return user
    
    def save(self, user: UserProfile) -> UserProfile:
        """
        Lưu người dùng vào database
        
        Args:
            user: Đối tượng UserProfile cần lưu
            
        Returns:
            Đối tượng UserProfile đã lưu
        """
        # Chuyển đổi đối tượng thành dictionary
        user_dict = user.to_dict()
        
        # Lưu vào database và lấy ID
        user_id = self.db.save_user(user_dict)
        
        # Cập nhật ID nếu là người dùng mới
        if not user.id:
            user.id = user_id
            
        return user
    
    def find_by_id(self, user_id: str) -> Optional[UserProfile]:
        """
        Tìm người dùng theo ID
        
        Args:
            user_id: ID của người dùng
            
        Returns:
            Đối tượng UserProfile hoặc None nếu không tìm thấy
        """
        print("find_by_id", user_id)
        user_dict = self.db.get_user_by_id(user_id)
        print("user_dict", user_dict)
        return self._dict_to_user(user_dict)

    def find_by_id_gameplay(self, user_id: str) -> Optional[UserProfile]:
        """
        Tìm người dùng theo ID

        Args:
            user_id: ID của người dùng

        Returns:
            Đối tượng UserProfile hoặc None nếu không tìm thấy
        """
        print("find_by_id", user_id)
        user_dict = self.db.get_user_by_id_gameplay(user_id)
        print("user_dict", user_dict)
        return self._dict_to_user(user_dict)
    
    def find_students(self, limit: int = 100, offset: int = 0) -> List[StudentProfile]:
        """
        Tìm tất cả học sinh với phân trang
        
        Args:
            limit: Số lượng kết quả tối đa
            offset: Vị trí bắt đầu
            
        Returns:
            Danh sách các đối tượng StudentProfile
        """
        students_dict = self.db.get_students(limit, offset)
        return [self._dict_to_user(s) for s in students_dict if s.get('role') == 'student']
    
    def find_teachers(self, limit: int = 100, offset: int = 0) -> List[TeacherProfile]:
        """
        Tìm tất cả giáo viên với phân trang
        
        Args:
            limit: Số lượng kết quả tối đa
            offset: Vị trí bắt đầu
            
        Returns:
            Danh sách các đối tượng TeacherProfile
        """
        teachers_dict = self.db.get_teachers(limit, offset)
        return [self._dict_to_user(t) for t in teachers_dict if t.get('role') == 'teacher']
    
    def delete_user(self, user_id: int) -> bool:
        """
        Xóa người dùng theo ID
        
        Args:
            user_id: ID của người dùng cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không
        """
        return self.db.delete_user(user_id)
    
    def count_users(self) -> dict:
        """
        Đếm số lượng người dùng theo loại
        
        Returns:
            Dictionary chứa số lượng người dùng theo loại
        """
        return self.db.count_users()

    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            # Thử tạo kết nối
            connection = self.db._get_connection()
            connection.close()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def add_user_id_only(self, user_id, role="student"):
        """Add user với role được chỉ định"""
        return self.db.add_user_id_only(user_id, role)

    def change_user_role(self, user_id: str, new_role: str) -> bool:
        """Thay đổi role của user"""
        return self.db.change_user_role(user_id, new_role)