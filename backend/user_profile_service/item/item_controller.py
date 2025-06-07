from flask import jsonify
from .item_service import ItemService

class ItemController:
    """Item controller for single sword system"""
    
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

    def get_user_sword(self, user_id: str):
        """
        Lấy thông tin thanh kiếm duy nhất của student
        """
        try:
            result = self.item_service.get_user_sword(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 404
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get sword: {str(e)}"
            }), 500

    def upgrade_sword(self, user_id: str):
        """
        Nâng cấp thanh kiếm bằng vàng
        """
        try:
            result = self.item_service.upgrade_sword(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                error_message = result.get('error', '')
                if "not found" in error_message:
                    status_code = 404
                elif "maximum level" in error_message:
                    status_code = 422
                elif "Not enough money" in error_message:
                    status_code = 402  # Payment Required
                else:
                    status_code = 400
                return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to upgrade sword: {str(e)}"
            }), 500