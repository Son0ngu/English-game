from typing import List, Optional, Dict, Any
from .item import Item
from ..database_interface import ItemDatabaseInterface  # Import từ thư mục cha
import time

class ItemRepository:
    """Repository for weapon data storage - level-based system"""
    
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
            # BỎ: price=item_dict.get('price', 0),
            effect=item_dict.get('effect', 0),
            type=item_dict.get('type'),
            level=item_dict.get('level', 1),
            max_level=item_dict.get('max_level', 1),
            tier=item_dict.get('tier', 'common'),
            unlock_level=item_dict.get('unlock_level', 1),
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
    
    def get_available_weapons_for_level(self, user_level: int) -> List[Item]:
        """
        Lấy danh sách vũ khí có thể chọn cho level hiện tại
        
        Args:
            user_level: Level hiện tại của user
            
        Returns:
            Danh sách 3 vũ khí có thể chọn
        """
        # Template weapons cho từng level
        weapon_templates = self._get_weapon_templates_by_level(user_level)
        return [self._dict_to_item(weapon) for weapon in weapon_templates]
    
    def _get_weapon_templates_by_level(self, level: int) -> List[Dict[str, Any]]:
        """Get weapon templates based on user level"""
        weapon_templates = []
        
        if level >= 1:
            # Level 1-2: Common weapons
            weapon_templates.extend([
                {
                    "id": f"sword_common_lvl{level}",
                    "name": f"Iron Sword Lv.{level}",
                    "description": "A sturdy iron sword for beginners",
                    "effect": 5 + level * 2,
                    "type": "weapon",
                    "tier": "common",
                    "unlock_level": level,
                    "is_template": True
                },
                {
                    "id": f"bow_common_lvl{level}",
                    "name": f"Hunter Bow Lv.{level}",
                    "description": "A reliable bow for ranged combat",
                    "effect": 4 + level * 2,
                    "type": "weapon",
                    "tier": "common",
                    "unlock_level": level,
                    "is_template": True
                },
                {
                    "id": f"staff_common_lvl{level}",
                    "name": f"Wooden Staff Lv.{level}",
                    "description": "A magical staff for spell casting",
                    "effect": 6 + level * 2,
                    "type": "weapon",
                    "tier": "common",
                    "unlock_level": level,
                    "is_template": True
                }
            ])
        
        if level >= 5:
            # Level 5+: Rare weapons
            weapon_templates.extend([
                {
                    "id": f"sword_rare_lvl{level}",
                    "name": f"Silver Blade Lv.{level}",
                    "description": "A gleaming silver sword with enhanced power",
                    "effect": 8 + level * 3,
                    "type": "weapon",
                    "tier": "rare",
                    "unlock_level": level,
                    "is_template": True
                },
                {
                    "id": f"bow_rare_lvl{level}",
                    "name": f"Elven Longbow Lv.{level}",
                    "description": "An elegant elven bow with precision",
                    "effect": 7 + level * 3,
                    "type": "weapon",
                    "tier": "rare",
                    "unlock_level": level,
                    "is_template": True
                },
                {
                    "id": f"staff_rare_lvl{level}",
                    "name": f"Crystal Staff Lv.{level}",
                    "description": "A staff embedded with magical crystals",
                    "effect": 9 + level * 3,
                    "type": "weapon",
                    "tier": "rare",
                    "unlock_level": level,
                    "is_template": True
                }
            ])
        
        if level >= 10:
            # Level 10+: Legendary weapons
            weapon_templates.extend([
                {
                    "id": f"sword_legendary_lvl{level}",
                    "name": f"Dragon Slayer Lv.{level}",
                    "description": "A legendary sword forged from dragon scales",
                    "effect": 12 + level * 4,
                    "type": "weapon",
                    "tier": "legendary",
                    "unlock_level": level,
                    "is_template": True
                },
                {
                    "id": f"bow_legendary_lvl{level}",
                    "name": f"Phoenix Feather Bow Lv.{level}",
                    "description": "A bow crafted from phoenix feathers",
                    "effect": 11 + level * 4,
                    "type": "weapon",
                    "tier": "legendary",
                    "unlock_level": level,
                    "is_template": True
                },
                {
                    "id": f"staff_legendary_lvl{level}",
                    "name": f"Archmage Scepter Lv.{level}",
                    "description": "The ultimate staff of arcane mastery",
                    "effect": 13 + level * 4,
                    "type": "weapon",
                    "tier": "legendary",
                    "unlock_level": level,
                    "is_template": True
                }
            ])
        
        # Return top 3 weapons for current level
        available_weapons = [w for w in weapon_templates if w["unlock_level"] == level]
        return available_weapons[:3] if available_weapons else weapon_templates[-3:]