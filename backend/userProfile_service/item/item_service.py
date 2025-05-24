import time
from typing import Dict, List, Any, Optional, Tuple
from userProfile_service.item.item import Item
from userProfile_service.item.item_repository import ItemRepository

class ItemService:
    def __init__(self):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {
            "item_purchases": 0, 
            "item_views": 0, 
            "item_upgrades": 0,
            "upgrades_successful": 0
        }
        self.repository = ItemRepository()
        
        # Catalog items (used when repository is not available)
        self.available_items = [
            {
                "id": "dict1", 
                "name": "Basic Dictionary", 
                "price": 100, 
                "effect": 5, 
                "type": "book",
                "level": 1,
                "max_level": 3,
                "can_upgrade": True
            },
            {
                "id": "dict2", 
                "name": "Advanced Dictionary", 
                "price": 300, 
                "effect": 15, 
                "type": "book",
                "level": 1,
                "max_level": 5,
                "can_upgrade": True
            },
            {
                "id": "pen1", 
                "name": "Magic Pen", 
                "price": 50, 
                "effect": 2, 
                "type": "tool",
                "level": 1,
                "max_level": 2,
                "can_upgrade": True
            }
        ]
        
        # Initialize database with catalog items
        self._initialize_catalog()
    
    def _initialize_catalog(self):
        """Ensure catalog items exist in database"""
        try:
            templates = self.repository.find_templates()
            
            if not templates or len(templates) == 0:
                for item_data in self.available_items:
                    template = Item(
                        id=item_data["id"],
                        name=item_data["name"],
                        price=item_data["price"],
                        effect=item_data["effect"],
                        type=item_data["type"],
                        level=item_data.get("level", 1),
                        max_level=item_data.get("max_level", 1),
                        is_template=True,
                        description=item_data.get("description", f"A {item_data['name']}")
                    )
                    self.repository.save_item(template)
        except Exception as e:
            self._last_error = e
        
    def get_item_catalog(self) -> List[Dict[str, Any]]:
        """Get all available items that can be purchased"""
        self._stats["item_views"] += 1
        
        try:
            templates = self.repository.find_templates()
            return [item.to_dict() for item in templates]
        except Exception as e:
            self._last_error = e
            return self.available_items
        
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get item details by ID"""
        try:
            item = self.repository.find_by_id(item_id)
            return item.to_dict() if item else None
        except Exception as e:
            self._last_error = e
            return None
    
    def get_user_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all items owned by a user"""
        try:
            items = self.repository.find_by_owner(user_id)
            return [item.to_dict() for item in items]
        except Exception as e:
            self._last_error = e
            return []
    
    def purchase_item(self, user_id: str, item_id: str) -> Dict[str, Any]:
        """Purchase an item from catalog for a user"""
        self._stats["item_purchases"] += 1
        
        try:
            # Get template from catalog
            template = self.repository.find_by_id(item_id)
            
            if not template or not template.is_template:
                return {"success": False, "message": "Item not found in catalog"}
            
            # Create new instance for user
            user_item = Item(
                name=template.name,
                description=template.description,
                price=template.price, 
                effect=template.effect,
                type=template.type,
                level=template.level,
                max_level=template.max_level,
                owner_id=user_id,
                is_template=False
            )
            
            # Save to database
            self.repository.save_item(user_item)
            
            return {
                "success": True,
                "message": f"Successfully purchased {template.name}",
                "item": user_item.to_dict(),
                "cost": template.price
            }
        except Exception as e:
            self._last_error = e
            return {"success": False, "message": f"Error purchasing item: {str(e)}"}
    
    def can_upgrade(self, item_id: str) -> Tuple[bool, str]:
        """Check if an item can be upgraded"""
        try:
            item = self.repository.find_by_id(item_id)
            
            if not item:
                return False, "Item not found"
                
            if item.level >= item.max_level:
                return False, "Item already at maximum level"
                
            if item.is_template:
                return False, "Templates cannot be upgraded"
                
            return True, "Item can be upgraded"
        except Exception as e:
            self._last_error = e
            return False, f"Error checking upgrade eligibility: {str(e)}"
    
    def get_upgrade_details(self, item_id: str) -> Dict[str, Any]:
        """Get item upgrade details including cost and effect changes"""
        try:
            item = self.repository.find_by_id(item_id)
            
            if not item:
                return {"error": "Item not found"}
                
            if item.level >= item.max_level:
                return {"error": "Item already at maximum level"}
            
            # Calculate upgrade costs and effects
            upgrade_cost = self._calculate_upgrade_cost(item)
            new_effect = self._calculate_new_effect(item)
            
            return {
                "item_id": item.id,
                "item_name": item.name,
                "current_level": item.level,
                "next_level": item.level + 1,
                "max_level": item.max_level,
                "upgrade_cost": upgrade_cost,
                "current_effect": item.effect,
                "next_effect": new_effect,
                "effect_increase": new_effect - item.effect
            }
        except Exception as e:
            self._last_error = e
            return {"error": f"Error getting upgrade details: {str(e)}"}
    
    def upgrade_item(self, item_id: str, user_id: str, available_money: int) -> Dict[str, Any]:
        """Upgrade an item owned by the user"""
        self._stats["item_upgrades"] += 1
        
        try:
            # Check if item can be upgraded
            can_upgrade, message = self.can_upgrade(item_id)
            
            if not can_upgrade:
                return {"success": False, "message": message}
                
            # Get item
            item = self.repository.find_by_id(item_id)
            
            # Verify ownership
            if item.owner_id != user_id:
                return {"success": False, "message": "You don't own this item"}
            
            # Calculate upgrade cost
            upgrade_cost = self._calculate_upgrade_cost(item)
            
            # Check if user has enough money
            if available_money < upgrade_cost:
                return {"success": False, "message": "Insufficient funds for upgrade"}
            
            # Calculate new effect
            new_effect = self._calculate_new_effect(item)
            
            # Upgrade the item
            old_level = item.level
            item.level += 1
            item.effect = new_effect
            
            # Save updated item
            self.repository.save_item(item)
            self._stats["upgrades_successful"] += 1
            
            return {
                "success": True,
                "message": f"Item upgraded from level {old_level} to {item.level}",
                "cost": upgrade_cost,
                "item": item.to_dict()
            }
        except Exception as e:
            self._last_error = e
            return {"success": False, "message": f"Error upgrading item: {str(e)}"}
    
    def _calculate_upgrade_cost(self, item) -> int:
        """Calculate cost to upgrade an item to next level"""
        if item.level >= item.max_level:
            return 0
            
        # Base formula: price * (1.5^current_level)
        return int(item.price * (1.5 ** item.level))
    
    def _calculate_new_effect(self, item) -> int:
        """Calculate new effect after upgrade"""
        if item.level >= item.max_level:
            return item.effect
            
        # Base formula: effect * 1.3
        return int(item.effect * 1.3)
    
    def check_internal(self) -> dict:
        """Internal health check for this service"""
        return {
            "status": "healthy" if not self._last_error else "degraded",
            "uptime": time.time() - self._startup_time,
            "stats": self._stats,
            "items_count": self._count_items(),
            "last_error": str(self._last_error) if self._last_error else None,
            "details": "Item service running normally"
        }
        
    def _count_items(self) -> int:
        """Count items in database"""
        try:
            templates = self.repository.find_templates()
            return len(templates)
        except Exception:
            return 0