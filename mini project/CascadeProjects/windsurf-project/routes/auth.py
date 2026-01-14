"""
Authentication routes for user registration, login, and logout
Handles all authentication-related functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.user import db, User
import re

# Create Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """
    Validate email format using regex
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, ""

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration
    GET: Display registration form
    POST: Process registration data
    """
    
    if request.method == 'GET':
        return render_template('register.html')
    
    # Handle POST request for registration
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Server-side validation
        errors = []
        
        # Username validation
        if not username:
            errors.append("Username is required")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(username) > 20:
            errors.append("Username must not exceed 20 characters")
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append("Username can only contain letters, numbers, and underscores")
        
        # Email validation
        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
            errors.append("Please enter a valid email address")
        
        # Password validation
        if not password:
            errors.append("Password is required")
        else:
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                errors.append(error_msg)
        
        # Confirm password validation
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            errors.append("Username already exists")
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append("Email already registered")
        
        # If there are errors, return them
        if errors:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'errors': errors}), 400
            else:
                for error in errors:
                    flash(error, 'error')
                return render_template('register.html', 
                                     username=username, 
                                     email=email)
        
        # Create new user
        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            success_message = "Registration successful! Please login to continue."
            
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': True, 'message': success_message})
            else:
                flash(success_message, 'success')
                return redirect(url_for('auth.login'))
                
        except Exception as e:
            db.session.rollback()
            error_message = "Registration failed. Please try again."
            
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'errors': [error_message]}), 500
            else:
                flash(error_message, 'error')
                return render_template('register.html', 
                                     username=username, 
                                     email=email)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login
    GET: Display login form
    POST: Process login credentials
    """
    
    # Redirect if user is already logged in
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    # Handle POST request for login
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', 'off') == 'on'
        
        # Server-side validation
        errors = []
        
        if not username:
            errors.append("Username or email is required")
        
        if not password:
            errors.append("Password is required")
        
        # If there are validation errors
        if errors:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'errors': errors}), 400
            else:
                for error in errors:
                    flash(error, 'error')
                return render_template('login.html', username=username)
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username.lower())
        ).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            error_message = "Invalid username/email or password"
            
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'errors': [error_message]}), 401
            else:
                flash(error_message, 'error')
                return render_template('login.html', username=username)
        
        # Check if user is active
        if not user.is_active:
            error_message = "Your account has been deactivated"
            
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'errors': [error_message]}), 403
            else:
                flash(error_message, 'error')
                return render_template('login.html', username=username)
        
        # Login successful - create session
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        
        # Set session permanence based on remember checkbox
        session.permanent = remember
        
        # Update last login time
        user.update_last_login()
        
        success_message = f"Welcome back, {user.username}!"
        
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({
                'success': True, 
                'message': success_message,
                'redirect': url_for('main.dashboard')
            })
        else:
            flash(success_message, 'success')
            return redirect(url_for('main.dashboard'))

@auth_bp.route('/logout')
def logout():
    """
    Handle user logout
    Clears the session and redirects to login page
    """
    
    # Clear session data
    session.clear()
    
    flash("You have been logged out successfully", 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/check-username')
def check_username():
    """
    Check if username is available (AJAX endpoint)
    
    Query Parameters:
        username (str): Username to check
        
    Returns:
        JSON: Availability status
    """
    
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({'available': False, 'message': 'Username is required'})
    
    if len(username) < 3:
        return jsonify({'available': False, 'message': 'Username must be at least 3 characters'})
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'available': False, 'message': 'Invalid username format'})
    
    # Check if username exists
    user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify({'available': False, 'message': 'Username already taken'})
    else:
        return jsonify({'available': True, 'message': 'Username is available'})

@auth_bp.route('/check-email')
def check_email():
    """
    Check if email is available (AJAX endpoint)
    
    Query Parameters:
        email (str): Email to check
        
    Returns:
        JSON: Availability status
    """
    
    email = request.args.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'available': False, 'message': 'Email is required'})
    
    if not validate_email(email):
        return jsonify({'available': False, 'message': 'Invalid email format'})
    
    # Check if email exists
    user = User.query.filter_by(email=email).first()
    
    if user:
        return jsonify({'available': False, 'message': 'Email already registered'})
    else:
        return jsonify({'available': True, 'message': 'Email is available'})
