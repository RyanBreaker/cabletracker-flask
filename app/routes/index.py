from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm
from app.models.user import User
from app.models.tracking import Room


@app.route('/')
def index():
    rooms = Room.query.all()
    return render_template('index.html', title='Home', rooms=rooms)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))
