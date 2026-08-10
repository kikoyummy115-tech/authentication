from flask import Flask
from config import config
from extension import db, login_manager, migrate
from app.models import User, Role, Permission

login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth
    from app.routes.main import main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    
    return app