"""
Main routes for the application
Handles dashboard, home page, and other general routes
"""

from flask import Blueprint, render_template, redirect, url_for, session, flash
from functools import wraps

# Create Blueprint for main routes
main_bp = Blueprint('main', __name__)

def login_required(f):
    """
    Decorator to require login for accessing routes
    
    Args:
        f (function): Route function to protect
        
    Returns:
        function: Wrapped function that checks for login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    """
    Home page route
    Displays welcome page with login/register options
    """
    
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard route for authenticated users
    Displays user information and available actions
    """
    
    # Get user information from session
    user_info = {
        'username': session.get('username'),
        'email': session.get('email'),
        'user_id': session.get('user_id')
    }
    
    return render_template('dashboard.html', user=user_info)

@main_bp.route('/profile')
@login_required
def profile():
    """
    User profile page
    Displays detailed user information
    """
    
    from models.user import User
    
    # Get full user information from database
    user = User.query.get(session.get('user_id'))
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    return render_template('profile.html', user=user)

@main_bp.route('/settings')
@login_required
def settings():
    """
    User settings page
    Allows users to manage their account settings
    """
    
    return render_template('settings.html')

@main_bp.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors
    
    Args:
        error: Error object
        
    Returns:
        Rendered 404 page
    """
    
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server errors
    
    Args:
        error: Error object
        
    Returns:
        Rendered 500 page
    """
    
    from models.user import db
    db.session.rollback()
    
    return render_template('errors/500.html'), 500

@main_bp.errorhandler(403)
def forbidden_error(error):
    """
    Handle 403 Forbidden errors
    
    Args:
        error: Error object
        
    Returns:
        Rendered 403 page
    """
    
    return render_template('errors/403.html'), 403
