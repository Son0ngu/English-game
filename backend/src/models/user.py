import hashlib
import time
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from bson import ObjectId
from typing import Dict, Any, List, Optional

Base = declarative_base()

class UserProfile:
    """Base user profile with dual database support for SQLite and MongoDB"""
    
    # Common fields for all database types
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password_hash = Column(String(256))
    email = Column(String(100))
    created_at = Column(Integer)
    last_login = Column(Integer)
    role = Column(String(20))  # "student", "teacher", "admin"
    
    def __init__(self, id=None, username=None, email=None):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = int(time.time())
        self.last_login = None
        self.role = "user"
        self.data = {}
    
    def set_password(self, password):
        """Hash and set the user's password"""
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
            'last_login': self.last_login,
            **self.data
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
    
    def save_to_mongo(self, collection):
        """Save user to MongoDB database"""
        data = self.to_mongo()
        
        if '_id' in data and data['_id'] is None:
            # Insert new document
            result = collection.insert_one(data)
            self.id = result.inserted_id
        else:
            # Update existing document
            collection.replace_one({'_id': data['_id']}, data, upsert=True)
            
        return self

class StudentProfile(UserProfile, Base):
    """Student user profile with game stats"""
    
    __tablename__ = 'student_profiles'
    
    # SQLAlchemy fields
    id = Column(Integer, ForeignKey('user_profiles.id'), primary_key=True)
    language_level = Column(Integer, default=1)
    points = Column(Integer, default=0)
    money = Column(Integer, default=0)
    hp = Column(Integer, default=100)
    atk = Column(Integer, default=10)
    items = Column(Text)  # Store as JSON string
    
    def __init__(self, id=None, username=None, email=None):
        super().__init__(id, username, email)
        self.language_level = 1
        self.points = 0
        self.money = 0
        self.hp = 100
        self.atk = 10
        self.items = "[]"  # JSON array as string
        self.role = "student"
    
    def view_progress(self):
        """Retrieve student's learning progress"""
        # Implementation would query progress from appropriate data source
        return {"level": self.language_level, "points": self.points}
        
    def participate_in_game(self):
        """Initialize game participation"""
        return {
            "ready": True,
            "hp": self.hp,
            "atk": self.atk,
            "inventory": self.get_items()
        }
    
    def buy_item(self, item, cost: int) -> bool:
        """Purchase an item if student can afford it"""
        if self.can_afford(cost):
            self.money -= cost
            items = self.get_items()
            items.append(item)
            self.set_items(items)
            return True
        return False
    
    def can_afford(self, cost: int) -> bool:
        """Check if student can afford an item"""
        return self.money >= cost
    
    def difficulty_setting(self, value: int) -> None:
        """Update student's preferred difficulty setting"""
        self.data["preferred_difficulty"] = value
    
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
        """Extended dictionary representation with student-specific fields"""
        base_dict = super().to_dict()
        return {
            **base_dict,
            'language_level': self.language_level,
            'points': self.points,
            'money': self.money,
            'hp': self.hp,
            'atk': self.atk,
            'items': self.get_items()
        }
    
    def to_mongo(self) -> Dict[str, Any]:
        """Convert to MongoDB document with student-specific fields"""
        doc = super().to_mongo()
        doc['items'] = self.get_items()  # Store as native array in MongoDB
        return doc
    
    @classmethod
    def from_mongo(cls, document: Dict[str, Any]):
        """Create student instance from MongoDB document"""
        student = super().from_mongo(document)
        
        if student and 'items' in document:
            import json
            student.items = json.dumps(document['items'])
            
        return student

class TeacherProfile(UserProfile, Base):
    """Teacher user profile"""
    
    __tablename__ = 'teacher_profiles'
    
    # SQLAlchemy fields
    id = Column(Integer, ForeignKey('user_profiles.id'), primary_key=True)
    subjects = Column(Text)  # Store as JSON array
    
    def __init__(self, id=None, username=None, email=None):
        super().__init__(id, username, email)
        self.subjects = "[]"  # JSON array as string
        self.role = "teacher"
    
    def manage_student(self):
        """Access student management functionality"""
        # Implementation for student management
        return {"access": True, "role": self.role}
    
    def assign_activity(self):
        """Assign learning activities to students"""
        # Implementation for assignment
        return {"assigned": True}
    
    def give_feedback(self):
        """Provide feedback on student work"""
        # Implementation for feedback
        return {"feedback_enabled": True}
    
    def create_course(self, data):
        """Create a new course from course data"""
        # Implementation for course creation
        from ..models.course import Course
        return Course()
    
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
        """Extended dictionary representation with teacher-specific fields"""
        base_dict = super().to_dict()
        return {
            **base_dict,
            'subjects': self.get_subjects()
        }
    
    def to_mongo(self) -> Dict[str, Any]:
        """Convert to MongoDB document with teacher-specific fields"""
        doc = super().to_mongo()
        doc['subjects'] = self.get_subjects()  # Store as native array in MongoDB
        return doc
    
    @classmethod
    def from_mongo(cls, document: Dict[str, Any]):
        """Create teacher instance from MongoDB document"""
        teacher = super().from_mongo(document)
        
        if teacher and 'subjects' in document:
            import json
            teacher.subjects = json.dumps(document['subjects'])
            
        return teacher