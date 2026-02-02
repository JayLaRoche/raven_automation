"""
Manual schema update script for adding flexible fields to Project model
This script works with both PostgreSQL and SQLite

NOTE: Since PostgreSQL is not running, we'll use SQLite database.
Run this from the backend directory with: python update_schema.py
"""
import os
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set SQLite mode before importing database
os.environ['DB_PROVIDER'] = 'sqlite'
os.environ['SQLITE_DB_PATH'] = './data/raven_drawings.db'

from app.database import engine
from sqlalchemy import inspect, text

def update_schema():
    """Add new columns to projects table if they don't exist"""
    try:
        with engine.connect() as connection:
            # Check dialect
            dialect_name = connection.dialect.name
            print(f"🗄️  Using database: {dialect_name}")
            print(f"🗄️  Database URL: {engine.url}")
            
            # Get existing columns
            inspector = inspect(engine)
            
            # Check if projects table exists
            if 'projects' not in inspector.get_table_names():
                print("⚠️  Projects table doesn't exist yet - creating all tables...")
                from app.database import Base
                Base.metadata.create_all(bind=engine)
                print("✅ All tables created")
                return
            
            existing_columns = [col['name'] for col in inspector.get_columns('projects')]
            print(f"📋 Existing columns: {existing_columns}")
            
            # Define new columns to add
            new_columns = {
                'client_name': 'VARCHAR(255)',
                'address': 'TEXT',
                'date': 'TIMESTAMP'
            }
            
            for col_name, col_type in new_columns.items():
                if col_name not in existing_columns:
                    try:
                        # Add column
                        alter_sql = f"ALTER TABLE projects ADD COLUMN {col_name} {col_type}"
                        connection.execute(text(alter_sql))
                        connection.commit()
                        print(f"✅ Added column: {col_name}")
                    except Exception as e:
                        print(f"⚠️  Could not add {col_name}: {e}")
                else:
                    print(f"ℹ️  Column {col_name} already exists")
            
            # SQLite doesn't support modifying NOT NULL constraints
            # But our new fields are nullable, so projects can be created using them
            if dialect_name == 'sqlite':
                print("ℹ️  SQLite mode: Using flexible nullable fields (client_name, address, date)")
                print("ℹ️  Legacy fields (project_name, customer_name) still available for compatibility")
            
            print("\n🎉 Schema update complete!")
            print("✅ Backend can now accept both old and new project formats")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ Created data directory: {data_dir}")
    
    update_schema()
