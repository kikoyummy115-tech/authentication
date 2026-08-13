import cloudinary
from flask import Flask
from config import config
from extension import db, login_manager, migrate, mail
from app.models import User, Role, Permission


login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])

    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET'],
        secure=True
    )

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.routes import auth, main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)

    
    return app
