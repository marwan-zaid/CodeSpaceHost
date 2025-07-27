from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import User, Student, Course, Enrollment, Grade
from utils import generate_student_id
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_students = Student.query.count()
    total_courses = Course.query.filter_by(is_active=True).count()
    total_enrollments = Enrollment.query.filter_by(status='enrolled').count()
    
    # Recent registrations
    recent_students = Student.query.order_by(Student.enrollment_date.desc()).limit(5).all()
    
    # Popular courses
    popular_courses = db.session.query(
        Course, 
        db.func.count(Enrollment.id).label('enrollment_count')
    ).join(Enrollment).filter(
        Enrollment.status == 'enrolled',
        Course.is_active == True
    ).group_by(Course.id).order_by(
        db.desc('enrollment_count')
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments,
                         recent_students=recent_students,
                         popular_courses=popular_courses)

@admin_bp.route('/students')
@login_required
@admin_required
def students():
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    # Build query
    query = Student.query.join(User)
    
    if search:
        query = query.filter(
            db.or_(
                Student.student_id.contains(search),
                Student.first_name.contains(search),
                Student.last_name.contains(search),
                User.email.contains(search)
            )
        )
    
    if status:
        query = query.filter(Student.status == status)
    
    students = query.order_by(Student.enrollment_date.desc()).all()
    
    return render_template('admin/students.html', 
                         students=students,
                         search=search,
                         status=status)

@admin_bp.route('/students/<int:student_id>')
@login_required
@admin_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Get enrolled courses
    enrolled_courses = student.get_enrolled_courses()
    
    # Get grades
    grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.recorded_date.desc()).all()
    
    # Get GPA
    gpa = student.get_gpa()
    
    return render_template('admin/student_detail.html',
                         student=student,
                         enrolled_courses=enrolled_courses,
                         grades=grades,
                         gpa=gpa)

@admin_bp.route('/courses')
@login_required
@admin_required
def courses():
    search = request.args.get('search', '')
    semester = request.args.get('semester', '')
    
    # Build query
    query = Course.query
    
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
    semesters = db.session.query(Course.semester).distinct().all()
    semesters = [s[0] for s in semesters]
    
    return render_template('admin/courses.html', 
                         courses=courses,
                         search=search,
                         semester=semester,
                         semesters=semesters)

@admin_bp.route('/courses/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_course():
    if request.method == 'POST':
        try:
            course = Course(
                course_code=request.form.get('course_code'),
                title=request.form.get('title'),
                description=request.form.get('description'),
                credits=int(request.form.get('credits', 3)),
                instructor=request.form.get('instructor'),
                schedule=request.form.get('schedule'),
                room=request.form.get('room'),
                max_enrollment=int(request.form.get('max_enrollment', 30)),
                semester=request.form.get('semester'),
                year=int(request.form.get('year', datetime.now().year))
            )
            
            db.session.add(course)
            db.session.commit()
            
            flash(f'Course {course.course_code} created successfully!', 'success')
            return redirect(url_for('admin.courses'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the course.', 'danger')
    
    return render_template('admin/create_course.html')

@admin_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        try:
            course.title = request.form.get('title', course.title)
            course.description = request.form.get('description', course.description)
            course.credits = int(request.form.get('credits', course.credits))
            course.instructor = request.form.get('instructor', course.instructor)
            course.schedule = request.form.get('schedule', course.schedule)
            course.room = request.form.get('room', course.room)
            course.max_enrollment = int(request.form.get('max_enrollment', course.max_enrollment))
            course.semester = request.form.get('semester', course.semester)
            course.year = int(request.form.get('year', course.year))
            
            db.session.commit()
            
            flash(f'Course {course.course_code} updated successfully!', 'success')
            return redirect(url_for('admin.courses'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the course.', 'danger')
    
    return render_template('admin/edit_course.html', course=course)

@admin_bp.route('/courses/<int:course_id>/grades', methods=['GET', 'POST'])
@login_required
@admin_required
def course_grades(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Get enrolled students
    enrolled_students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == 'enrolled'
    ).all()
    
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id'))
            percentage = float(request.form.get('percentage'))
            assignment_type = request.form.get('assignment_type', 'final')
            comments = request.form.get('comments', '')
            
            # Check if grade already exists for this assignment type
            existing_grade = Grade.query.filter_by(
                student_id=student_id,
                course_id=course_id,
                assignment_type=assignment_type
            ).first()
            
            if existing_grade:
                # Update existing grade
                existing_grade.set_grade_from_percentage(percentage)
                existing_grade.comments = comments
                existing_grade.recorded_by = current_user.username
                existing_grade.recorded_date = datetime.utcnow()
            else:
                # Create new grade
                grade = Grade(
                    student_id=student_id,
                    course_id=course_id,
                    assignment_type=assignment_type,
                    comments=comments,
                    recorded_by=current_user.username
                )
                grade.set_grade_from_percentage(percentage)
                db.session.add(grade)
            
            db.session.commit()
            flash('Grade recorded successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while recording the grade.', 'danger')
    
    # Get grades for this course
    grades = Grade.query.filter_by(course_id=course_id).all()
    
    # Organize grades by student and assignment type
    student_grades = {}
    for grade in grades:
        if grade.student_id not in student_grades:
            student_grades[grade.student_id] = {}
        student_grades[grade.student_id][grade.assignment_type] = grade
    
    return render_template('admin/course_grades.html',
                         course=course,
                         enrolled_students=enrolled_students,
                         student_grades=student_grades)
