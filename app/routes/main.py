from flask import Blueprint
from flask_login import login_required
from app.decorator import permissions_required


main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    "Display the user's dashboard"
    return "Hello, World!"


@main.route('/settings')
@login_required
def settings():
    "Display the user's settings"
    return "Settings Page"


@main.route('/admin')
@login_required
@permissions_required('admin')
def admin():
    "Display the admin panel"
    return "Admin Page"