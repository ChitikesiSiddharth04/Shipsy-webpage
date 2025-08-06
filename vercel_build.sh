#!/bin/bash
# Vercel build script for ML Experiments Tracker

echo "--- Starting Vercel Build ---"

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p /tmp/vercel

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize the database
echo "Initializing database..."
python -c "
import os
from models import DatabaseManager, User, Experiment

# Initialize database
db = DatabaseManager()

# Create default admin user if it doesn't exist
user_model = User(db)
if not user_model.get_user_by_username('admin'):
    user_model.create_user('admin', 'password123')
    print('Default admin user created: admin/password123')
"

echo "--- Vercel Build Completed ---"
