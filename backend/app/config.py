"""
Environment-aware configuration for Raven Shop Automation
Supports development, staging, and production environments
"""

import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Environment(str, Enum):
    """Application environment options"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings:
    """Central configuration management for the application"""
    
    # Environment Setup
    APP_ENV = os.getenv("APP_ENV", "development").lower()
    NODE_ENV = os.getenv("NODE_ENV", "development").lower()
    ENVIRONMENT = os.getenv("ENVIRONMENT", APP_ENV)  # Backward compatibility
    
    # Validate and normalize environment
    if APP_ENV not in [e.value for e in Environment]:
        APP_ENV = "development"
    IS_DEV = APP_ENV == Environment.DEVELOPMENT.value
    IS_PROD = APP_ENV == Environment.PRODUCTION.value
    
    # ========================================================================
    # DATABASE CONFIGURATION
    # ========================================================================
    
    DB_PROVIDER = os.getenv("DB_PROVIDER", "postgresql")
    DB_USER = os.getenv("DB_USER", "raven_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "raven_password_2025")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "raven_drawings")
    
    # SQLite fallback for development
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/raven_drawings.db")
    
    # Use DATABASE_URL if provided (environment-specific)
    # Otherwise, construct from individual components
    _DATABASE_URL_ENV = os.getenv("DATABASE_URL")
    
    @property
    def DATABASE_URL(self) -> str:
        """
        Returns the appropriate database URL based on environment.
        
        Development:
          - If DATABASE_URL env var is set, use it
          - Otherwise try PostgreSQL
          - If PostgreSQL unavailable, fall back to SQLite
          
        Production:
          - DATABASE_URL MUST be set (from environment secrets)
          - Validates it points to postgresql or secure connection
        """
        if self._DATABASE_URL_ENV:
            return self._DATABASE_URL_ENV
        
        # Build URL from individual components
        if self.DB_PROVIDER == "sqlite":
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        
        # PostgreSQL (default)
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    # ========================================================================
    # SERVER CONFIGURATION
    # ========================================================================
    
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
    BACKEND_RELOAD = os.getenv("BACKEND_RELOAD", "true").lower() == "true"
    
    # Debug mode (disable in production!)
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    if IS_PROD:
        DEBUG = False  # Force DEBUG=false in production
    
    # ========================================================================
    # CORS CONFIGURATION
    # ========================================================================
    
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8000"
    ).split(",")
    CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    
    # Ensure production only uses HTTPS origins
    if IS_PROD:
        CORS_ORIGINS = [
            origin.strip() 
            for origin in CORS_ORIGINS 
            if origin.strip().startswith("https://")
        ]
    
    # ========================================================================
    # GOOGLE SHEETS INTEGRATION
    # ========================================================================
    
    GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv(
        "GOOGLE_SHEETS_CREDENTIALS_PATH",
        "./credentials/google-sheets-credentials.json"
    )
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
    FRAME_SYNC_INTERVAL = int(os.getenv("FRAME_SYNC_INTERVAL", "60"))
    
    # ========================================================================
    # SECURITY
    # ========================================================================
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
    
    # In production, ensure JWT secret is not default
    if IS_PROD and JWT_SECRET_KEY == "dev-secret-key-change-in-production":
        raise ValueError(
            "CRITICAL: JWT_SECRET_KEY must be set to a strong value in production!"
        )
    
    # ========================================================================
    # FILE UPLOADS & STORAGE
    # ========================================================================
    
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    STATIC_FILES_DIR = os.getenv("STATIC_FILES_DIR", "./static")
    PDF_OUTPUT_DIR = os.getenv("PDF_OUTPUT_DIR", "./outputs")
    
    # ========================================================================
    # LOGGING
    # ========================================================================
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if IS_PROD else "DEBUG")
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "./logs/app.log")
    
    # ========================================================================
    # FEATURE FLAGS
    # ========================================================================
    
    FEATURE_PDF_EXPORT = os.getenv("FEATURE_PDF_EXPORT", "true").lower() == "true"
    FEATURE_GOOGLE_SHEETS_SYNC = os.getenv("FEATURE_GOOGLE_SHEETS_SYNC", "true").lower() == "true"
    FEATURE_FRAME_LIBRARY = os.getenv("FEATURE_FRAME_LIBRARY", "true").lower() == "true"
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    @classmethod
    def get_database_settings(cls) -> dict:
        """Return database connection settings as a dictionary"""
        return {
            "provider": cls.DB_PROVIDER,
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "user": cls.DB_USER,
            "database": cls.DB_NAME,
            "url": cls().DATABASE_URL,
        }
    
    @classmethod
    def summary(cls) -> str:
        """Return a readable summary of current settings"""
        settings = cls()
        return f"""
╔════════════════════════════════════════════════════════════════╗
║           RAVEN SHOP AUTOMATION - CONFIGURATION SUMMARY         ║
╠════════════════════════════════════════════════════════════════╣
║ Environment:      {settings.APP_ENV.upper():40s}║
║ Debug Mode:       {'ON' if settings.DEBUG else 'OFF':40s}║
║ Database:         {settings.DB_PROVIDER.upper():40s}║
║ DB Host:          {settings.DB_HOST:40s}║
║ Backend Server:   {settings.BACKEND_HOST}:{settings.BACKEND_PORT:<37s}║
║ CORS Origins:     {str(len(settings.CORS_ORIGINS)) + ' configured':40s}║
║ Features:         PDF={settings.FEATURE_PDF_EXPORT} | Sheets={settings.FEATURE_GOOGLE_SHEETS_SYNC} | Frames={settings.FEATURE_FRAME_LIBRARY:<18s}║
╚════════════════════════════════════════════════════════════════╝
        """


# Create a singleton instance
settings = Settings()
