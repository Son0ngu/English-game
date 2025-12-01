from flask import jsonify
from userProfile_service.item.item_service import ItemService
import time

class ItemController:
    def __init__(self, item_service: ItemService):
        """
        Khởi tạo ItemController với ItemService
        
        Parameters:
            item_service: Dịch vụ quản lý vật phẩm
        """
        self.item_service = item_service

    def get_all_items(self):
        """Lấy tất cả các vật phẩm mẫu"""
        templates = self.item_service.get_item_catalog()
        return jsonify({"items": templates}), 200

    def get_item(self, item_id):
        """Lấy thông tin một vật phẩm cụ thể"""
        item = self.item_service.get_item_by_id(item_id)
        if not item:
            return jsonify({"error": f"Item with ID {item_id} not found"}), 404
        return jsonify({"item": item}), 200

    def get_user_items(self, user_id):
        """Lấy tất cả vật phẩm của một người dùng"""
        items = self.item_service.get_user_items(user_id)
        return jsonify({"items": items, "user_id": user_id}), 200

    def purchase_item(self, data):
        """Mua vật phẩm cho người dùng"""
        if not data or 'user_id' not in data or 'item_id' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        result = self.item_service.purchase_item(data['user_id'], data['item_id'])
        
        if not result.get('success', False):
            return jsonify({"error": result.get('error', "Failed to purchase item")}), 400
        
        return jsonify(result), 200

    def upgrade_item(self, data):
        """Nâng cấp vật phẩm"""
        if not data or 'user_id' not in data or 'item_id' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        available_money = data.get('available_money', 0)
        
        result = self.item_service.upgrade_item(
            data['item_id'], 
            data['user_id'],
            available_money
        )
        
        if not result.get('success', False):
            return jsonify({"error": result.get('error', "Failed to upgrade item")}), 400
        
        return jsonify(result), 200
        
    def check_health(self):
        """Kiểm tra trạng thái dịch vụ"""
        # Implement health check logic if needed
        return jsonify({
            "status": "healthy",
            "service": "item_service",
            "timestamp": int(time.time())
        }), 200