from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from FileManager.auth import auth
from FileManager.auth.forms import LoginForm
from FileManager.models import User
import bcrypt

@auth.route('/', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('file_manager.dashboard'))
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('file_manager.dashboard'))
            else:
                flash('Credenciales incorrectas. Por favor, vuelvalo a intentar', 'danger')
        return render_template('login.html', form=form)
    except Exception as e:
        flash('Error en la autenticación', 'danger')
        print(e)
        return render_template('login.html')
        

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
