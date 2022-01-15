import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from flask import send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from blog import app
from blog.form import RegisterForm, LoginForm, PostForm
from blog.models import User, BlogPost


@app.route("/")
def home():
    user = current_user.username if current_user.is_authenticated else False
    posts = BlogPost.objects
    return render_template("home.html", username=user, posts=posts)


@app.route("/post/<string:id>")
def get_single_post(id):
    user = current_user.username if current_user.is_authenticated else False
    post = BlogPost.objects(id=id).first()
    return render_template("single.html", username=user, post=post, image=post.image_path)


@app.route("/post/delete/<string:id>")
@login_required
def post_delete(id):
    user = current_user.username if current_user.is_authenticated else False
    post = BlogPost.objects(id=id)
    if user == post[0].author:
        BlogPost.objects(id=id).delete()
        flash("Post Deleted Successfully", "success")
        return redirect(url_for("home"))
    return render_template("single.html", username=user, post=post[0])


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/profile")
@login_required
def profile():
    user = current_user.username if current_user.is_authenticated else False
    user_posts = None
    if user:
        user_posts = BlogPost.objects(author=current_user.username)
    return render_template("profile.html", username=user, user=current_user, posts=user_posts)


@app.route("/post", methods=["POST", "GET"])
@login_required
def post():
    form = PostForm()
    if request.method == "POST":
        if 'image' not in request.files:
            flash("there is no image in form!", "danger")
        else:
            image = request.files['image']
            file_name = image.filename
            # creating object save
            final = {
                "title": form.title.data,
                "description": form.description.data,
                "image_path": file_name,
                "category": form.category.data,
                "author": current_user.username,
                "created_at": datetime.now()
            }

            path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            image.save(path)
            BlogPost(**final).save()

            flash("Post Created successfully", "success")
    user = current_user.username if current_user.is_authenticated else False
    return render_template("post.html", username=user, form=form)


@app.route("/post/edit/<string:id>", methods=["POST", "GET"])
@login_required
def post_edit(id):
    post = BlogPost.objects(id=id).first()
    form = PostForm()
    form.title.data = post.title
    form.description.data = post.description
    form.category.data = post.category

    if request.method == "POST":
        if 'image' not in request.files:
            flash("there is no image in form!", "danger")
        else:
            image = request.files['image']
            file_name = image.filename
            # creating object save
            final = {
                "title": form.title.data,
                "description": form.description.data,
                "image_path": file_name,
                "category": form.category.data,
                "author": current_user.username,
                "created_at": datetime.now()
            }
            path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            image.save(path)

            post.update(**final)

            flash("Post Update successfully", "success")
    user = current_user.username if current_user.is_authenticated else False
    return render_template("post.html", username=user, form=form)


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
        existing_user = User.objects(email=form.email.data).first()
        check_username = User.objects(username=form.username.data).first()
        if existing_user is None and check_username is None:
            hashpass = generate_password_hash(form.password.data, method='sha256')
            final = {"email": form.email.data, "password": hashpass, "username": form.username.data,
                     "name": form.name.data}
            usr = User(**final).save()
            login_user(usr)
            flash(f"User {form.username.data} created successfully", "success")
            return redirect(url_for('home'))
        else:
            flash(f"User {form.username.data} exists. Please try login or another username", "warning")
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        # if form.validate():
        check_user = User.objects(email=form.email.data).first()
        check_username = User.objects(username=form.email.data).first()
        if check_user or check_username:
            to_use = check_user if check_user else check_username
            if check_password_hash(to_use['password'], form.password.data):
                login_user(to_use)
                return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    flash(f"{current_user.username} Logged out", "success")
    logout_user()
    return redirect(url_for('home'))
