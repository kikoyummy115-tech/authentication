from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user
from extension import db
from app.models.user import User

from app.utils import otp_verification
import random

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    "Login in user required username and password"

    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # Add login logic here
        user = User.query.filter_by(email=email).first()
        
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
    "Register a new user and otp verify"
    
    if request.method == 'POST':
        # Handle registration logic here
        username = request.form.get('username').strip() 
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # You would typically add validation and user creation logic here
        if not username or not email or not password:
            flash('Please fill out all fields', 'danger')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already Exist', 'danger')
            return redirect(url_for('auth.register'))
        
        # 1. Generate 6- Digital OTP
        otp = random.randint(100000, 999999)
        
        # 2. Store user registration info and OTP temporarily in flask session
        session['register_user'] = {
            'username': username,
            'email': email,
            'password': password
        }
        
        session['register_otp'] = otp
        
        # 3. Send OTP by function
        try:
            otp_verification(email=email, otp=otp)
            flash('A 6 digit verification code has been sent to your email.', 'info')
            return redirect(url_for('auth.verify_otp'))
        except Exception as e:
            session.pop('register_user', None)
            session.pop('register_otp', None)
            flash('Failed to send verification email. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
        
    return render_template('auth/register.html')


@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    "Verify the 6 digit OTP and instantly log the user in"
    
    if "register_user" not in session or 'register_otp' not in session:
        flash('Please register first.', 'warning')
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        user_otp = request.form.get('otp', '').strip()
        
        print(user_otp)
        # Create and save the new user to Database
        if user_otp and int(user_otp) == session.get('register_otp'): 
            user_date = session.get('register_user')           
            
            # Create and save the new user Database
            
            new_user = User(username=user_date['username'], email=user_date['email']) 
            new_user.password = user_date['password']
            new_user.role_id = 1
        
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)

            # Clear temporary session storage
            session.pop('register_user', None)
            session.pop('register_otp', None)
            
            flash('Registration successful and email verify!', 'success')            
            return redirect(url_for('main.dashboard'))
        else:
            flash('invalid verification code. Please try again.', 'danger')
        
    return render_template('auth/verify_otp.html')
        
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()
        # Anti-enumeration measure: Always flash success to hide valid vs invalid emails
        flash('If the email exists, a password reset link has been dispatched.', 'info')
        if user:
            pass
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')

@auth.route('/logout')
def logout():    
    logout_user()
    flash("Successfully logout account", 'success')
    return redirect(url_for('auth.login'))