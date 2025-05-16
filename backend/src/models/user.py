from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from bson import ObjectId
import hashlib
import time
from typing import Dict, Any, List, Optional

Base = declarative_base()

class UserProfile(Base):
    """Base user profile model"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(String(20), default="student")
    created_at = Column(Integer)
    last_login = Column(Integer)
    
    def __init__(self, **kwargs):
        self.created_at = int(time.time())
        self.last_login = self.created_at
        self.data = {}
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify a password against the stored hash"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary representation"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    def to_mongo(self) -> Dict[str, Any]:
        """Convert user to MongoDB document format"""
        from ..utils.mongo_formatter import MongoFormatter
        
        data = self.to_dict()
        
        # Tạo _id từ id
        data['_id'] = MongoFormatter.format_id(self.id)
        
        # MongoDB convention là dùng _id, không dùng id
        if 'id' in data:
            del data['id']
            
        return data
    
    @classmethod
    def from_mongo(cls, document: Dict[str, Any]):
        """Create user instance from MongoDB document"""
        if not document:
            return None
            
        user = cls()
        
        # Map MongoDB _id to id
        if '_id' in document:
            user.id = document['_id']
            
        # Copy all other fields
        for key, value in document.items():
            if key != '_id' and hasattr(user, key):
                setattr(user, key, value)
                
        return user
        
    def save_to_sqlite(self, session):
        """Save user to SQLite database"""
        session.add(self)
        session.commit()
        return self


class StudentProfile(UserProfile):
    """Student profile with game stats"""
    __tablename__ = 'student_profiles'
    
    id = Column(Integer, ForeignKey('user_profiles.id'), primary_key=True)
    language_level = Column(Integer, default=1)
    points = Column(Integer, default=0)
    money = Column(Integer, default=100)
    hp = Column(Integer, default=100)
    atk = Column(Integer, default=10)
    items = Column(Text, default="[]")  # JSON string of items
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Get student's items as Python list"""
        import json
        try:
            return json.loads(self.items)
        except:
            return []
            
    def set_items(self, items_list: List[Dict[str, Any]]) -> None:
        """Save items list back to storage format"""
        import json
        self.items = json.dumps(items_list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to include student-specific fields"""
        data = super().to_dict()
        data.update({
            'language_level': self.language_level,
            'points': self.points,
            'money': self.money, 
            'hp': self.hp,
            'atk': self.atk,
            'items': self.get_items()
        })
        return data


class TeacherProfile(UserProfile):
    """Teacher profile with teaching info"""
    __tablename__ = 'teacher_profiles'
    
    id = Column(Integer, ForeignKey('user_profiles.id'), primary_key=True)
    subjects = Column(Text, default="[]")  # JSON string of subjects
    
    def get_subjects(self) -> List[str]:
        """Get teacher's subjects as Python list"""
        import json
        try:
            return json.loads(self.subjects)
        except:
            return []
            
    def set_subjects(self, subjects_list: List[str]) -> None:
        """Save subjects list back to storage format"""
        import json
        self.subjects = json.dumps(subjects_list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to include teacher-specific fields"""
        data = super().to_dict()
        data.update({
            'subjects': self.get_subjects()
        })
        return data