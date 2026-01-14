"""
Main Flask application for User Registration and Login System
This is the entry point of the application
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models.user import db, User
from config.config import config
import os
from datetime import timedelta

def create_app(config_name='default'):
    """
    Application factory function to create and configure the Flask app
    
    Args:
        config_name (str): Configuration name ('development', 'production', 'default')
        
    Returns:
        Flask: Configured Flask application instance
    """
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Configure session timeout (30 minutes)
    app.permanent_session_lifetime = timedelta(minutes=30)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Import and register routes
    from routes.auth import auth_bp
    from routes.main import main_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
