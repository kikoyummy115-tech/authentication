from extenstion import db
from .association import role_permissions

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, default='user')
    
    users = db.relationship('User', backref='role', lazy='dynamic')
    permissions = db.relationship('Permission', secondary=role_permissions, backref='roles', lazy='select')
    
    def __repr__(self):
        return f"<Role {self.name}>"
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions.append(perm)
    
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions.remove(perm)
        
    def reset_permissions(self):
        self.permissions = []

        
    def has_permission(self, perm):
        return perm in self.permissions