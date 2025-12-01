from typing import Dict, List, Any, Optional, Tuple
from userProfile_service.item.item import Item
from userProfile_service.item.item_repository import ItemRepository
import time
import math

class ItemService:
    """Item service focused on item upgrades only"""
    
    def __init__(self):
        """Khởi tạo ItemService"""
        self._startup_time = time.time()
        self._last_error = None
        self.item_repository = ItemRepository()
        
        # Upgrade configuration
        self._upgrade_cost_multiplier = 1.5  # Cost increases 50% per level
        self._effect_improvement_rate = 1.3  # Effect increases 30% per level

    def check_internal(self) -> dict:
        """Kiểm tra trạng thái nội bộ của service"""
        try:
            repository_status = self.item_repository.test_connection()
            
            return {
                "status": "healthy" if repository_status else "degraded",
                "uptime_seconds": int(time.time() - self._startup_time),
                "last_error": str(self._last_error) if self._last_error else None,
                "repository_status": "connected" if repository_status else "disconnected",
                "focus": "item_upgrades_only"
            }
        except Exception as e:
            self._last_error = e
            return {
                "status": "error",
                "error": str(e),
                "uptime_seconds": int(time.time() - self._startup_time)
            }

    def get_user_items(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách items của user
        
        Args:
            user_id: ID của user
            
        Returns:
            Danh sách items với thông tin upgrade
        """
        try:
            items = self.item_repository.find_by_owner(user_id)
            result = []
            
            for item in items:
                item_dict = item.to_dict()
                
                # Thêm thông tin upgrade
                if item.level < item.max_level:
                    upgrade_info = self.calculate_upgrade_cost(item)
                    item_dict['upgrade_info'] = upgrade_info
                else:
                    item_dict['upgrade_info'] = {
                        "can_upgrade": False,
                        "reason": "max_level_reached"
                    }
                
                result.append(item_dict)
            
            return result
        except Exception as e:
            self._last_error = e
            return []

    def calculate_upgrade_cost(self, item: Item) -> Dict[str, Any]:
        """
        Tính toán chi phí nâng cấp item
        
        Args:
            item: Item cần tính chi phí
            
        Returns:
            Dictionary chứa thông tin chi phí và hiệu ứng sau nâng cấp
        """
        if item.level >= item.max_level:
            return {
                "can_upgrade": False,
                "reason": "max_level_reached",
                "current_level": item.level,
                "max_level": item.max_level
            }
        
        # Tính chi phí nâng cấp
        base_cost = item.price if item.price > 0 else 100
        upgrade_cost = int(base_cost * (self._upgrade_cost_multiplier ** item.level))
        
        # Tính effect sau nâng cấp
        current_effect = item.effect if item.effect > 0 else 1
        new_effect = int(current_effect * self._effect_improvement_rate)
        
        return {
            "can_upgrade": True,
            "current_level": item.level,
            "next_level": item.level + 1,
            "max_level": item.max_level,
            "upgrade_cost": upgrade_cost,
            "current_effect": item.effect,
            "new_effect": new_effect,
            "effect_increase": new_effect - item.effect,
            "cost_currency": "coins"
        }

    def upgrade_item(self, user_id: str, item_id: str, available_money: int) -> Dict[str, Any]:
        """
        Nâng cấp item của user
        
        Args:
            user_id: ID của user
            item_id: ID của item cần nâng cấp
            available_money: Số tiền hiện có của user
            
        Returns:
            Kết quả nâng cấp
        """
        try:
            # Tìm item
            item = self.item_repository.find_by_id(item_id)
            if not item:
                return {
                    "success": False,
                    "error": "Item not found",
                    "error_code": "ITEM_NOT_FOUND"
                }
            
            # Kiểm tra ownership
            if item.owner_id != user_id:
                return {
                    "success": False,
                    "error": "You don't own this item",
                    "error_code": "NOT_OWNER"
                }
            
            # Kiểm tra có thể nâng cấp không
            if item.level >= item.max_level:
                return {
                    "success": False,
                    "error": "Item is already at maximum level",
                    "error_code": "MAX_LEVEL_REACHED",
                    "current_level": item.level,
                    "max_level": item.max_level
                }
            
            # Tính chi phí
            upgrade_info = self.calculate_upgrade_cost(item)
            if not upgrade_info["can_upgrade"]:
                return {
                    "success": False,
                    "error": "Item cannot be upgraded",
                    "error_code": "CANNOT_UPGRADE"
                }
            
            upgrade_cost = upgrade_info["upgrade_cost"]
            new_effect = upgrade_info["new_effect"]
            
            # Kiểm tra tiền
            if available_money < upgrade_cost:
                return {
                    "success": False,
                    "error": f"Not enough money. Need {upgrade_cost}, have {available_money}",
                    "error_code": "INSUFFICIENT_FUNDS",
                    "required": upgrade_cost,
                    "available": available_money,
                    "deficit": upgrade_cost - available_money
                }
            
            # Thực hiện nâng cấp
            old_level = item.level
            old_effect = item.effect
            
            success = self.item_repository.update_item_level(
                item_id, 
                item.level + 1, 
                new_effect
            )
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully upgraded {item.name}",
                    "item_id": item_id,
                    "item_name": item.name,
                    "upgrade_cost": upgrade_cost,
                    "old_level": old_level,
                    "new_level": old_level + 1,
                    "old_effect": old_effect,
                    "new_effect": new_effect,
                    "effect_increase": new_effect - old_effect,
                    "remaining_money": available_money - upgrade_cost
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to upgrade item (database error)",
                    "error_code": "DATABASE_ERROR"
                }
                
        except Exception as e:
            self._last_error = e
            return {
                "success": False,
                "error": f"Internal error: {str(e)}",
                "error_code": "INTERNAL_ERROR"
            }

    def get_upgradeable_items(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách items có thể nâng cấp của user
        
        Args:
            user_id: ID của user
            
        Returns:
            Danh sách items có thể nâng cấp với thông tin chi phí
        """
        try:
            upgradeable_items = self.item_repository.find_upgradeable_items(user_id)
            result = []
            
            for item in upgradeable_items:
                item_dict = item.to_dict()
                upgrade_info = self.calculate_upgrade_cost(item)
                item_dict['upgrade_info'] = upgrade_info
                result.append(item_dict)
            
            return result
        except Exception as e:
            self._last_error = e
            return []

    def get_item_details(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Lấy chi tiết của một item
        
        Args:
            item_id: ID của item
            
        Returns:
            Chi tiết item hoặc None
        """
        try:
            item = self.item_repository.find_by_id(item_id)
            if not item:
                return None
                
            item_dict = item.to_dict()
            
            # Thêm thông tin upgrade nếu có thể
            if item.level < item.max_level:
                upgrade_info = self.calculate_upgrade_cost(item)
                item_dict['upgrade_info'] = upgrade_info
            
            return item_dict
        except Exception as e:
            self._last_error = e
            return None