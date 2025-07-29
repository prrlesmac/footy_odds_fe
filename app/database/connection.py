from sqlalchemy import create_engine
from app.config.settings import Config

class DatabaseConnection:
    _engine = None
    
    @classmethod
    def get_engine(cls):
        """Get or create database engine (singleton pattern)."""
        if cls._engine is None:
            config = Config()
            cls._engine = create_engine(config.DATABASE_URL)
        return cls._engine
    
    @classmethod
    def execute_query(cls, query):
        """Execute a query and return results."""
        engine = cls.get_engine()
        with engine.connect() as conn:
            result = conn.execute(query)
            return result.fetchall()