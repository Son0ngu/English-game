from flask import Blueprint, request
from injector import inject
from ..services.item_service import ItemService
from ..services.user_service import UserProfileService
from ..controllers.response_utils import mongo_response, error_response

# Create blueprint for item routes
item_bp = Blueprint('items', __name__, url_prefix='/api/items')

@item_bp.route('/', methods=['GET'])
@inject
def get_all_items(item_service: ItemService):
    """Get all item templates"""
    templates = item_service.get_all_templates()
    return mongo_response({"items": templates})

@item_bp.route('/<item_id>', methods=['GET'])
@inject
def get_item(item_service: ItemService, item_id: str):
    """Get a specific item"""
    item = item_service.get_item(item_id)
    if not item:
        return error_response(f"Item with ID {item_id} not found", 404)
    return mongo_response({"item": item})

@item_bp.route('/user/<user_id>', methods=['GET'])
@inject
def get_user_items(item_service: ItemService, user_id: str):
    """Get all items owned by a user"""
    items = item_service.get_user_items(user_id)
    return mongo_response({"items": items, "user_id": user_id})

@item_bp.route('/purchase', methods=['POST'])
@inject
def purchase_item(item_service: ItemService, user_service: UserProfileService):
    """Purchase an item for a user"""
    data = request.json
    if not data or 'user_id' not in data or 'item_id' not in data:
        return error_response("Missing required fields", 400)
    
    result = item_service.purchase_item(data['user_id'], data['item_id'])
    if not result.get('success', False):
        return error_response(result.get('error', "Failed to purchase item"), 400)
    
    return mongo_response(result)

@item_bp.route('/upgrade', methods=['POST'])
@inject
def upgrade_item(item_service: ItemService):
    """Upgrade an item"""
    data = request.json
    if not data or 'user_id' not in data or 'item_id' not in data:
        return error_response("Missing required fields", 400)
    
    result = item_service.upgrade_item(data['user_id'], data['item_id'])
    if not result.get('success', False):
        return error_response(result.get('error', "Failed to upgrade item"), 400)
    
    return mongo_response(result)