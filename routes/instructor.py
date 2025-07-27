
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import User, Student, Course, Enrollment, Grade, Instructor

instructor_bp = Blueprint('instructor', __name__)

def instructor_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_instructor():
            flash('Access denied. Instructor privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@instructor_bp.route('/dashboard')
@login_required
@instructor_required
def dashboard():
    # Get instructor profile
    instructor = current_user.instructor_profile
    if not instructor:
        flash('Instructor profile not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get instructor's courses
    courses = Course.query.filter(
        db.or_(
            Course.instructor_name == instructor.full_name,
            Course.instructor_id == instructor.id
        ),
        Course.is_active == True
    ).all()
    
    # Get total enrollments across all courses
    total_enrollments = 0
    for course in courses:
        total_enrollments += course.get_enrolled_count()
    
    # Get recent enrollments
    recent_enrollments = []
    for course in courses:
        course_enrollments = Enrollment.query.filter_by(
            course_id=course.id, 
            status='enrolled'
        ).order_by(Enrollment.enrollment_date.desc()).limit(5).all()
        recent_enrollments.extend(course_enrollments)
    
    # Sort by enrollment date and limit to 10
    recent_enrollments = sorted(recent_enrollments, 
                               key=lambda x: x.enrollment_date, 
                               reverse=True)[:10]
    
    return render_template('instructor/dashboard.html',
                         instructor=instructor,
                         courses=courses,
                         total_courses=len(courses),
                         total_enrollments=total_enrollments,
                         recent_enrollments=recent_enrollments)

@instructor_bp.route('/courses')
@login_required
@instructor_required
def courses():
    instructor = current_user.instructor_profile
    if not instructor:
        flash('Instructor profile not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get instructor's courses
    courses = Course.query.filter(
        db.or_(
            Course.instructor_name == instructor.full_name,
            Course.instructor_id == instructor.id
        ),
        Course.is_active == True
    ).order_by(Course.course_code).all()
    
    return render_template('instructor/courses.html', 
                         instructor=instructor,
                         courses=courses)

@instructor_bp.route('/course/<int:course_id>/students')
@login_required
@instructor_required
def course_students(course_id):
    instructor = current_user.instructor_profile
    if not instructor:
        flash('Instructor profile not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get the course and verify instructor access
    course = Course.query.get_or_404(course_id)
    
    if (course.instructor_name != instructor.full_name and 
        course.instructor_id != instructor.id):
        flash('Access denied. You can only view your own courses.', 'danger')
        return redirect(url_for('instructor.courses'))
    
    # Get enrolled students
    enrolled_students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == 'enrolled'
    ).order_by(Student.last_name, Student.first_name).all()
    
    # Get grades for this course
    grades = Grade.query.filter_by(course_id=course_id).all()
    student_grades = {}
    for grade in grades:
        if grade.student_id not in student_grades:
            student_grades[grade.student_id] = []
        student_grades[grade.student_id].append(grade)
    
    return render_template('instructor/course_students.html',
                         course=course,
                         enrolled_students=enrolled_students,
                         student_grades=student_grades)

@instructor_bp.route('/students')
@login_required
@instructor_required
def all_students():
    instructor = current_user.instructor_profile
    if not instructor:
        flash('Instructor profile not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get all students enrolled in instructor's courses
    instructor_courses = Course.query.filter(
        db.or_(
            Course.instructor_name == instructor.full_name,
            Course.instructor_id == instructor.id
        ),
        Course.is_active == True
    ).all()
    
    course_ids = [course.id for course in instructor_courses]
    
    students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.course_id.in_(course_ids),
        Enrollment.status == 'enrolled'
    ).distinct().order_by(Student.last_name, Student.first_name).all()
    
    # Get enrollment info for each student
    student_enrollments = {}
    for student in students:
        student_courses = []
        for course in instructor_courses:
            enrollment = Enrollment.query.filter_by(
                student_id=student.id,
                course_id=course.id,
                status='enrolled'
            ).first()
            if enrollment:
                student_courses.append(course)
        student_enrollments[student.id] = student_courses
    
    return render_template('instructor/students.html',
                         instructor=instructor,
                         students=students,
                         student_enrollments=student_enrollments,
                         instructor_courses=instructor_courses)
