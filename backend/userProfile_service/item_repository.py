from typing import List, Optional, Dict, Any
from .item import Item
from .database_interface import ItemDatabaseInterface

class ItemRepository:
    """Repository for item data storage"""
    
    def __init__(self):
        """Initialize repository with database interface"""
        self.db = ItemDatabaseInterface()
    
    def _dict_to_item(self, item_dict: Dict[str, Any]) -> Optional[Item]:
        """
        Chuyển đổi dictionary thành đối tượng Item
        
        Args:
            item_dict: Dictionary chứa dữ liệu item
            
        Returns:
            Đối tượng Item
        """
        if not item_dict:
            return None
            
        item = Item(
            id=item_dict.get('id'),
            name=item_dict.get('name'),
            description=item_dict.get('description'),
            price=item_dict.get('price', 0),
            effect=item_dict.get('effect', 0),
            type=item_dict.get('type'),
            level=item_dict.get('level', 1),
            max_level=item_dict.get('max_level', 1),
            created_at=item_dict.get('created_at', int(time.time())),
            owner_id=item_dict.get('owner_id'),
            is_template=item_dict.get('is_template', False)
        )
        
        return item
    
    def save_item(self, item: Item) -> Item:
        """
        Lưu item vào database
        
        Args:
            item: Đối tượng Item cần lưu
            
        Returns:
            Đối tượng Item đã lưu
        """
        # Chuyển đổi đối tượng thành dictionary
        item_dict = item.to_dict()
        
        # Lưu vào database và lấy ID
        item_id = self.db.save_item(item_dict)
        
        # Cập nhật ID nếu là item mới
        if not item.id:
            item.id = item_id
            
        return item
    
    def find_by_id(self, item_id: str) -> Optional[Item]:
        """
        Tìm item theo ID
        
        Args:
            item_id: ID của item
            
        Returns:
            Đối tượng Item hoặc None nếu không tìm thấy
        """
        item_dict = self.db.get_item_by_id(item_id)
        return self._dict_to_item(item_dict)
    
    def find_templates(self) -> List[Item]:
        """
        Tìm tất cả các item mẫu (template)
        
        Returns:
            Danh sách các đối tượng Item template
        """
        templates_dict = self.db.get_templates()
        return [self._dict_to_item(t) for t in templates_dict]
    
    def find_by_owner(self, owner_id: str) -> List[Item]:
        """
        Tìm tất cả các item của một người dùng
        
        Args:
            owner_id: ID của người dùng sở hữu
            
        Returns:
            Danh sách các đối tượng Item thuộc sở hữu của người dùng
        """
        items_dict = self.db.get_items_by_owner(owner_id)
        return [self._dict_to_item(i) for i in items_dict]