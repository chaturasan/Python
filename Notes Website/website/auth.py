from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .validations import *;
from .models import User
from . import db


signup_schema = Schema({
    'email': And(str, Use(str.lower), lambda s: '@' in s),  
    'first_name': And(str, lambda s: len(s) >= 3),          
    'password': And(str, lambda s: len(s) >= 5),    
    'password_confirm': And(str, Use(str.lower))
})

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = dict()
        data['email'] = request.form.get('email')
        data['password'] = request.form.get('password')

        _, err = validate_login_data(data)
        if err:
            flash(err, category="error")
            return render_template("login.html")
        
        user = User.query.filter_by(email=data['email']).first()
        if user:
            if check_password_hash(user.password, data['password']):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist.', category='error')
            
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = dict()
        data['email'] = request.form.get('email')
        data['first_name'] = request.form.get('firstName')
        data['password'] = request.form.get('password')
        data['password_confirm'] = request.form.get('password_confirm')
        _, err = validate_signup_data(data)
        if err:
            flash(err, category="error")
            return render_template("signup.html")
        
        user = User.query.filter_by(email=data['email']).first()
         
        if user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=data['email'], first_name=data['first_name'], password=generate_password_hash(
                data['password']))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)