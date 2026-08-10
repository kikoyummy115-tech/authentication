from flask import Blueprint, render_template, redirect, url_for, flash, request

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    "Login in user required username and password"
    
    return "Login Page"


@auth.route('/register')
def register():
    "Register a new user"
    
    return "Register Page"


@auth.route('/logout')
def logout():    
    
    
    return "Logout Page"


