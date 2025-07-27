from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Course, Student, Enrollment, Grade

course_bp = Blueprint('course', __name__)

@course_bp.route('/list')
def list_courses():
    search = request.args.get('search', '')
    semester = request.args.get('semester', '')
    
    # Build query
    query = Course.query.filter(Course.is_active == True)
    
    if search:
        query = query.filter(
            db.or_(
                Course.course_code.contains(search),
                Course.title.contains(search),
                Course.instructor.contains(search)
            )
        )
    
    if semester:
        query = query.filter(Course.semester == semester)
    
    courses = query.order_by(Course.course_code).all()
    
    # Get unique semesters for filter
    semesters = db.session.query(Course.semester).filter(Course.is_active == True).distinct().all()
    semesters = [s[0] for s in semesters]
    
    return render_template('course/list.html', 
                         courses=courses, 
                         search=search,
                         semester=semester,
                         semesters=semesters)

@course_bp.route('/detail/<int:course_id>')
def detail(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Get enrollment count
    enrollment_count = course.get_enrolled_count()
    
    # Check if current user is enrolled (if student)
    is_enrolled = False
    can_enroll = False
    
    if current_user.is_authenticated and not current_user.is_admin():
        student = current_user.student_profile
        if student:
            is_enrolled = course.is_student_enrolled(student.id)
            can_enroll = not is_enrolled and course.has_capacity()
    
    return render_template('course/detail.html', 
                         course=course,
                         enrollment_count=enrollment_count,
                         is_enrolled=is_enrolled,
                         can_enroll=can_enroll)
