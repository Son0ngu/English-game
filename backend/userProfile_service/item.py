import time
import uuid
from typing import Dict, Any

class Item:
    """Item model for objects in the game"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.price = kwargs.get('price', 0)
        self.effect = kwargs.get('effect', 0)
        self.type = kwargs.get('type', '')
        self.level = kwargs.get('level', 1)
        self.max_level = kwargs.get('max_level', 1)
        self.created_at = kwargs.get('created_at', int(time.time()))
        self.owner_id = kwargs.get('owner_id')
        self.is_template = kwargs.get('is_template', False)
        
        # Tạo ID nếu chưa được cung cấp
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'effect': self.effect,
            'type': self.type,
            'level': self.level,
            'max_level': self.max_level,
            'created_at': self.created_at,
            'owner_id': self.owner_id,
            'is_template': self.is_template,
            'can_upgrade': self.level < self.max_level
        }