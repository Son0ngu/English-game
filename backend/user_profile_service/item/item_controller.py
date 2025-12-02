from flask import jsonify
from .item_service import ItemService

class ItemController:
    """Item controller for level-based weapon selection"""
    
    def __init__(self, item_service: ItemService):
        """
        Khởi tạo ItemController
        
        Args:
            item_service: Service xử lý logic item
        """
        self.item_service = item_service

    def check_health(self):
        """Kiểm tra tình trạng hoạt động của Item service"""
        try:
            health_status = self.item_service.check_internal()
            status_code = 200 if health_status.get('status') == 'healthy' else 503
            return jsonify(health_status), status_code
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": f"Health check failed: {str(e)}"
            }), 500

    def get_user_items(self, user_id: str):
        """
        Lấy danh sách weapons của user
        
        Args:
            user_id: ID của user
        """
        try:
            items = self.item_service.get_user_items(user_id)
            return jsonify({
                "user_id": user_id,
                "weapons": items,
                "count": len(items),
                "system": "level_based_selection"
            }), 200
        except Exception as e:
            return jsonify({
                "error": f"Failed to get user weapons: {str(e)}"
            }), 500

    def get_available_weapons(self, user_id: str):
        """
        Lấy 3 weapons có thể chọn cho level hiện tại
        
        Args:
            user_id: ID của user
        """
        try:
            result = self.item_service.get_available_weapons_for_level(int(user_id))
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 404
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get available weapons: {str(e)}"
            }), 500

    def select_weapon(self, data):
        """
        Chọn weapon từ 3 options
        
        Args:
            data: Dictionary chứa user_id và weapon_id
        """
        try:
            user_id = data.get('user_id')
            weapon_id = data.get('weapon_id')

            if not user_id or not weapon_id:
                return jsonify({
                    "success": False,
                    "error": "Missing required fields: user_id, weapon_id"
                }), 400

            result = self.item_service.select_weapon(int(user_id), weapon_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to select weapon: {str(e)}"
            }), 500

    def upgrade_weapon(self, data):
        """
        Nâng cấp weapon (level up)
        
        Args:
            data: Dictionary chứa user_id và weapon_id
        """
        try:
            user_id = data.get('user_id')
            weapon_id = data.get('weapon_id')

            if not user_id or not weapon_id:
                return jsonify({
                    "success": False,
                    "error": "Missing required fields: user_id, weapon_id"
                }), 400

            result = self.item_service.upgrade_weapon(int(user_id), weapon_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                error_message = result.get('error', '')
                if "not found" in error_message or "not owned" in error_message:
                    status_code = 404
                elif "maximum level" in error_message:
                    status_code = 422
                else:
                    status_code = 400
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to upgrade weapon: {str(e)}"
            }), 500

    def get_upgradeable_items(self, user_id: str):
        """
        Lấy danh sách weapons có thể upgrade
        
        Args:
            user_id: ID của user
        """
        try:
            items = self.item_service.get_upgradeable_items(user_id)
            return jsonify({
                "user_id": user_id,
                "upgradeable_weapons": items,
                "count": len(items)
            }), 200
        except Exception as e:
            return jsonify({
                "error": f"Failed to get upgradeable weapons: {str(e)}"
            }), 500

    def get_item(self, item_id: str):
        """
        Lấy chi tiết của một weapon
        
        Args:
            item_id: ID của weapon
        """
        try:
            item = self.item_service.get_item_details(item_id)
            if item:
                return jsonify(item), 200
            else:
                return jsonify({"error": "Weapon not found"}), 404
        except Exception as e:
            return jsonify({
                "error": f"Failed to get weapon details: {str(e)}"
            }), 500