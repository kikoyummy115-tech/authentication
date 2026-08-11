from functools import wraps
from flask import request, abort
from app.models import User

def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Mock Auth: Extracting user from query string for demonstration
            # In production, use: current_user from flask_login
            email = request.args.get('user')
            current_user = User.query.filter_by(email=email).first()
            
            if not current_user:
                abort(401, description="Authentication required.")
                
            if not current_user.has_permission(permission_name):
                abort(403, description="You do not have permission to access this resource.")
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
