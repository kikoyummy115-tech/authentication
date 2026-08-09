from extenstion import db
from .association import role_permissions

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    
    users = db.relationship('User', backref='role', lazy='dynamic')
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))
    
    def __repr__(self):
        return f"<Role {self.name}>"
    
    def add_permission(self, perm):
        pass 
    
    def remove_permission(self, perm):
        pass
    
    def reset_permissions(self):
        pass
    
    def has_permission(self, perm):
        pass
