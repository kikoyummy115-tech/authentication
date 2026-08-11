from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from extension import db

from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    "Login in user required username and password"

    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # Add login logic here
        user = User.query.filter_by(email=email).first()
        
        print(user.verify_password(password))
        if user and user.verify_password(password):
            # Log the user in (you would typically use Flask-Login here)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    "Register a new user"
    
    if request.method == 'POST':
        # Handle registration logic here
        username = request.form.get('username').strip() 
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # You would typically add validation and user creation logic here
        if not username or not email or not password:
            flash('Please fill out all fields', 'danger')
            return render_template('auth/register.html')
        
        user = User(username=username, email=email)
        user.password = password  # This will hash the password
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')





@auth.route('/logout')
def logout():    
    logout_user()  # This will log the user out
    return redirect(url_for('auth.login'))