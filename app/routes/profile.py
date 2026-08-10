from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user

from app.decorator import permission_required

from app.routes import main

@main.route('/profile')
@login_required
def profile():
    "View the profile page for the current user."
    
    return render_template('views/profile.html')