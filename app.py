import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# 1. Initialize extensions without an app
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# 2. Create the Application Factory function
def create_app(**kwargs):
    app = Flask(__name__)

    # 3. Configure the app from environment variables
    # This is the secret to making it work on Render
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a-strong-dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        logging.error("DATABASE_URL environment variable not set.")
        raise ValueError("DATABASE_URL environment variable not set.")
        
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Apply ProxyFix for deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # 4. Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # 5. Import models and blueprints inside the factory
    from models import User
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.course import course_bp
    from routes.admin import admin_bp
    from routes.instructor import instructor_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(course_bp, url_prefix='/course')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(instructor_bp, url_prefix='/instructor')

    # Define the user_loader inside the factory
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Main route
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    # 6. Create database tables within the app context
    with app.app_context():
        db.create_all()
        logging.info("Database tables created or already exist.")

    return app

# 7. (Optional but recommended) Create a run.py for local development
# You don't need to upload this file to GitHub, it's just for you.
# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
