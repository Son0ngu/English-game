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
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create UserProfile from dictionary"""
        return cls(**data)

class StudentProfile(UserProfile):
    """Student profile with game stats và map progression"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language_level = kwargs.get('language_level', 1)
        self.points = kwargs.get('points', 0)
        self.money = kwargs.get('money', 100)
        self.hp = kwargs.get('hp', 100)
        self.atk = kwargs.get('atk', 10)
        
        # Map progression fields
        self.current_map = kwargs.get('current_map', 1)
        self.max_map_unlocked = kwargs.get('max_map_unlocked', 1)
        self._maps_completed = kwargs.get('maps_completed', '[]')
        
        # Items
        self._items = kwargs.get('items', '[]')
        
        # Initialize items properly
        if 'items' in kwargs:
            self.set_items(kwargs['items'])

    def get_items(self) -> List[Dict[str, Any]]:
        """Get items as Python list"""
        try:
            if isinstance(self._items, str):
                return json.loads(self._items)
            elif isinstance(self._items, list):
                return self._items
            else:
                return []
        except:
            return []
            
    def set_items(self, items_list: List[Dict[str, Any]]) -> None:
        """Save items list"""
        if isinstance(items_list, list):
            self._items = json.dumps(items_list)
        elif isinstance(items_list, str):
            self._items = items_list
        else:
            self._items = '[]'
    
    def add_item(self, item: Dict[str, Any]) -> bool:
        """Add an item to inventory"""
        try:
            items = self.get_items()
            items.append(item)
            self.set_items(items)
            return True
        except:
            return False
    
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from inventory"""
        try:
            items = self.get_items()
            items = [item for item in items if item.get('id') != item_id]
            self.set_items(items)
            return True
        except:
            return False

    def get_maps_completed(self) -> List[int]:
        """Get completed maps as Python list"""
        try:
            if isinstance(self._maps_completed, str):
                return json.loads(self._maps_completed)
            elif isinstance(self._maps_completed, list):
                return self._maps_completed
            else:
                return []
        except:
            return []
            
    def set_maps_completed(self, maps_list: List[int]) -> None:
        """Save completed maps list"""
        if isinstance(maps_list, list):
            self._maps_completed = json.dumps(maps_list)
        elif isinstance(maps_list, str):
            self._maps_completed = maps_list
        else:
            self._maps_completed = '[]'
    
    def complete_map(self, map_number: int) -> bool:
        """Mark map as completed and unlock next map"""
        completed_maps = self.get_maps_completed()
        
        # Chỉ complete map theo thứ tự
        if map_number == self.current_map and map_number not in completed_maps:
            completed_maps.append(map_number)
            self.set_maps_completed(completed_maps)
            
            # Unlock next map
            self.current_map = map_number + 1
            self.max_map_unlocked = max(self.max_map_unlocked, map_number + 1)
            
            return True
        return False
    
    def can_access_map(self, map_number: int) -> bool:
        """Check if student can access specific map"""
        return map_number <= self.max_map_unlocked
    
    def get_map_progress(self) -> Dict[str, Any]:
        """Get map progression summary"""
        completed_maps = self.get_maps_completed()
        return {
            "current_map": self.current_map,
            "max_map_unlocked": self.max_map_unlocked,
            "completed_maps": completed_maps,
            "total_completed": len(completed_maps),
            "progress_percent": (len(completed_maps) / 10) * 100  # Giả sử có 10 maps
        }

    def view_progress(self) -> Dict[str, Any]:
        """View detailed progress information"""
        return {
            "user_id": self.id,
            "language_level": self.language_level,
            "points": self.points,
            "money": self.money,
            "hp": self.hp,
            "atk": self.atk,
            "map_progression": self.get_map_progress(),
            "total_items": len(self.get_items()),
            "last_updated": int(time.time())
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        base_dict = super().to_dict()
        base_dict.update({
            'language_level': self.language_level,
            'points': self.points,
            'money': self.money,
            'hp': self.hp,
            'atk': self.atk,
            'current_map': self.current_map,
            'max_map_unlocked': self.max_map_unlocked,
            'maps_completed': self._maps_completed,
            'items': self._items
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create StudentProfile from dictionary"""
        return cls(**data)

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
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create TeacherProfile from dictionary"""
        return cls(**data)