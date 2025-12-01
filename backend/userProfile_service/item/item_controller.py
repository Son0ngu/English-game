from flask import jsonify
from .item_service import ItemService

class ItemController:
    """Item controller focused on upgrades only"""
    
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
        Lấy danh sách items của user với thông tin upgrade
        
        Args:
            user_id: ID của user
        """
        try:
            items = self.item_service.get_user_items(user_id)
            return jsonify({
                "user_id": user_id,
                "items": items,
                "count": len(items),
                "focus": "upgrade_system"
            }), 200
        except Exception as e:
            return jsonify({
                "error": f"Failed to get user items: {str(e)}"
            }), 500

    def get_upgradeable_items(self, user_id: str):
        """
        Lấy danh sách items có thể nâng cấp của user
        
        Args:
            user_id: ID của user
        """
        try:
            items = self.item_service.get_upgradeable_items(user_id)
            return jsonify({
                "user_id": user_id,
                "upgradeable_items": items,
                "count": len(items)
            }), 200
        except Exception as e:
            return jsonify({
                "error": f"Failed to get upgradeable items: {str(e)}"
            }), 500

    def get_item(self, item_id: str):
        """
        Lấy chi tiết của một item
        
        Args:
            item_id: ID của item
        """
        try:
            item = self.item_service.get_item_details(item_id)
            if item:
                return jsonify(item), 200
            else:
                return jsonify({"error": "Item not found"}), 404
        except Exception as e:
            return jsonify({
                "error": f"Failed to get item details: {str(e)}"
            }), 500

    def upgrade_item(self, data):
        """
        Nâng cấp item của user
        
        Args:
            data: Dictionary chứa thông tin nâng cấp
                - user_id: ID của user
                - item_id: ID của item
                - available_money: Số tiền hiện có
        """
        try:
            user_id = data.get('user_id')
            item_id = data.get('item_id')
            available_money = data.get('available_money', 0)

            if not user_id or not item_id:
                return jsonify({
                    "success": False,
                    "error": "Missing required fields: user_id, item_id"
                }), 400

            result = self.item_service.upgrade_item(user_id, item_id, available_money)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                # Trả về status code khác nhau tùy theo lỗi
                error_code = result.get('error_code')
                if error_code == 'ITEM_NOT_FOUND':
                    status_code = 404
                elif error_code == 'NOT_OWNER':
                    status_code = 403
                elif error_code == 'INSUFFICIENT_FUNDS':
                    status_code = 402  # Payment Required
                elif error_code in ['MAX_LEVEL_REACHED', 'CANNOT_UPGRADE']:
                    status_code = 422  # Unprocessable Entity
                else:
                    status_code = 500
                    
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to upgrade item: {str(e)}",
                "error_code": "CONTROLLER_ERROR"
            }), 500

    def calculate_upgrade_cost(self, item_id: str):
        """
        Tính toán chi phí nâng cấp cho một item
        
        Args:
            item_id: ID của item
        """
        try:
            item = self.item_service.get_item_details(item_id)
            if not item:
                return jsonify({"error": "Item not found"}), 404
                
            upgrade_info = item.get('upgrade_info')
            if not upgrade_info:
                return jsonify({
                    "error": "No upgrade information available for this item"
                }), 422
                
            return jsonify({
                "item_id": item_id,
                "item_name": item.get('name'),
                "upgrade_cost_info": upgrade_info
            }), 200
            
        except Exception as e:
            return jsonify({
                "error": f"Failed to calculate upgrade cost: {str(e)}"
            }), 500