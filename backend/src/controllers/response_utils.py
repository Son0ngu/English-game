from flask import jsonify
from ..utils.mongo_formatter import MongoFormatter
from typing import Any, Dict, List, Union, Optional

def mongo_response(data: Any, status_code: int = 200):
    """Create Flask response with MongoDB-style JSON format"""
    mongo_data = MongoFormatter.to_mongo_style(data)
    return jsonify(mongo_data), status_code

def error_response(message: str, status_code: int = 400):
    """Create error response in MongoDB-style"""
    error_data = {
        "error": True,
        "message": message,
        "status": status_code
    }
    return jsonify(error_data), status_code