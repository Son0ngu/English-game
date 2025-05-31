from typing import Dict, List, Any, Optional, Tuple
from user_profile_service.item.item import Item
from user_profile_service.item.item_repository import ItemRepository
from user_profile_service.user.user_repository import UserRepository
from user_profile_service.user.user import StudentProfile
import time

class ItemService:
    """Item service focused on level-based weapon selection"""
    
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
                "focus": "level_based_weapon_selection"
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
        Lấy danh sách vũ khí hiện tại của user
        
        Args:
            user_id: ID của user
            
        Returns:
            Danh sách vũ khí đã chọn
        """
        try:
            items = self.item_repository.find_by_owner(user_id)
            return [item.to_dict() for item in items]
        except Exception as e:
            self._last_error = e
            return []

    def get_available_weapons_for_level(self, user_id: int) -> dict:
        """
        Lấy 3 vũ khí có thể chọn cho level hiện tại
        
        Args:
            user_id: ID của user
            
        Returns:
            Dictionary chứa thông tin vũ khí có thể chọn
        """
        try:
            # Lấy thông tin user
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            current_level = user.language_level
            
            # Lấy 3 vũ khí có thể chọn cho level hiện tại
            available_weapons = self.item_repository.get_available_weapons_for_level(current_level)
            
            return {
                "success": True,
                "user_level": current_level,
                "available_weapons": [weapon.to_dict() for weapon in available_weapons],
                "selection_required": len(available_weapons) > 0,
                "message": f"Choose 1 weapon from 3 options for level {current_level}"
            }
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}

    def select_weapon(self, user_id: int, weapon_id: str) -> dict:
        """
        Chọn vũ khí từ 3 options available
        
        Args:
            user_id: ID của user
            weapon_id: ID của weapon được chọn
            
        Returns:
            Kết quả việc chọn weapon
        """
        try:
            # Lấy thông tin user
            user = self.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            current_level = user.language_level
            
            # Lấy danh sách vũ khí có thể chọn
            available_weapons = self.item_repository.get_available_weapons_for_level(current_level)
            
            # Kiểm tra weapon_id có trong danh sách không
            selected_weapon = None
            for weapon in available_weapons:
                if weapon.id == weapon_id:
                    selected_weapon = weapon
                    break
            
            if not selected_weapon:
                return {
                    "success": False, 
                    "error": "Invalid weapon selection",
                    "available_weapons": [w.id for w in available_weapons]
                }
            
            # Tạo weapon instance cho user
            new_weapon = Item(
                id=f"{weapon_id}_user_{user_id}",
                name=selected_weapon.name,
                description=selected_weapon.description,
                effect=selected_weapon.effect,
                type=selected_weapon.type,
                tier=selected_weapon.tier,
                unlock_level=selected_weapon.unlock_level,
                owner_id=str(user_id),
                level=1,
                max_level=5
            )
            
            # Lưu weapon vào repository
            self.item_repository.save_item(new_weapon)
            
            # Cập nhật ATK của user dựa trên weapon effect
            user.atk = 10 + selected_weapon.effect  # Base ATK + weapon effect
            self.user_repository.save(user)
            
            return {
                "success": True,
                "selected_weapon": new_weapon.to_dict(),
                "user_level": current_level,
                "new_atk": user.atk,
                "message": f"Successfully selected {selected_weapon.name}!"
            }
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}

    def upgrade_weapon(self, user_id: int, weapon_id: str) -> dict:
        """
        Nâng cấp weapon hiện có (level up weapon)
        
        Args:
            user_id: ID của user
            weapon_id: ID của weapon cần upgrade
            
        Returns:
            Kết quả upgrade weapon
        """
        try:
            # Tìm weapon
            weapon = self.item_repository.find_by_id(weapon_id)
            if not weapon or weapon.owner_id != str(user_id):
                return {"success": False, "error": "Weapon not found or not owned"}
            
            # Kiểm tra có thể upgrade không
            if weapon.level >= weapon.max_level:
                return {"success": False, "error": "Weapon already at maximum level"}
            
            # Upgrade weapon
            old_level = weapon.level
            old_effect = weapon.effect
            
            weapon.level += 1
            weapon.effect = int(weapon.effect * 1.2)  # Tăng 20% effect mỗi level
            
            # Lưu weapon đã upgrade
            self.item_repository.save_item(weapon)
            
            # Cập nhật ATK của user
            user = self.user_repository.find_by_id(user_id)
            if user and isinstance(user, StudentProfile):
                user.atk = 10 + weapon.effect
                self.user_repository.save(user)
            
            return {
                "success": True,
                "weapon": weapon.to_dict(),
                "upgrade_info": {
                    "old_level": old_level,
                    "new_level": weapon.level,
                    "old_effect": old_effect,
                    "new_effect": weapon.effect,
                    "effect_increase": weapon.effect - old_effect
                },
                "new_user_atk": user.atk if user else None
            }
            
        except Exception as e:
            self._last_error = e
            return {"success": False, "error": str(e)}

    def get_upgradeable_items(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách weapons có thể nâng cấp
        
        Args:
            user_id: ID của user
            
        Returns:
            Danh sách weapons có thể upgrade
        """
        try:
            items = self.item_repository.find_by_owner(user_id)
            upgradeable = []
            
            for item in items:
                if item.level < item.max_level:
                    item_dict = item.to_dict()
                    item_dict['upgrade_preview'] = {
                        "next_level": item.level + 1,
                        "next_effect": int(item.effect * 1.2),
                        "effect_increase": int(item.effect * 1.2) - item.effect
                    }
                    upgradeable.append(item_dict)
            
            return upgradeable
        except Exception as e:
            self._last_error = e
            return []

    def get_item_details(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Lấy chi tiết của một weapon
        
        Args:
            item_id: ID của weapon
            
        Returns:
            Chi tiết weapon hoặc None
        """
        try:
            item = self.item_repository.find_by_id(item_id)
            if not item:
                return None
                
            item_dict = item.to_dict()
            
            # Thêm thông tin upgrade preview nếu có thể
            if item.level < item.max_level:
                item_dict['upgrade_preview'] = {
                    "next_level": item.level + 1,
                    "next_effect": int(item.effect * 1.2),
                    "effect_increase": int(item.effect * 1.2) - item.effect
                }
            
            return item_dict
        except Exception as e:
            self._last_error = e
            return None