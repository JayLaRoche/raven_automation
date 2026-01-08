#!/usr/bin/env python3
"""
Raven Shop Drawing - Desktop Application Entry Point
Main application launcher for PyQt6 CAD drawing generator
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Application entry point"""
    
    # Set high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Raven Shop Drawing")
    app.setOrganizationName("Raven Custom Glass")
    app.setOrganizationDomain("ravencustomglass.com")
    
    try:
        # Import here to catch database connection errors
        from src.database.connection import DatabaseManager
        from src.ui.main_window import MainWindow
        
        # Initialize database connection
        db_manager = DatabaseManager()
        
        # Test connection
        try:
            conn = db_manager.get_connection()
            db_manager.return_connection(conn)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Database Connection Error",
                f"Failed to connect to PostgreSQL database:\n\n{str(e)}\n\n"
                "Please check your .env configuration and ensure PostgreSQL is running."
            )
            return 1
        
        # Create and show main window
        window = MainWindow(db_manager)
        window.show()
        
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "Application Error",
            f"Failed to start application:\n\n{str(e)}"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())
