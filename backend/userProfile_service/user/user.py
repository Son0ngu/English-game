from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import time
import json
from typing import Dict, Any, List, Optional

Base = declarative_base()

class UserProfile:
    """Base user profile model"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        self.role = kwargs.get('role', 'student')
        self.created_at = kwargs.get('created_at', int(time.time()))
        self.last_login = kwargs.get('last_login', self.created_at)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary representation"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

class StudentProfile(UserProfile):
    """Student profile with game stats"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language_level = kwargs.get('language_level', 1)
        self.points = kwargs.get('points', 0)
        self.money = kwargs.get('money', 100)
        self.hp = kwargs.get('hp', 100)
        self.atk = kwargs.get('atk', 10)
        self._items = "[]"
        if 'items' in kwargs:
            self.set_items(kwargs['items'])
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Get student's items as Python list"""
        try:
            return json.loads(self._items)
        except:
            return []
            
    def set_items(self, items_list: List[Dict[str, Any]]) -> None:
        """Save items list back to storage format"""
        self._items = json.dumps(items_list)
    
    def buy_item(self, item: Dict[str, Any], cost: int) -> bool:
        """Buy an item if student has enough money"""
        if self.money >= cost:
            self.money -= cost
            items = self.get_items()
            items.append(item)
            self.set_items(items)
            return True
        return False
    
    def view_progress(self) -> Dict[str, Any]:
        """Get student's learning progress"""
        return {
            "level": self.language_level,
            "points": self.points,
            "items_count": len(self.get_items()),
            "progress_percent": min(100, (self.points / 1000) * 100)  # Giả sử 1000 điểm = 100%
        }
    
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subjects = "[]"
        if 'subjects' in kwargs:
            self.set_subjects(kwargs['subjects'])
    
    def get_subjects(self) -> List[str]:
        """Get teacher's subjects as Python list"""
        try:
            return json.loads(self._subjects)
        except:
            return []
            
    def set_subjects(self, subjects_list: List[str]) -> None:
        """Save subjects list back to storage format"""
        self._subjects = json.dumps(subjects_list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to include teacher-specific fields"""
        data = super().to_dict()
        data.update({
            'subjects': self.get_subjects()
        })
        return data