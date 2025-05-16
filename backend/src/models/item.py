from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
import time
from typing import Dict, Any

Base = declarative_base()

class Item(Base):
    """Item model for database storage"""
    
    __tablename__ = 'items'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, default=0)
    effect = Column(Integer, default=0)
    type = Column(String(50))
    level = Column(Integer, default=1)
    max_level = Column(Integer, default=1) 
    created_at = Column(Integer)
    owner_id = Column(String(100), nullable=True)
    is_template = Column(Boolean, default=False)
    
    def __init__(self, **kwargs):
        self.created_at = int(time.time())
        
        # Tạo ID nếu chưa được cung cấp
        if 'id' not in kwargs:
            import uuid
            self.id = str(uuid.uuid4())[:8]
            
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
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
    
    def to_mongo(self) -> Dict[str, Any]:
        """Convert to MongoDB format"""
        data = self.to_dict()
        data['_id'] = self.id
        if 'id' in data:
            del data['id']
        return data