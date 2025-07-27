# Student Registration System

A comprehensive Flask web application for student registration, course management, and administrative functions with PostgreSQL database integration.

## Features

### For Students
- **Account Registration & Login**: Secure user authentication with role-based access
- **Course Browsing**: View available courses with detailed information
- **Course Enrollment**: Enroll in available courses with capacity tracking
- **Academic Dashboard**: View enrolled courses and academic progress
- **Grade Tracking**: Monitor grades and academic performance
- **Profile Management**: Update personal information and contact details

### For Administrators
- **Student Management**: View, edit, and manage student profiles
- **Course Management**: Create, edit, and manage course offerings
- **Enrollment Oversight**: Monitor course enrollments and capacity
- **Grade Management**: Input and manage student grades
- **Academic Analytics**: View enrollment statistics and academic metrics
- **System Administration**: Manage user accounts and system settings

## Technology Stack

### Backend
- **Flask**: Python web framework for server-side logic
- **SQLAlchemy**: Object-relational mapping for database operations
- **PostgreSQL**: Production-ready relational database
- **Flask-Login**: User session management and authentication
- **Werkzeug**: Password hashing and security utilities

### Frontend
- **Bootstrap 5**: Modern responsive UI framework with dark theme
- **Jinja2**: Server-side template rendering
- **Feather Icons**: Clean, minimalist icon library
- **Responsive Design**: Mobile-friendly interface

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- pip package manager

### Environment Variables
Set the following environment variables:
```bash
DATABASE_URL=postgresql://username:password@host:port/database
SESSION_SECRET=your-secret-key-here
```

### Installation Steps
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python init_data.py
   ```
4. Run the application:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## Database Schema

### Core Models
- **User**: Authentication and role management (student/admin)
- **Student**: Student profile and academic information
- **Course**: Course catalog and scheduling details
- **Enrollment**: Student-course relationships
- **Grade**: Academic performance tracking

### Key Relationships
- One-to-one: User ↔ Student
- Many-to-many: Student ↔ Course (through Enrollment)
- One-to-many: Student → Grade
- One-to-many: Course → Grade

## Default Accounts

The system comes with pre-configured accounts for testing:

**Administrator Account:**
- Username: `admin`
- Password: `admin123`
- Access: Full system administration

**Student Account:**
- Username: `student1`
- Password: `student123`
- Access: Student portal and course enrollment

## Project Structure

```
├── routes/                 # Route handlers
│   ├── admin.py           # Administrative functions
│   ├── auth.py            # Authentication routes
│   ├── course.py          # Course management
│   └── student.py         # Student portal
├── templates/             # Jinja2 templates
│   ├── admin/            # Admin interface templates
│   ├── auth/             # Login/registration forms
│   ├── course/           # Course browsing templates
│   └── student/          # Student dashboard templates
├── app.py                # Flask application factory
├── models.py             # Database models
├── utils.py              # Utility functions
├── main.py               # Application entry point
└── init_data.py          # Sample data initialization
```

## Usage

### Student Workflow
1. Register for a new account or login
2. Browse available courses in the catalog
3. Enroll in desired courses (subject to capacity)
4. View enrolled courses in the dashboard
5. Monitor grades and academic progress
6. Update profile information as needed

### Administrator Workflow
1. Login with administrator credentials
2. Manage student accounts and profiles
3. Create and configure course offerings
4. Monitor course enrollments and capacity
5. Input grades for enrolled students
6. View system-wide analytics and reports

## Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask-Login for secure user sessions
- **Role-Based Access**: Separate interfaces for students and administrators
- **CSRF Protection**: Built-in Flask security mechanisms
- **Input Validation**: Server-side validation for all forms

## API Endpoints

### Authentication
- `GET /login` - Login form
- `POST /login` - Process login
- `GET /register` - Registration form
- `POST /register` - Process registration
- `GET /logout` - User logout

### Student Portal
- `GET /student/dashboard` - Student dashboard
- `GET /student/courses` - Enrolled courses
- `GET /student/grades` - Academic grades
- `GET /student/profile` - Profile management

### Course Management
- `GET /courses` - Course catalog
- `GET /course/<id>` - Course details
- `POST /course/<id>/enroll` - Course enrollment

### Administration
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/students` - Student management
- `GET /admin/courses` - Course administration
- `POST /admin/course/create` - Create new course

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions about this application, please create an issue in the repository or contact the development team.