"""
Vercel Serverless Function Entry Point
This file is the entry point for Vercel's serverless functions.
"""
import os
import sys
import logging

# Add the parent directory to the path so we can import app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app import app as application
    
    # Test the database connection on startup
    @application.before_first_request
    def init_database():
        try:
            from models import db_manager
            conn = db_manager.get_connection()
            conn.execute('SELECT 1')
            logger.info("Database connection test successful")
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            raise
    
    logger.info("Application initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize application: {str(e)}")
    raise
