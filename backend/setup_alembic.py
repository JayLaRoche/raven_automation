#!/usr/bin/env python3
"""
Setup Alembic for Database Migrations
Initializes Alembic and creates initial migration
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("ALEMBIC DATABASE MIGRATIONS SETUP")
print("=" * 70)
print()

print("[Step 1] Initializing Alembic")
print("-" * 70)

# Initialize Alembic
os.system('alembic init alembic')

print("\n[Step 2] Configuring alembic.ini")
print("-" * 70)

# Update alembic.ini with PostgreSQL URL
alembic_ini = Path('alembic.ini')
if alembic_ini.exists():
    content = alembic_ini.read_text()
    
    # Replace sqlalchemy.url
    db_url = os.getenv('DATABASE_URL', 'postgresql://raven_user:raven_password_2025@localhost:5432/raven_drawings')
    content = content.replace(
        'sqlalchemy.url = driver://user:pass@localhost/dbname',
        f'sqlalchemy.url = {db_url}'
    )
    
    alembic_ini.write_text(content)
    print("✓ Updated sqlalchemy.url in alembic.ini")
else:
    print("⚠️  alembic.ini not found")

print("\n[Step 3] Configuring env.py")
print("-" * 70)

env_py = Path('alembic/env.py')
if env_py.exists():
    # Update env.py to use our models
    env_content = """from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import your models
from app.database import Base
from app.models import Project, Window, Door

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata from your models
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""
    env_py.write_text(env_content)
    print("✓ Updated env.py with model imports")

print("\n[Step 4] Creating Initial Migration")
print("-" * 70)

# Create initial migration
os.system('alembic revision --autogenerate -m "Initial schema with reference tables"')

print("\n" + "=" * 70)
print("ALEMBIC SETUP COMPLETE")
print("=" * 70)
print()
print("Next steps:")
print()
print("1. Review the generated migration:")
print("   alembic/versions/*.py")
print()
print("2. Apply the migration:")
print("   alembic upgrade head")
print()
print("3. Create new migrations when models change:")
print("   alembic revision --autogenerate -m 'Description of changes'")
print()
print("4. Rollback migrations:")
print("   alembic downgrade -1")
print()
print("5. View migration history:")
print("   alembic history")
print()
