from userProfile_service.user.user import UserProfile, StudentProfile, TeacherProfile
from userProfile_service.user.user_repository import UserRepository
import time
from typing import Dict, List, Optional, Any

class UserProfileService:
    def __init__(self):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"profile_updates": 0, "progress_updates": 0}
        self.user_repository = UserRepository()
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user details by ID"""
        try:
            user = self.user_repository.find_by_id(user_id)
            if user:
                return user.to_dict()
            return None
        except Exception as e:
            self._last_error = e
            return None
    
    def update_profile(self, user_id: int, updates: dict) -> dict:
        """Update user profile attributes"""
        self._stats["profile_updates"] += 1
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Update basic user properties
            for key, value in updates.items():
                if hasattr(user, key) and key not in ['id', 'role', 'created_at']:
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
    
    def update_progress(self, user_id: int, lesson_id: str, points: int) -> dict:
        """Update user progress for a specific lesson"""
        self._stats["progress_updates"] += 1
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Update points and potentially level
            old_points = user.points
            user.points += points
            
            # Level up logic (every 1000 points = 1 level)
            old_level = user.language_level
            new_level = max(1, user.points // 1000 + 1)
            user.language_level = new_level
            
            # Save updated user
            self.user_repository.save(user)
            
            return {
                "success": True, 
                "old_points": old_points,
                "new_points": user.points,
                "points_gained": points,
                "old_level": old_level,
                "new_level": new_level,
                "level_up": new_level > old_level
            }
            
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
    
    def update_student_money(self, user_id: int, amount: int, operation: str = "add") -> dict:
        """Update student's money (for item purchases/rewards)"""
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            old_money = user.money
            
            if operation == "add":
                user.money += amount
            elif operation == "subtract":
                if user.money < amount:
                    return {"success": False, "error": "Insufficient funds", "current_money": user.money, "required": amount}
                user.money -= amount
            elif operation == "set":
                user.money = amount
            else:
                return {"success": False, "error": "Invalid operation. Use 'add', 'subtract', or 'set'"}
            
            # Save updated user
            self.user_repository.save(user)
            
            return {
                "success": True,
                "old_money": old_money,
                "new_money": user.money,
                "amount_changed": amount,
                "operation": operation
            }
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def update_student_stats(self, user_id: int, hp: int = None, atk: int = None) -> dict:
        """Update student's game stats (HP, ATK)"""
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
            
            return {"success": True, "updates": updates}
            
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
                "focus": "user_management_read_only"  # No creation, no authentication
            }
        except Exception as e:
            self._last_error = e
            return {
                "status": "error",
                "error": str(e),
                "uptime_seconds": int(time.time() - self._startup_time)
            }