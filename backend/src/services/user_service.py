from ..models.user import UserProfile, StudentProfile, TeacherProfile
from ..data.user_repository import UserRepository
import hashlib
import time
from typing import Dict, List, Optional, Any, Union
from bson import ObjectId

class UserProfileService:
    def __init__(self, user_repository: UserRepository):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"login_attempts": 0, "profile_updates": 0, "progress_updates": 0}
        self.user_repository = user_repository
    
    def authenticate(self, username: str, password: str) -> dict:
        """Authenticate a user by username and password"""
        self._stats["login_attempts"] += 1
        try:
            user = self.user_repository.find_by_username(username)
            if user and user.verify_password(password):
                # Update last login time
                user.last_login = int(time.time())
                self.user_repository.save(user)
                return {"success": True, "user_id": user.id, "role": user.role}
            return {"success": False, "error": "Invalid credentials"}
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def create_user(self, user_data: dict, user_type: str = "student") -> dict:
        """Create a new user"""
        try:
            # Check if username already exists
            if self.user_repository.find_by_username(user_data.get('username')):
                return {"success": False, "error": "Username already exists"}
            
            # Create appropriate user type
            if user_type == "teacher":
                user = TeacherProfile(
                    username=user_data.get('username'),
                    email=user_data.get('email')
                )
                
                # Set teacher-specific fields
                if 'subjects' in user_data:
                    user.set_subjects(user_data['subjects'])
                    
            else:  # Default to student
                user = StudentProfile(
                    username=user_data.get('username'),
                    email=user_data.get('email')
                )
                
                # Set student-specific fields
                if 'language_level' in user_data:
                    user.language_level = user_data['language_level']
                
            # Set password
            if 'password' in user_data:
                user.set_password(user_data['password'])
            
            # Save user
            saved_user = self.user_repository.save(user)
            
            return {"success": True, "user_id": str(saved_user.id)}
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def get_user(self, user_id: Union[str, int, ObjectId]) -> Optional[dict]:
        """Get user details by ID"""
        try:
            user = self.user_repository.find_by_id(user_id)
            if user:
                return user.to_dict()
            return None
        except Exception as e:
            self._last_error = e
            return None
    
    def update_profile(self, user_id: Union[str, int, ObjectId], updates: dict) -> dict:
        """Update user profile attributes"""
        self._stats["profile_updates"] += 1
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Update basic user properties
            for key, value in updates.items():
                if hasattr(user, key) and key not in ['id', 'password_hash', 'role']:
                    setattr(user, key, value)
            
            # Handle special fields based on user type
            if isinstance(user, StudentProfile):
                if 'items' in updates:
                    user.set_items(updates['items'])
                    
                if 'preferred_difficulty' in updates:
                    user.difficulty_setting(updates['preferred_difficulty'])
                    
            elif isinstance(user, TeacherProfile):
                if 'subjects' in updates:
                    user.set_subjects(updates['subjects'])
            
            # Save updated user
            self.user_repository.save(user)
            return {"success": True}
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def update_progress(self, user_id: Union[str, int, ObjectId], lesson_id: str, points: int) -> dict:
        """Update user progress for a specific lesson"""
        self._stats["progress_updates"] += 1
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Update points
            user.points += points
            
            # Save updated user
            self.user_repository.save(user)
            return {"success": True, "total_points": user.points}
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
    
    def get_student_progress(self, user_id: Union[str, int, ObjectId]) -> dict:
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
    
    def buy_item_for_student(self, user_id: Union[str, int, ObjectId], item: dict, cost: int) -> dict:
        """Purchase an item for a student"""
        try:
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Try to buy the item
            success = user.buy_item(item, cost)
            if not success:
                return {"success": False, "error": "Insufficient funds"}
            
            # Save updated user
            self.user_repository.save(user)
            return {
                "success": True, 
                "remaining_money": user.money,
                "items": user.get_items()
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
    
    def delete_user(self, user_id: Union[str, int, ObjectId]) -> dict:
        """Delete a user"""
        try:
            success = self.user_repository.delete_user(user_id)
            if success:
                return {"success": True}
            return {"success": False, "error": "User not found"}
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}
            
    def check_internal(self) -> dict:
        """Internal health check for this service"""
        try:
            # Get count of users from repository
            student_count = len(self.user_repository.find_students(1000))
            teacher_count = len(self.user_repository.find_teachers(1000))
            
            return {
                "status": "healthy" if not self._last_error else "degraded",
                "uptime": time.time() - self._startup_time,
                "user_stats": {
                    "students": student_count,
                    "teachers": teacher_count,
                    "total": student_count + teacher_count
                },
                "operation_stats": self._stats,
                "last_error": str(self._last_error) if self._last_error else None,
                "details": "User profile service running normally"
            }
        except Exception as e:
            self._last_error = e
            return {
                "status": "degraded",
                "uptime": time.time() - self._startup_time,
                "last_error": str(e),
                "details": "User profile service health check failed"
            }