from flask import Blueprint, request
from injector import inject
from ..services.item_service import ItemService
from ..services.user_service import UserProfileService
from ..controllers.response_utils import mongo_response, error_response

# Create blueprint for item routes
item_bp = Blueprint('items', __name__, url_prefix='/api/items')

@item_bp.route('/catalog', methods=['GET'])
@inject
def get_catalog(item_service: ItemService):
    """Get item catalog"""
    items = item_service.get_item_catalog()
    return mongo_response({"items": items})

@item_bp.route('/<item_id>', methods=['GET'])
@inject
def get_item(item_service: ItemService, item_id: str):
    """Get item details"""
    item = item_service.get_item_by_id(item_id)
    if not item:
        return error_response("Item not found", 404)
    return mongo_response(item)

@item_bp.route('/user/<user_id>', methods=['GET'])
@inject
def get_user_items(item_service: ItemService, user_id: str):
    """Get user's items"""
    items = item_service.get_user_items(user_id)
    return mongo_response({"user_id": user_id, "items": items})

@item_bp.route('/purchase', methods=['POST'])
@inject
def purchase_item(item_service: ItemService, user_service: UserProfileService):
    """Purchase an item"""
    data = request.json
    
    if not data or 'user_id' not in data or 'item_id' not in data:
        return error_response("Missing required fields", 400)
    
    # Get user's money
    user = user_service.get_user(data['user_id'])
    if not user:
        return error_response("User not found", 404)
    
    # Get item price
    item = item_service.get_item_by_id(data['item_id'])
    if not item:
        return error_response("Item not found", 404)
    
    # Check if user has enough money
    if user.get('money', 0) < item.get('price', 0):
        return error_response("Insufficient funds", 400)
    
    # Purchase item
    result = item_service.purchase_item(data['user_id'], data['item_id'])
    
    if result.get('success'):
        # Update user's money
        user_service.update_profile(
            data['user_id'], 
            {"money": user.get('money', 0) - item.get('price', 0)}
        )
        return mongo_response(result, 201)
    else:
        return error_response(result.get('message', "Failed to purchase item"), 400)

@item_bp.route('/<item_id>/upgrade', methods=['POST'])
@inject
def upgrade_item(item_service: ItemService, user_service: UserProfileService, item_id: str):
    """Upgrade an item"""
    data = request.json
    
    if not data or 'user_id' not in data:
        return error_response("Missing user_id", 400)
    
    # Get user's money
    user = user_service.get_user(data['user_id'])
    if not user:
        return error_response("User not found", 404)
    
    # Get upgrade details
    upgrade_info = item_service.get_upgrade_details(item_id)
    if 'error' in upgrade_info:
        return error_response(upgrade_info['error'], 400)
    
    # Check if user has enough money
    if user.get('money', 0) < upgrade_info.get('upgrade_cost', 0):
        return error_response("Insufficient funds for upgrade", 400)
    
    # Attempt upgrade
    result = item_service.upgrade_item(
        item_id, 
        data['user_id'], 
        user.get('money', 0)
    )
    
    if result.get('success'):
        # Update user's money
        user_service.update_profile(
            data['user_id'], 
            {"money": user.get('money', 0) - result.get('cost', 0)}
        )
        return mongo_response(result)
    else:
        return error_response(result.get('message', "Failed to upgrade item"), 400)

@item_bp.route('/<item_id>/upgrade-info', methods=['GET'])
@inject
def get_upgrade_info(item_service: ItemService, item_id: str):
    """Get upgrade information for an item"""
    upgrade_info = item_service.get_upgrade_details(item_id)
    
    if 'error' in upgrade_info:
        return error_response(upgrade_info['error'], 404 if "not found" in upgrade_info['error'] else 400)
    
    return mongo_response(upgrade_info)