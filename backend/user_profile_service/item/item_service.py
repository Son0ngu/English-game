import time
from typing import List, Dict, Any, Optional
from .item_repository import ItemRepository
from user_profile_service.user.user_repository import UserRepository
from user_profile_service.user.user import StudentProfile

class ItemService:
    """Item service focused on single sword system"""
    
    def __init__(self):
        """Khởi tạo ItemService"""
        self._startup_time = time.time()
        self._last_error = None
        self.item_repository = ItemRepository()
        self.user_repository = UserRepository()

    def check_internal(self) -> dict:
        """Kiểm tra trạng thái nội bộ của service"""
        try:
            repository_status = self.item_repository.test_connection()
            
            return {
                "status": "healthy" if repository_status else "degraded",
                "uptime_seconds": int(time.time() - self._startup_time),
                "last_error": str(self._last_error) if self._last_error else None,
                "repository_status": "connected" if repository_status else "disconnected",
                "focus": "single_sword_upgrade_system"
            }
        except Exception as e:
            self._last_error = e
            return {
                "status": "error",
                "error": str(e),
                "uptime_seconds": int(time.time() - self._startup_time)
            }

    def get_user_sword(self, user_id: str) -> dict:
        """
        Lấy thanh kiếm duy nhất của student
        
        Args:
            user_id: ID của user
            
        Returns:
            Thông tin thanh kiếm
        """
        try:
            # Lấy thông tin user
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Tìm sword duy nhất của user
            sword_id = f"sword_{user_id}"
            sword = self.item_repository.find_by_id(sword_id)
            
            if not sword:
                return {"success": False, "error": "Sword not found"}
            
            # Tính cost upgrade cho level tiếp theo
            next_upgrade_cost = self._calculate_upgrade_cost(sword.level) if sword.level < sword.max_level else None
            
            sword_data = sword.to_dict()
            sword_data['upgrade_cost'] = next_upgrade_cost
            sword_data['can_afford'] = user.money >= next_upgrade_cost if next_upgrade_cost else False
            
            # Standardized response format
            return {
                "success": True,
                "data": {
                    "sword": sword_data,
                    "user_stats": {
                        "money": user.money,
                        "hp": user.hp,
                        "atk": user.atk,
                        "level": user.language_level
                    },
                    "upgrade_info": {
                        "can_upgrade": sword.can_upgrade(),
                        "current_cost": next_upgrade_cost,
                        "can_afford": user.money >= next_upgrade_cost if next_upgrade_cost else False,
                        "progress": f"{sword.level}/{sword.max_level}"
                    }
                },
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": int(time.time())
            }

    def _calculate_upgrade_cost(self, current_level: int) -> int:
        """Tính cost nâng cấp: level^2 * 50 vàng"""
        return (current_level ** 2) * 50

    def upgrade_sword(self, user_id: str) -> dict:
        """Upgrade sword with enhanced validation"""
        try:
            # Validate input
            if not user_id or not isinstance(user_id, str):
                return {"success": False, "error": "Invalid user_id"}

            # Lấy thông tin user
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Validate user money
            if user.money < 0:
                return {"success": False, "error": "Invalid money amount"}

            # Tìm sword
            sword_id = f"sword_{user_id}"
            sword = self.item_repository.find_by_id(sword_id)
            if not sword:
                return {"success": False, "error": "Sword not found"}
            
            # Kiểm tra có thể upgrade không
            if not sword.can_upgrade():
                return {"success": False, "error": f"Sword already at maximum level ({sword.max_level})"}
            
            # Tính cost upgrade
            upgrade_cost = sword.get_upgrade_cost()
            
            # Kiểm tra đủ tiền không
            if user.money < upgrade_cost:
                return {
                    "success": False, 
                    "error": f"Not enough money. Required: {upgrade_cost}, Have: {user.money}",
                    "upgrade_cost": upgrade_cost,
                    "user_money": user.money
                }
            
            # Lưu giá trị cũ
            old_level = sword.level
            old_effect = sword.effect
            old_money = user.money
            old_hp = user.hp
            old_atk = user.atk
            
            # Upgrade sword
            sword.level += 1
            sword.effect = int(sword.effect * 1.3)  # Tăng 30% effect mỗi level
            
            # Trừ tiền user
            user.money -= upgrade_cost
            
            # Nâng cấp stats của user
            hp_increase = 20  # Mỗi level tăng 20 HP
            atk_increase = int(sword.effect * 0.5)  # ATK = 50% sword effect
            
            user.hp += hp_increase
            user.atk = 10 + atk_increase  # Base ATK + bonus từ sword
            
            # Lưu thay đổi
            self.item_repository.save_item(sword)
            self.user_repository.save(user)
            
            return {
                "success": True,
                "sword": sword.to_dict(),
                "upgrade_info": {
                    "old_level": old_level,
                    "new_level": sword.level,
                    "old_effect": old_effect,
                    "new_effect": sword.effect,
                    "effect_increase": sword.effect - old_effect,
                    "upgrade_cost": upgrade_cost,
                    "money_before": old_money,
                    "money_after": user.money
                },
                "stat_changes": {
                    "hp": {"old": old_hp, "new": user.hp, "increase": hp_increase},
                    "atk": {"old": old_atk, "new": user.atk, "increase": user.atk - old_atk}
                },
                "next_upgrade_cost": self._calculate_upgrade_cost(sword.level) if sword.level < sword.max_level else None
            }
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}