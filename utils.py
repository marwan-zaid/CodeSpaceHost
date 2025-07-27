import string
import random
from datetime import datetime

def generate_student_id():
    """Generate a unique student ID in format: YYYYNNNN"""
    year = datetime.now().year
    # Generate 4 random digits
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"{year}{random_part}"

def format_date(date_obj):
    """Format date object to readable string"""
    if date_obj:
        return date_obj.strftime('%B %d, %Y')
    return 'Not set'

def format_datetime(datetime_obj):
    """Format datetime object to readable string"""
    if datetime_obj:
        return datetime_obj.strftime('%B %d, %Y at %I:%M %p')
    return 'Not set'

def calculate_age(birth_date):
    """Calculate age from birth date"""
    if birth_date:
        today = datetime.now().date()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return None

def get_semester_options():
    """Get list of semester options"""
    return ['Fall', 'Spring', 'Summer']

def get_year_options():
    """Get list of year options (current year and next 2 years)"""
    current_year = datetime.now().year
    return [current_year + i for i in range(3)]

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Basic phone number validation"""
    import re
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's 10 digits (US format)
    return len(digits_only) == 10

def format_phone(phone):
    """Format phone number to (XXX) XXX-XXXX"""
    import re
    digits_only = re.sub(r'\D', '', phone)
    if len(digits_only) == 10:
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    return phone

def get_grade_description(grade_letter):
    """Get description for grade letter"""
    descriptions = {
        'A': 'Excellent',
        'B': 'Good',
        'C': 'Satisfactory',
        'D': 'Poor',
        'F': 'Failing'
    }
    return descriptions.get(grade_letter, 'Unknown')

def get_status_badge_class(status):
    """Get Bootstrap badge class for status"""
    classes = {
        'active': 'bg-success',
        'inactive': 'bg-warning',
        'graduated': 'bg-info',
        'enrolled': 'bg-primary',
        'dropped': 'bg-secondary',
        'completed': 'bg-success'
    }
    return classes.get(status, 'bg-light')
