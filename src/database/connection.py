"""
Database Connection Manager
PostgreSQL connection pooling with singleton pattern
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from typing import Optional
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Singleton database connection pool manager for PostgreSQL"""
    
    _instance: Optional['DatabaseManager'] = None
    _connection_pool: Optional[pool.SimpleConnectionPool] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._connection_pool is None:
            self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool"""
        try:
            self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=20,
                dbname=os.getenv('DB_NAME', 'raven_cad'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                cursor_factory=RealDictCursor
            )
            logger.info(f"Database connection pool initialized: {os.getenv('DB_NAME')}")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        if self._connection_pool is None:
            raise RuntimeError("Connection pool not initialized")
        return self._connection_pool.getconn()
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        if self._connection_pool is None:
            raise RuntimeError("Connection pool not initialized")
        self._connection_pool.putconn(conn)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self._connection_pool is not None:
            self._connection_pool.closeall()
            logger.info("All database connections closed")
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            cur.close()
            self.return_connection(conn)
            logger.info(f"Database connection successful: {version}")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False


class DatabaseContext:
    """Context manager for database connections"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.conn = None
    
    def __enter__(self):
        self.conn = self.db_manager.get_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.db_manager.return_connection(self.conn)
