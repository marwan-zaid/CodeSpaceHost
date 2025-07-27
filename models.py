from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student', 'admin', or 'instructor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_active = db.Column(db.Boolean, default=True)
    
    # Relationship to student profile
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_active(self):
        return self.user_active
    
    def __repr__(self):
        return f'<User {self.username}>'

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    office = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship to user
    user = db.relationship('User', backref=db.backref('instructor_profile', uselist=False))
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_courses(self):
        return Course.query.filter_by(instructor_name=self.full_name, is_active=True).all()
    
    def __repr__(self):
        return f'<Instructor {self.instructor_id}: {self.full_name}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # 'active', 'inactive', 'graduated'
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', cascade="all, delete-orphan")
    grades = db.relationship('Grade', backref='student', cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_enrolled_courses(self):
        return [enrollment.course for enrollment in self.enrollments if enrollment.status == 'enrolled']
    
    def get_gpa(self):
        grades = [grade.grade_points for grade in self.grades if grade.grade_points is not None]
        if not grades:
            return 0.0
        return sum(grades) / len(grades)
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.full_name}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False, default=3)
    instructor = db.Column(db.String(100))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=True)
    instructor_name = db.Column(db.String(100))  # For backward compatibility
    schedule = db.Column(db.String(200))  # e.g., "MWF 10:00-11:00"
    room = db.Column(db.String(50))
    max_enrollment = db.Column(db.Integer, default=30)
    semester = db.Column(db.String(20), nullable=False)  # e.g., "Fall 2024"
    year = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', cascade="all, delete-orphan")
    grades = db.relationship('Grade', backref='course', cascade="all, delete-orphan")
    
    def get_enrolled_count(self):
        return len([e for e in self.enrollments if e.status == 'enrolled'])
    
    def has_capacity(self):
        return self.get_enrolled_count() < self.max_enrollment
    
    def is_student_enrolled(self, student_id):
        return any(e.student_id == student_id and e.status == 'enrolled' for e in self.enrollments)
    
    def __repr__(self):
        return f'<Course {self.course_code}: {self.title}>'

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled')  # 'enrolled', 'dropped', 'completed'
    
    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)
    
    def __repr__(self):
        return f'<Enrollment {self.student.full_name} in {self.course.course_code}>'

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade_letter = db.Column(db.String(2))  # A, B, C, D, F
    grade_points = db.Column(db.Float)  # 4.0 scale
    percentage = db.Column(db.Float)  # 0-100
    assignment_type = db.Column(db.String(50), default='final')  # 'midterm', 'final', 'assignment', etc.
    recorded_date = db.Column(db.DateTime, default=datetime.utcnow)
    recorded_by = db.Column(db.String(100))  # Instructor name
    comments = db.Column(db.Text)
    
    def set_grade_from_percentage(self, percentage):
        """Convert percentage to letter grade and grade points"""
        self.percentage = percentage
        if percentage >= 90:
            self.grade_letter = 'A'
            self.grade_points = 4.0
        elif percentage >= 80:
            self.grade_letter = 'B'
            self.grade_points = 3.0
        elif percentage >= 70:
            self.grade_letter = 'C'
            self.grade_points = 2.0
        elif percentage >= 60:
            self.grade_letter = 'D'
            self.grade_points = 1.0
        else:
            self.grade_letter = 'F'
            self.grade_points = 0.0
    
    def __repr__(self):
        return f'<Grade {self.student.full_name} - {self.course.course_code}: {self.grade_letter}>'
