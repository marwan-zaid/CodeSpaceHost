from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import User, Student, Course, Enrollment, Grade
from datetime import datetime

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student_profile
    if not student:
        flash('Student profile not found. Please contact an administrator.', 'danger')
        return redirect(url_for('index'))
    
    # Get enrolled courses
    enrolled_courses = student.get_enrolled_courses()
    
    # Get recent grades
    recent_grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.recorded_date.desc()).limit(5).all()
    
    # Calculate GPA
    gpa = student.get_gpa()
    
    return render_template('student/dashboard.html', 
                         student=student, 
                         enrolled_courses=enrolled_courses,
                         recent_grades=recent_grades,
                         gpa=gpa)

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student_profile
    if not student:
        flash('Student profile not found. Please contact an administrator.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # Update profile information
            student.first_name = request.form.get('first_name', student.first_name)
            student.last_name = request.form.get('last_name', student.last_name)
            student.phone = request.form.get('phone', student.phone)
            student.address = request.form.get('address', student.address)
            
            # Update user email if provided
            new_email = request.form.get('email')
            if new_email and new_email != current_user.email:
                # Check if email is already taken
                existing_user = db.session.query(db.exists().where(
                    db.and_(User.email == new_email, User.id != current_user.id)
                )).scalar()
                
                if existing_user:
                    flash('Email already in use by another account.', 'danger')
                    return render_template('student/profile.html', student=student)
                
                current_user.email = new_email
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'danger')
    
    return render_template('student/profile.html', student=student)

@student_bp.route('/courses')
@login_required
def courses():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student_profile
    if not student:
        flash('Student profile not found. Please contact an administrator.', 'danger')
        return redirect(url_for('index'))
    
    # Get enrolled courses
    enrolled_courses = student.get_enrolled_courses()
    
    # Get available courses (not enrolled in)
    enrolled_course_ids = [course.id for course in enrolled_courses]
    available_courses = Course.query.filter(
        ~Course.id.in_(enrolled_course_ids),
        Course.is_active == True
    ).all()
    
    return render_template('student/courses.html', 
                         student=student,
                         enrolled_courses=enrolled_courses,
                         available_courses=available_courses)

@student_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll_course(course_id):
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student_profile
    if not student:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('student.courses'))
    
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        student_id=student.id, 
        course_id=course.id,
        status='enrolled'
    ).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course.', 'warning')
        return redirect(url_for('student.courses'))
    
    # Check course capacity
    if not course.has_capacity():
        flash('This course is full. Please try again later.', 'warning')
        return redirect(url_for('student.courses'))
    
    try:
        # Create enrollment
        enrollment = Enrollment(student_id=student.id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()
        
        flash(f'Successfully enrolled in {course.title}!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during enrollment. Please try again.', 'danger')
    
    return redirect(url_for('student.courses'))

@student_bp.route('/drop/<int:course_id>', methods=['POST'])
@login_required
def drop_course(course_id):
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student_profile
    if not student:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('student.courses'))
    
    enrollment = Enrollment.query.filter_by(
        student_id=student.id, 
        course_id=course_id,
        status='enrolled'
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'warning')
        return redirect(url_for('student.courses'))
    
    try:
        enrollment.status = 'dropped'
        db.session.commit()
        
        flash(f'Successfully dropped {enrollment.course.title}.', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while dropping the course. Please try again.', 'danger')
    
    return redirect(url_for('student.courses'))

@student_bp.route('/grades')
@login_required
def grades():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student_profile
    if not student:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get all grades organized by course
    grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.recorded_date.desc()).all()
    
    # Group grades by course
    grades_by_course = {}
    for grade in grades:
        course_id = grade.course_id
        if course_id not in grades_by_course:
            grades_by_course[course_id] = {
                'course': grade.course,
                'grades': []
            }
        grades_by_course[course_id]['grades'].append(grade)
    
    gpa = student.get_gpa()
    
    return render_template('student/grades.html', 
                         student=student,
                         grades_by_course=grades_by_course,
                         gpa=gpa)
