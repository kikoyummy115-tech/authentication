from extension import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import timezone, datetime


from .permission import Permission

class User(UserMixin ,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    img_url = db.Column(db.String(256), default=None)
    
    gender = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True) 
    
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
     
    def has_permission(self, perm):
        if self.role is None:
            return False
        return self.role.has_permission(perm)
    
    def is_online(self):
        if self.last_seen is None:
            return False
        current_time = datetime.now(timezone.utc)
        time_difference = (current_time - self.last_seen.replace(tzinfo=timezone.utc)).total_seconds()
        return time_difference < 300  

    
    def __repr__(self):
        return f"<User {self.username}>"


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))