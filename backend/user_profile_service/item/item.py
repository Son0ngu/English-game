import time
import uuid
from typing import Dict, Any

class Item:
    """Item model for sword system only"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.effect = kwargs.get('effect', 5)  # Sword damage
        self.type = kwargs.get('type', 'weapon')  # Always weapon
        self.level = kwargs.get('level', 1)
        self.max_level = kwargs.get('max_level', 10)
        self.created_at = kwargs.get('created_at', int(time.time()))
        self.owner_id = kwargs.get('owner_id')
        self.is_template = kwargs.get('is_template', False)
        
        # Auto-generate ID if not provided
        if not self.id:
            if self.owner_id and not self.is_template:
                self.id = f"sword_{self.owner_id}"  # Unique sword per user
            else:
                self.id = str(uuid.uuid4())[:8]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'effect': self.effect,
            'type': self.type,
            'level': self.level,
            'max_level': self.max_level,
            'created_at': self.created_at,
            'owner_id': self.owner_id,
            'is_template': self.is_template
        }

    def can_upgrade(self) -> bool:
        """Check if sword can be upgraded"""
        return self.level < self.max_level

    def get_upgrade_cost(self) -> int:
        """Calculate upgrade cost: level^2 * 50"""
        return (self.level ** 2) * 50

    def upgrade(self) -> bool:
        """Upgrade sword level and effect"""
        if not self.can_upgrade():
            return False
        
        self.level += 1
        self.effect = int(self.effect * 1.3)  # 30% increase per level
        return True

    def __str__(self):
        return f"{self.name} (Level {self.level}/{self.max_level}, Effect: {self.effect})"