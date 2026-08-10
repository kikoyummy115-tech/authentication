from extenstion import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # e.g., 'write_post', 'delete_user'
    
    
    def _repr__(self):
        return f"<Permission {self.name}>"