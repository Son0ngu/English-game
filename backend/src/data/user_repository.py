from typing import List, Optional, Union
from sqlalchemy.orm import Session
from ..models.user import UserProfile, StudentProfile, TeacherProfile
from sqlalchemy import text
import time
from bson import ObjectId

class UserRepository:
    """Repository for user data storage and retrieval"""
    
    def __init__(self, db_type: str, connection):
        """Initialize repository with database connection
        
        Args:
            db_type: Type of database ("sqlite" or "mongodb")
            connection: SQLAlchemy session or MongoDB client
        """
        self.db_type = db_type
        self.connection = connection
    
    def save(self, user: UserProfile) -> UserProfile:
        """Save a user to the database"""
        if self.db_type == "sqlite":
            session = self.connection
            session.add(user)
            session.commit()
            return user
        else:
            # MongoDB implementation
            collection = self.connection.users
            data = user.to_mongo()
            if '_id' in data and data['_id'] is None:
                result = collection.insert_one(data)
                user.id = result.inserted_id
            else:
                collection.replace_one({'_id': data['_id']}, data, upsert=True)
            return user
    
    def find_by_id(self, user_id: Union[str, int, ObjectId]) -> Optional[UserProfile]:
        """Find a user by ID"""
        if self.db_type == "sqlite":
            session = self.connection
            
            # First try as student
            student = session.query(StudentProfile).filter(StudentProfile.id == user_id).first()
            if student:
                return student
                
            # Then try as teacher
            teacher = session.query(TeacherProfile).filter(TeacherProfile.id == user_id).first()
            return teacher
        else:
            # MongoDB implementation
            collection = self.connection.users
            data = collection.find_one({'_id': user_id})
            
            if not data:
                return None
                
            # Create appropriate user type based on role
            role = data.get('role', 'student')
            if role == 'teacher':
                return TeacherProfile.from_mongo(data)
            else:
                return StudentProfile.from_mongo(data)
    
    def find_by_username(self, username: str) -> Optional[UserProfile]:
        """Find a user by username"""
        if self.db_type == "sqlite":
            session = self.connection
            
            # Try as student first
            student = session.query(StudentProfile).filter(
                text("username = :username")
            ).params(username=username).first()
            
            if student:
                return student
                
            # Try as teacher next
            teacher = session.query(TeacherProfile).filter(
                text("username = :username")
            ).params(username=username).first()
            
            return teacher
        else:
            # MongoDB implementation
            collection = self.connection.users
            data = collection.find_one({'username': username})
            
            if not data:
                return None
                
            # Create appropriate user type
            role = data.get('role', 'student')
            if role == 'teacher':
                return TeacherProfile.from_mongo(data)
            else:
                return StudentProfile.from_mongo(data)
    
    def find_students(self, limit: int = 100, offset: int = 0) -> List[StudentProfile]:
        """Find all students with pagination"""
        if self.db_type == "sqlite":
            session = self.connection
            return session.query(StudentProfile).limit(limit).offset(offset).all()
        else:
            # MongoDB implementation
            collection = self.connection.users
            cursor = collection.find({'role': 'student'}).skip(offset).limit(limit)
            
            students = []
            for data in cursor:
                student = StudentProfile.from_mongo(data)
                if student:
                    students.append(student)
            
            return students
    
    def find_teachers(self, limit: int = 100, offset: int = 0) -> List[TeacherProfile]:
        """Find all teachers with pagination"""
        if self.db_type == "sqlite":
            session = self.connection
            return session.query(TeacherProfile).limit(limit).offset(offset).all()
        else:
            # MongoDB implementation
            collection = self.connection.users
            cursor = collection.find({'role': 'teacher'}).skip(offset).limit(limit)
            
            teachers = []
            for data in cursor:
                teacher = TeacherProfile.from_mongo(data)
                if teacher:
                    teachers.append(teacher)
            
            return teachers
    
    def delete_user(self, user_id: Union[str, int, ObjectId]) -> bool:
        """Delete a user by ID
        
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if self.db_type == "sqlite":
            session = self.connection
            
            # Try as student first
            student = session.query(StudentProfile).filter(StudentProfile.id == user_id).first()
            if student:
                session.delete(student)
                session.commit()
                return True
                
            # Try as teacher next
            teacher = session.query(TeacherProfile).filter(TeacherProfile.id == user_id).first()
            if teacher:
                session.delete(teacher)
                session.commit()
                return True
                
            return False
        else:
            # MongoDB implementation
            collection = self.connection.users
            result = collection.delete_one({'_id': user_id})
            return result.deleted_count > 0
    
    def count_users(self) -> dict:
        """Count users by role"""
        if self.db_type == "sqlite":
            session = self.connection
            student_count = session.query(StudentProfile).count()
            teacher_count = session.query(TeacherProfile).count()
            
            return {
                'students': student_count,
                'teachers': teacher_count,
                'total': student_count + teacher_count
            }
        else:
            # MongoDB implementation
            collection = self.connection.users
            student_count = collection.count_documents({'role': 'student'})
            teacher_count = collection.count_documents({'role': 'teacher'})
            
            return {
                'students': student_count,
                'teachers': teacher_count,
                'total': student_count + teacher_count
            }