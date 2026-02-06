from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from app.config import settings

load_dotenv()

# Use environment-aware configuration
# DATABASE_URL can be overridden via environment variables
DATABASE_URL = settings.DATABASE_URL

# Render.com uses postgres:// but SQLAlchemy 2.x requires postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with appropriate settings based on environment
if "postgresql" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10 if settings.IS_PROD else 5,
        max_overflow=20 if settings.IS_PROD else 10,
        pool_pre_ping=True,  # Verify connections before using
        echo=settings.DEBUG  # SQL logging in debug mode
    )
elif "sqlite" in DATABASE_URL:
    # SQLite for development without PostgreSQL
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
else:
    # Fallback for unknown providers
    engine = create_engine(DATABASE_URL, echo=settings.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

