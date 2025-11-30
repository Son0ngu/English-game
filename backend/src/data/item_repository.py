from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.item import Item

class ItemRepository:
    """Repository for item data storage"""
    
    def __init__(self, db_type: str, connection):
        """
        Initialize repository
        
        Args:
            db_type: "sqlite" or "mongodb" 
            connection: SQLAlchemy session or MongoDB client
        """
        self.db_type = db_type
        self.connection = connection
    
    def save_item(self, item: Item) -> Item:
        """Save an item to database"""
        if self.db_type == "sqlite":
            session = self.connection
            session.add(item)
            session.commit()
            return item
        else:
            # MongoDB implementation
            collection = self.connection.items
            data = item.to_mongo()
            collection.replace_one({'_id': data['_id']}, data, upsert=True)
            return item
    
    def find_by_id(self, item_id: str) -> Optional[Item]:
        """Find an item by ID"""
        if self.db_type == "sqlite":
            session = self.connection
            return session.query(Item).filter(Item.id == item_id).first()
        else:
            # MongoDB implementation
            collection = self.connection.items
            data = collection.find_one({'_id': item_id})
            if not data:
                return None
                
            item = Item()
            for key, value in data.items():
                if key == '_id':
                    item.id = value
                elif hasattr(item, key):
                    setattr(item, key, value)
            return item
    
    def find_templates(self) -> List[Item]:
        """Find all item templates"""
        if self.db_type == "sqlite":
            session = self.connection
            return session.query(Item).filter(Item.is_template == True).all()
        else:
            # MongoDB implementation
            collection = self.connection.items
            items_data = collection.find({'is_template': True})
            
            result = []
            for data in items_data:
                item = Item()
                item.id = data['_id']
                for key, value in data.items():
                    if key != '_id' and hasattr(item, key):
                        setattr(item, key, value)
                result.append(item)
            return result
    
    def find_by_owner(self, owner_id: str) -> List[Item]:
        """Find all items owned by a user"""
        if self.db_type == "sqlite":
            session = self.connection
            return session.query(Item).filter(Item.owner_id == owner_id).all()
        else:
            # MongoDB implementation
            collection = self.connection.items
            items_data = collection.find({'owner_id': owner_id})
            
            result = []
            for data in items_data:
                item = Item()
                item.id = data['_id']
                for key, value in data.items():
                    if key != '_id' and hasattr(item, key):
                        setattr(item, key, value)
                result.append(item)
            return result