from typing import Optional, Dict, Any
from .item import Item
from ..database_interface import ItemDatabaseInterface
import time

class ItemRepository:
    """Repository for single sword system - minimal and focused"""
    
    def __init__(self):
        """Initialize repository with database interface"""
        self.db = ItemDatabaseInterface()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            connection = self.db._get_connection()
            connection.close()
            return True
        except Exception as e:
            print(f"Item database connection failed: {e}")
            return False

    def find_by_id(self, item_id: str) -> Optional[Item]:
        """Find sword by ID"""
        item_dict = self.db.get_item_by_id(item_id)
        return self._dict_to_item(item_dict)

    def save_item(self, item: Item) -> Item:
        """Save sword to database"""
        item_dict = item.to_dict()
        item_id = self.db.save_item(item_dict)
        
        if not item.id:
            item.id = item_id
            
        return item

    def _dict_to_item(self, item_dict: Dict[str, Any]) -> Optional[Item]:
        """Convert dictionary to Item object"""
        if not item_dict:
            return None
            
        return Item(
            id=item_dict.get('id'),
            name=item_dict.get('name'),
            description=item_dict.get('description'),
            effect=item_dict.get('effect', 5),
            type=item_dict.get('type', 'weapon'),
            level=item_dict.get('level', 1),
            max_level=item_dict.get('max_level', 10),
            created_at=item_dict.get('created_at', int(time.time())),
            owner_id=item_dict.get('owner_id'),
            is_template=item_dict.get('is_template', False)
        )