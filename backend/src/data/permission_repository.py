from typing import Dict, List, Any
import json
import os

class PermissionRepository:
    """Repository for persisting permissions to database/file"""
    
    def __init__(self, db_config=None):
        self.db_config = db_config or {}
        self.file_path = self.db_config.get("permissions_file", "permissions.json")
    
    def save_permissions(self, role_permissions: Dict[str, List[str]], 
                         temp_permissions: Dict[str, int]) -> bool:
        """Save permissions to file"""
        try:
            data = {
                "role_permissions": role_permissions,
                "temp_permissions": temp_permissions
            }
            
            os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving permissions: {str(e)}")
            return False
    
    def load_permissions(self) -> Dict[str, Any]:
        """Load permissions from file"""
        try:
            if not os.path.exists(self.file_path):
                return {
                    "role_permissions": {
                        "student": ["READ"],
                        "teacher": ["READ", "WRITE"],
                        "admin": ["READ", "WRITE", "DELETE"]
                    },
                    "temp_permissions": {}
                }
                
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Error loading permissions: {str(e)}")
            return {
                "role_permissions": {
                    "student": ["READ"],
                    "teacher": ["READ", "WRITE"],
                    "admin": ["READ", "WRITE", "DELETE"]
                },
                "temp_permissions": {}
            }