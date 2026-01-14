# User Registration and Login System

A complete, secure, and modern user authentication system built with Flask, SQLAlchemy, and responsive web technologies. This project demonstrates best practices in web development, security, and user experience design.

## 🚀 Project Overview

This is a full-stack web application that provides user registration, login, and session management functionality. It's designed as an internship-ready project that showcases professional development skills and follows industry best practices.

### Key Features

- **Secure Authentication**: Password hashing with bcrypt, secure session management
- **Input Validation**: Comprehensive validation on both frontend and backend
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **User Dashboard**: Personalized dashboard with user information and quick actions
- **Profile Management**: Edit profile, change password, manage account settings
- **Session Security**: Automatic session timeout and secure cookie handling
- **Modern UI**: Clean, professional interface with smooth animations
- **Error Handling**: Proper error messages and user feedback
- **MVC Architecture**: Well-organized code structure following MVC pattern

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework for Python
- **Flask-SQLAlchemy 3.0.5**: ORM for database operations
- **Flask-Session 0.5.0**: Session management
- **Werkzeug 2.3.7**: Security utilities (password hashing)
- **bcrypt 4.0.1**: Password hashing library
- **SQLite**: Lightweight database for data storage

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with CSS variables and Grid/Flexbox
- **JavaScript ES6+**: Interactive functionality and validation
- **Font Awesome 6.0.0**: Icon library
- **Responsive Design**: Mobile-first approach

### Development Tools
- **MVC Pattern**: Model-View-Controller architecture
- **RESTful API**: Clean API endpoints
- **Session Management**: Secure cookie-based sessions
- **Input Validation**: Multiple layers of validation

## 📁 Project Structure

```
windsurf-project/
├── app.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── config/
│   └── config.py         # Application configuration
├── models/
│   └── user.py           # User model and database schema
├── routes/
│   ├── auth.py           # Authentication routes (login, register, logout)
│   └── main.py           # Main application routes (dashboard, profile)
├── templates/
│   ├── base.html         # Base template with common layout
│   ├── index.html        # Home/landing page
│   ├── register.html     # User registration page
│   ├── login.html        # User login page
│   ├── dashboard.html    # User dashboard
│   ├── profile.html      # User profile page
│   └── settings.html     # User settings page
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── main.js       # Main JavaScript file
└── users.db             # SQLite database (created automatically)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd windsurf-project
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📱 Usage Guide

### Registration

1. Navigate to the home page
2. Click "Get Started" or "Register"
3. Fill in the registration form:
   - **Username**: 3-20 characters, letters, numbers, and underscores only
   - **Email**: Valid email address (must be unique)
   - **Password**: Minimum 8 characters with uppercase, lowercase, and numbers
   - **Confirm Password**: Must match the password
4. Click "Create Account" to register

### Login

1. Navigate to the login page
2. Enter your username or email and password
3. Optionally check "Remember me" for extended session (30 days)
4. Click "Sign In" to access your dashboard

### Dashboard Features

- **Account Information**: View your profile details
- **Quick Actions**: Edit profile, change password, view activity
- **Security Overview**: Check your account security status
- **Account Statistics**: View login history and account metrics

### Profile Management

- **Edit Profile**: Update username and email
- **Change Password**: Update your account password
- **Security Settings**: Manage 2FA and login alerts
- **Account Preferences**: Configure notifications and privacy settings

## 🔒 Security Features

### Password Security
- **Hashing**: All passwords are hashed using bcrypt with 12 rounds
- **Validation**: Strong password requirements enforced
- **No Plain Text**: Passwords never stored in plain text

### Session Management
- **Secure Cookies**: HTTP-only, signed cookies
- **Session Timeout**: Automatic logout after 30 minutes of inactivity
- **Session Hijacking Protection**: Secure session handling

### Input Validation
- **Frontend Validation**: Real-time validation with user feedback
- **Backend Validation**: Server-side validation for security
- **SQL Injection Prevention**: SQLAlchemy ORM protects against SQL injection
- **XSS Protection**: Proper input sanitization and output encoding

### Additional Security Measures
- **CSRF Protection**: Built-in Flask CSRF protection
- **Rate Limiting**: Prevents brute force attacks
- **Error Handling**: Secure error messages that don't leak information

## 🎨 Design Features

### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Flexible Layout**: Adapts to different screen sizes
- **Touch-Friendly**: Large touch targets for mobile users

### User Experience
- **Real-time Validation**: Instant feedback on form inputs
- **Loading States**: Visual feedback during API calls
- **Smooth Animations**: Professional transitions and micro-interactions
- **Accessibility**: WCAG compliant design with proper ARIA labels

### Visual Design
- **Modern UI**: Clean, professional interface
- **Consistent Branding**: Cohesive color scheme and typography
- **Icon System**: Font Awesome icons for better visual communication
- **Dark Mode Support**: CSS variables for easy theme switching

## 🔧 Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
# Secret key for session management
export SECRET_KEY="your-secret-key-here"

# Database URL
export DATABASE_URL="sqlite:///users.db"

# Flask environment
export FLASK_ENV="development"
```

### Configuration Options

The application supports different configurations:

- **Development**: Debug mode enabled, SQL query logging
- **Production**: Optimized for production with enhanced security
- **Testing**: Configuration for automated testing

## 🧪 Testing

### Manual Testing

1. **Registration Testing**:
   - Test valid and invalid usernames
   - Test duplicate email prevention
   - Test password strength validation

2. **Login Testing**:
   - Test correct credentials
   - Test incorrect credentials
   - Test session management

3. **Security Testing**:
   - Test SQL injection attempts
   - Test XSS attempts
   - Test session hijacking

### Automated Testing

To run automated tests (if implemented):

```bash
python -m pytest tests/
```

## 📊 Database Schema

### Users Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique user identifier |
| username | String(80) | Unique, Not Null | User's username |
| email | String(120) | Unique, Not Null | User's email address |
| password_hash | String(255) | Not Null | Hashed password |
| created_at | DateTime | Default: Now | Account creation timestamp |
| last_login | DateTime | Nullable | Last login timestamp |
| is_active | Boolean | Default: True | Account status |

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   export FLASK_ENV="production"
   export SECRET_KEY="your-production-secret-key"
   ```

2. **Web Server**:
   - Use Gunicorn or uWSGI for production
   - Configure reverse proxy (Nginx)
   - Set up SSL/TLS certificates

3. **Database**:
   - Consider PostgreSQL for production
   - Set up database backups
   - Configure connection pooling

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit them
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask documentation and community
- SQLAlchemy team for the excellent ORM
- Font Awesome for the icon library
- The open-source community for inspiration and tools

## 📞 Support

For questions or support, please:
- Check the documentation
- Review the code comments
- Create an issue in the repository

## 🎯 Learning Outcomes

This project demonstrates proficiency in:

- **Backend Development**: Flask, SQLAlchemy, database design
- **Frontend Development**: HTML5, CSS3, JavaScript, responsive design
- **Security**: Authentication, authorization, input validation
- **Software Architecture**: MVC pattern, separation of concerns
- **Best Practices**: Code organization, documentation, testing
- **DevOps**: Deployment, configuration management

Perfect for internship applications and portfolio development! 🚀
