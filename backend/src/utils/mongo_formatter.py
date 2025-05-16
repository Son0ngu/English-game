from bson import ObjectId
from typing import Any, Dict, List, Union
import json
import uuid

class MongoFormatter:
    """Utility to format SQLite data as MongoDB-style JSON"""
    
    @staticmethod
    def format_id(id_value: Any) -> str:
        """Format any ID as MongoDB-style string ID"""
        if id_value is None:
            return str(uuid.uuid4())
        if isinstance(id_value, ObjectId):
            return str(id_value)
        return str(id_value)
    
    @staticmethod
    def to_mongo_style(data: Any) -> Union[Dict, List, Any]:
        """Convert SQLAlchemy model or dictionary to MongoDB-style JSON"""
        if hasattr(data, 'to_mongo'):
            # Object has a built-in to_mongo method
            return data.to_mongo()
        
        if hasattr(data, 'to_dict'):
            # Convert to dict first
            data = data.to_dict()
        
        if isinstance(data, dict):
            result = {}
            # Convert 'id' to '_id'
            if 'id' in data:
                result['_id'] = MongoFormatter.format_id(data['id'])
                # Keep original id for compatibility
                result['id'] = data['id']
            else:
                # Generated ID if none exists
                result['_id'] = MongoFormatter.format_id(None)
            
            # Process all other fields
            for key, value in data.items():
                if key != 'id':
                    result[key] = MongoFormatter.to_mongo_style(value)
            
            return result
            
        elif isinstance(data, list):
            return [MongoFormatter.to_mongo_style(item) for item in data]
        
        return data
    
    @staticmethod
    def to_json(data: Any) -> str:
        """Convert data to MongoDB-style JSON string"""
        class MongoJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, ObjectId):
                    return str(obj)
                return super().default(obj)
        
        mongo_data = MongoFormatter.to_mongo_style(data)
        return json.dumps(mongo_data, cls=MongoJSONEncoder)