# Student Registration System

## Overview

This is a Flask-based student registration system that provides functionality for student course enrollment, grade management, and administrative oversight. The application uses a traditional MVC architecture with SQLAlchemy for database management and Flask-Login for authentication.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management
- **Template Engine**: Jinja2 (Flask's default)
- **Password Security**: Werkzeug's password hashing utilities

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme
- **Icons**: Feather Icons
- **Templates**: Server-side rendered Jinja2 templates
- **Responsive Design**: Bootstrap grid system for mobile compatibility

### Database Architecture
- **Default Database**: SQLite (configurable via environment variable)
- **Schema Design**: Relational model with proper foreign key relationships
- **Connection Management**: Built-in connection pooling and health checks

## Key Components

### Models (models.py)
- **User**: Handles authentication and user roles (student/admin)
- **Student**: Student profile information and academic data
- **Course**: Course catalog and scheduling information
- **Enrollment**: Student-course relationships
- **Grade**: Academic performance tracking

### Routes Structure
- **Authentication** (`routes/auth.py`): Login, logout, and registration
- **Student Portal** (`routes/student.py`): Student dashboard, profile, and course management
- **Admin Panel** (`routes/admin.py`): Administrative functions for managing students and courses
- **Course Catalog** (`routes/course.py`): Public course browsing and enrollment

### Utility Functions (utils.py)
- Student ID generation
- Date/time formatting helpers
- Validation functions for email and phone
- Academic semester and year options

## Data Flow

1. **User Registration**: New students create accounts through the registration form
2. **Authentication**: Users log in and are redirected based on their role (student/admin)
3. **Course Management**: Students browse courses and enroll; admins manage course offerings
4. **Grade Tracking**: Administrators input grades; students view their academic progress
5. **Profile Management**: Users can update their personal information

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: Authentication management
- Werkzeug: WSGI utilities and security functions

### Frontend Libraries (CDN)
- Bootstrap 5: UI framework with dark theme
- Feather Icons: Icon library

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Deployment Strategy

### Development Setup
- Uses SQLite database for local development
- Debug mode enabled in main.py
- Proxy fix middleware for deployment behind reverse proxies

### Production Considerations
- Environment-based configuration for database connections
- Session secret management via environment variables
- Connection pooling configured for database reliability
- WSGI-compatible for deployment with various servers

### Security Features
- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control (student/admin)
- CSRF protection through Flask's built-in mechanisms

## Missing Components

The application appears to be incomplete, with several blueprint imports missing from app.py and some model relationships (Course, Enrollment, Grade models) referenced but not fully defined in the provided models.py file. The system would need these components completed for full functionality.