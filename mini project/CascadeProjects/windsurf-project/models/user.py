"""
User model for the User Registration and Login System
Defines the database schema for user authentication
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """
    User model class representing the users table in the database
    Stores user authentication information and profile data
    """
    
    __tablename__ = 'users'
    
    # Primary key for the user table
    id = db.Column(db.Integer, primary_key=True)
    
    # User information fields
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # User status
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, username, email, password):
        """
        Initialize a new user instance
        
        Args:
            username (str): Unique username for the user
            email (str): Unique email address for the user
            password (str): Plain text password (will be hashed)
        """
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """
        Hash and set the user's password
        
        Args:
            password (str): Plain text password to hash
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify if the provided password matches the stored hash
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update the last_login timestamp to current time"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """
        Convert user object to dictionary representation
        
        Returns:
            dict: User data without sensitive information
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        """String representation of the User object"""
        return f'<User {self.username}>'

def create_tables():
    """Create all database tables defined in the models"""
    db.create_all()

def init_db():
    """Initialize the database with tables"""
    from config.config import Config
    from flask import Flask
    
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        create_tables()
