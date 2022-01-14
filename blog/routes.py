from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from blog import app
from blog.form import RegisterForm, LoginForm
from blog.models import User


@app.route("/")
@login_required
def home():
    return render_template("home.html", name=current_user.username)


@app.errorhandler(500)
def internal_error(e):
    print(e)
    return render_template('500.html'), 404


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        print("is post")
        existing_user = User.objects(email=form.email.data).first()
        if existing_user is None:
            print('1212121')
            hashpass = generate_password_hash(form.password.data, method='sha256')
            final = {"email": form.email.data, "password": hashpass}
            hey = User(**final).save()
            login_user(hey)
            return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        # if form.validate():
        check_user = User.objects(email=form.email.data).first()
        if check_user:
            if check_password_hash(check_user['password'], form.password.data):
                login_user(check_user)
                return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
