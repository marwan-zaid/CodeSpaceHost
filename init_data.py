"""
Initialize the database with sample data
"""
from app import app, db
from models import User, Student, Course, Enrollment, Grade, Instructor
from utils import generate_student_id
from datetime import datetime

def init_sample_data():
    with app.app_context():
        # Create tables
        db.create_all()

        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin_user = User()
            admin_user.username = 'admin'
            admin_user.email = 'admin@school.edu'
            admin_user.role = 'admin'
            admin_user.set_password('admin123')
            db.session.add(admin_user)

            # Create instructor user
            instructor_user = User()
            instructor_user.username = 'instructor1'
            instructor_user.email = 'instructor1@school.edu'
            instructor_user.role = 'instructor'
            instructor_user.set_password('instructor123')
            db.session.add(instructor_user)

        # Create sample student user
        student_user = User.query.filter_by(username='student1').first()
        if not student_user:
            student_user = User()
            student_user.username = 'student1'
            student_user.email = 'student1@school.edu'
            student_user.role = 'student'
            student_user.set_password('student123')
            db.session.add(student_user)
            db.session.flush()

            # Create student profile
            student = Student()
            student.user_id = student_user.id
            student.student_id = generate_student_id()
            student.first_name = 'John'
            student.last_name = 'Doe'
            student.phone = '555-123-4567'
            db.session.add(student)

        # Create sample courses
        if Course.query.count() == 0:
            
            # Create instructor profile
            instructor_profile = Instructor()
            instructor_profile.user_id=instructor_user.id
            instructor_profile.instructor_id='INST001'
            instructor_profile.first_name='Dr. Ahmed'
            instructor_profile.last_name='Al-Rashid'
            instructor_profile.department='Computer Science'
            instructor_profile.phone='+966501234567'
            instructor_profile.office='Building A, Room 301'
            db.session.add(instructor_profile)
            db.session.commit()

            courses = [
                {
                    'course_code': 'CS101',
                    'title': 'Introduction to Computer Science',
                    'description': 'Fundamentals of programming and computer science concepts.',
                    'credits': 3,
                    'instructor': 'Dr. Ahmed Al-Rashid',
                    'instructor_id': instructor_profile.id,
                    'instructor_name': 'Dr. Ahmed Al-Rashid',
                    'schedule': 'MWF 10:00-11:00 AM',
                    'room': 'Room 101',
                    'max_enrollment': 30,
                    'semester': 'Fall',
                    'year': 2024
                },
                {
                    'course_code': 'MATH201',
                    'title': 'Calculus II',
                    'description': 'Advanced calculus including integration techniques and series.',
                    'credits': 4,
                    'instructor': 'Prof. Johnson',
                    'schedule': 'TTH 2:00-3:30 PM',
                    'room': 'Room 203',
                    'max_enrollment': 25,
                    'semester': 'Fall',
                    'year': 2024
                },
                {
                    'course_code': 'ENG102',
                    'title': 'English Composition',
                    'description': 'Academic writing and research skills.',
                    'credits': 3,
                    'instructor': 'Dr. Wilson',
                    'schedule': 'MWF 1:00-2:00 PM',
                    'room': 'Room 150',
                    'max_enrollment': 20,
                    'semester': 'Spring',
                    'year': 2025
                }
            ]

            for course_data in courses:
                course = Course()
                for key, value in course_data.items():
                    setattr(course, key, value)
                db.session.add(course)

        db.session.commit()
        print("Sample data initialized successfully!")

if __name__ == '__main__':
    init_sample_data()