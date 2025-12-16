from user_profile_service.user.user import UserProfile, StudentProfile, TeacherProfile
from user_profile_service.user.user_repository import UserRepository
import time
from typing import Dict, List, Optional, Any

class UserProfileService:
    def __init__(self):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"profile_updates": 0, "progress_updates": 0}
        self.user_repository = UserRepository()
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user details by ID"""
        try:
            print(f"Looking for user: {user_id}")
            user = self.user_repository.find_by_id(user_id)
            print(f"Found user: {user}")
            
            if not user:
                print(f"User {user_id} not found")
                return None
            
            if user:
                print(f"Found user: {user.to_dict()}")
                return user.to_dict()
                
            return None
        except Exception as e:
            print(f"💥 Error getting user {user_id}: {e}")
            self._last_error = e
            return None

    def get_user_gameplay(self, user_id: str) -> Optional[dict]:
        """Get user details by ID"""
        try:
            print(f"Looking for user: {user_id}")
            # user = self.user_repository.find_by_id(user_id)
            user = self.user_repository.find_by_id_gameplay(user_id)
            print(f"Found user: {user}")

            if not user:
                print(f"User {user_id} not found")
                return None

            if user:
                print(f"Found user: {user.to_dict()}")
                return user.to_dict()

            return None
        except Exception as e:
            print(f"💥 Error getting user {user_id}: {e}")
            self._last_error = e
            return None
    
    def update_profile(self, user_id: str, updates: dict) -> dict:
        """Update user profile attributes"""
        self._stats["profile_updates"] += 1
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Update basic user properties (exclude money)
            for key, value in updates.items():
                if hasattr(user, key) and key not in ['id', 'role', 'created_at', 'money']:
                    setattr(user, key, value)
            
            # Handle special fields based on user type
            if isinstance(user, StudentProfile):
                if 'items' in updates:
                    user.set_items(updates['items'])
                    
            elif isinstance(user, TeacherProfile):
                if 'subjects' in updates:
                    user.set_subjects(updates['subjects'])
            
            # Save updated user
            self.user_repository.save(user)
            return {"success": True, "updated_fields": list(updates.keys())}
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def update_progress_with_weapon_upgrade(self, user_id: int, lesson_id: str, points: int) -> dict:
        """Update user progress với automatic weapon upgrade"""
        self._stats["progress_updates"] += 1
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Update points và level
            old_points = user.points
            old_level = user.language_level
            old_atk = user.atk
            
            user.points += points
            
            # Level up logic (every 1000 points = 1 level)
            new_level = max(1, user.points // 1000 + 1)
            user.language_level = new_level
            
            # Auto weapon upgrade khi level up
            weapon_upgraded = False
            if new_level > old_level:
                # Mỗi level tăng ATK lên 2 points
                new_atk = 10 + (new_level - 1) * 2  # Base ATK = 10
                user.atk = new_atk
                weapon_upgraded = True
            
            # Save updated user
            self.user_repository.save(user)
            
            result = {
                "success": True, 
                "old_points": old_points,
                "new_points": user.points,
                "points_gained": points,
                "old_level": old_level,
                "new_level": new_level,
                "level_up": new_level > old_level,
                "weapon_upgraded": weapon_upgraded
            }
            
            if weapon_upgraded:
                result["weapon_upgrade"] = {
                    "old_atk": old_atk,
                    "new_atk": user.atk,
                    "atk_gained": user.atk - old_atk
                }
            
            return result
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def get_student_progress(self, user_id: int) -> dict:
        """Get a student's learning progress"""
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Call the student's view_progress method
            progress_data = user.view_progress()
            return {"success": True, **progress_data}
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    # BỎ: update_student_money method hoàn toàn
    
    def update_student_stats(self, user_id: int, hp: int = None, atk: int = None) -> dict:
        """Update student's game stats (HP, ATK) and return detailed info"""
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            updates = {}
            if hp is not None:
                old_hp = user.hp
                user.hp = max(0, hp)  # HP không được âm
                updates['hp'] = {"old": old_hp, "new": user.hp}
                
            if atk is not None:
                old_atk = user.atk
                user.atk = max(1, atk)  # ATK tối thiểu là 1
                updates['atk'] = {"old": old_atk, "new": user.atk}
        
            if not updates:
                return {"success": False, "error": "No stats to update"}
            
            # Save updated user
            self.user_repository.save(user)
            
            # Return detailed stats including items and level
            return {
                "success": True, 
                "updates": updates,
                "current_stats": {
                    "hp": user.hp,
                    "atk": user.atk,
                    "level": user.language_level,
                    "points": user.points,
                    "items": user.get_items() if hasattr(user, 'get_items') else [],
                    "equipped_items": getattr(user, 'equipped_items', []),
                    "username": user.username
                }
            }
        
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def get_all_students(self, limit: int = 100, offset: int = 0) -> list:
        """Get all student profiles"""
        try:
            students = self.user_repository.find_students(limit, offset)
            return [student.to_dict() for student in students]
        except Exception as e:
            self._last_error = e
            return []
    
    def get_all_teachers(self, limit: int = 100, offset: int = 0) -> list:
        """Get all teacher profiles"""
        try:
            teachers = self.user_repository.find_teachers(limit, offset)
            return [teacher.to_dict() for teacher in teachers]
        except Exception as e:
            self._last_error = e
            return []

    def find_by_role(self, role: str, limit: int = 100, offset: int = 0) -> List[UserProfile]:
        """Find users by role - wrapper method"""
        if role == 'student':
            return self.user_repository.find_students(limit, offset)
        elif role == 'teacher':
            return self.user_repository.find_teachers(limit, offset)
        else:
            return []

    def delete_user(self, user_id: int) -> dict:
        """Delete a user"""
        try:
            success = self.user_repository.delete_user(user_id)
            if success:
                return {"success": True, "message": f"User {user_id} deleted successfully"}
            return {"success": False, "error": "User not found"}
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def get_user_count(self) -> dict:
        """Get count of users by type"""
        try:
            count_data = self.user_repository.count_users()
            return {"success": True, **count_data}
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
            
    def check_internal(self) -> dict:
        """Kiểm tra trạng thái nội bộ của service"""
        try:
            # Test repository connection
            test_result = self.user_repository.test_connection()
            
            return {
                "status": "healthy" if test_result else "degraded",
                "uptime_seconds": int(time.time() - self._startup_time),
                "last_error": str(self._last_error) if self._last_error else None,
                "stats": self._stats.copy(),
                "repository_status": "connected" if test_result else "disconnected",
                "focus": "progress_based_upgrades"  # No money system
            }
        except Exception as e:
            self._last_error = e
            return {
                "status": "error",
                "error": str(e),
                "uptime_seconds": int(time.time() - self._startup_time)
            }

    def get_user_stats_only(self, user_id):
        """Lấy chỉ ATK và HP của user"""
        try:
            # user_data = self.get_user(user_id)
            user_data = self.get_user_gameplay(user_id)
            print(f"User data 1234 for {user_id}: {user_data}")
            if user_data:
                atk = user_data.get('atk', 0)
                hp = user_data.get('hp', 0)
                return {"atk": atk, "hp": hp}
            else:
                print(f"User with ID {user_id} not found")
                return None
        except Exception as e:
            print(f"User with ID {user_id} not found")
            return None

    def add_user_id_only(self, user_id, role="student"):
        """Add user profile với role được chỉ định"""
        return self.user_repository.add_user_id_only(user_id, role)

    def change_user_role(self, user_id: str, new_role: str) -> dict:
        """Thay đổi role của user"""
        try:
            # Validate role
            valid_roles = ['student', 'teacher', 'admin']
            if new_role not in valid_roles:
                return {
                    "success": False,
                    "error": f"Invalid role '{new_role}'. Must be one of: {valid_roles}"
                }
            
            # Lấy user hiện tại
            current_user = self.get_user(user_id)
            if not current_user:
                return {
                    "success": False,
                    "error": f"User with ID '{user_id}' not found"
                }
            
            old_role = current_user.get('role', 'student')
            
            # Nếu role giống nhau, không cần thay đổi
            if old_role == new_role:
                return {
                    "success": True,
                    "message": f"User already has role '{new_role}'",
                    "user": {
                        "user_id": user_id,
                        "old_role": old_role,
                        "new_role": new_role,
                        "changed": False
                    }
                }
            
            # Thay đổi role trong database
            result = self.user_repository.change_user_role(user_id, new_role)
            
            if result:
                return {
                    "success": True,
                    "message": f"User role changed from '{old_role}' to '{new_role}' successfully",
                    "user": {
                        "user_id": user_id,
                        "old_role": old_role,
                        "new_role": new_role,
                        "changed": True,
                        "permissions_updated": True
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to change user role in database"
                }
                
        except Exception as e:
            print(f"Error changing user role: {e}")
            return {
                "success": False,
                "error": f"Failed to change user role: {str(e)}"
            }