from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from typing import Union, Dict
import os

class DatabaseConfig:
    def __init__(self, config=None):
        self.config = config or {}
        # Luôn mặc định sử dụng SQLite
        self.db_type = "sqlite"
        self._sqlite_connection = None
        self._mongo_connection = None
    
    def get_connection(self):
        """Get database connection based on configured type"""
        # Luôn sử dụng SQLite connection
        return self._get_sqlite_connection()
    
    def _get_sqlite_connection(self):
        """Get SQLite connection"""
        if not self._sqlite_connection:
            db_path = self.config.get("sqlite_path", "english_game.db")
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            sqlite_url = f"sqlite:///{db_path}"
            engine = create_engine(sqlite_url)
            Session = sessionmaker(bind=engine)
            
            # Create tables if they don't exist
            from ..models.user import Base as UserBase
            from ..models.item import Base as ItemBase
            
            UserBase.metadata.create_all(engine)
            ItemBase.metadata.create_all(engine)
            
            self._sqlite_connection = Session()
        
        return self._sqlite_connection
    
    def close(self):
        """Close database connections"""
        if self._sqlite_connection:
            self._sqlite_connection.close()
            self._sqlite_connection = None