from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from models.User import User
from flask_login import login_user, login_required, logout_user, current_user
from utils import db
from utils.db import db

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.')
            return redirect(url_for('users.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito.')
        return redirect(url_for('users.login'))
    return render_template('register.html')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('efectivos.home'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template('login.html')

@users.route('/logout')
def logout():
    logout_user()
    flash('Sesión cerrada.')
    return redirect(url_for('users.login'))