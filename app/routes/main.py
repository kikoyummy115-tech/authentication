from flask import Blueprint, render_template
from flask_login import login_required

from app.decorator import permission_required

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    "Display the user's dashboard"
    return render_template('dashboard.html')

@main.route('/settings')
@login_required
def settings():
    "Display the user's settings"
    return "Settings Page"


@main.route('/admin')
@login_required
@permission_required(['admin', 'superuser'])
def admin():
    "Display the admin panel"
    return "Admin Page"