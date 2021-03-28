import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Relaks import app, db, bcrypt
from Relaks.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from Relaks.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.category).paginate(page=page, per_page=5)
    return render_template('home.html', post=post)


@app.route("/stres")
def stres():
    return render_template('stres.html', title='Stres')


@app.route("/dobor")
def dobor():
    return render_template('dobor.html', title='Dobór')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/photo', picture_fn)

    # speed up the page because of smaller size
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='photo/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/harmonogram")
@login_required
def harmonogram():
    return render_template('harmonogram.html', title='Harmonogram')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Twoje konto zostało utworzone! Teraz możesz się zalogować.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Błąd logowania. Sprawdź czy email i hasło są poprawne', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/oddechowe", methods=['GET', 'POST'])
@login_required
def oddech():
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter(
        Post.category == 'oddechowe').paginate(page=page, per_page=5)


    return render_template('oddech.html', title='Oddechowe',  post=post)


@app.route("/miesnie", methods=['GET', 'POST'])
@login_required
def miesnie():
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter(
        Post.category == 'mięśniowe').paginate(page=page, per_page=5)

    return render_template('miesnie.html', title='Mięśnie', post=post)


@app.route("/mindfullness", methods=['GET', 'POST'])
@login_required
def mindfullness():
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter(
        Post.category == 'mindfullness').paginate(page=page, per_page=5)

    return render_template('mindfullness.html', title='Mindfullness', post=post)


@app.route("/wizualizacje", methods=['GET', 'POST'])
@login_required
def wizualizacje():
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter(
        Post.category == 'wizualizacje').paginate(page=page, per_page=5)

    return render_template('wizualizacje.html', title='Wizualizacje', post=post)


@app.route("/inne", methods=['GET', 'POST'])
@login_required
def inne():
    page = request.args.get('page', 1, type=int)

    post = Post.query.filter(
        Post.category == 'inne').paginate(page=page, per_page=5)
    return render_template('inne.html', title='Inne', post=post)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.name, post=post)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(name=form.name.data, category=form.category.data, time=form.time.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Twój post został stworzony!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Nowe ćwiczenie', form=form)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.name = form.name.data
        post.category = form.category.data
        post.time = form.time.data
        post.content = form.content.data
        db.session.commit()
        flash("Twój post został edytowany", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.name.data = post.name
        form.category.data = post.category
        form.time.data = post.time
        form.content.data = post.content
    return render_template('update.html', title=update_post, post=post, form=form, legend='Edytuj post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Twój post został usunięty ', 'success')
    return redirect(url_for('home'))


@app.route("/category/<category>")
def category_posts(category):
    page = request.args.get('page', 1, type=int)
    category = Post.category.query.filter_by(category.category).first_or_404()
    post = Post.query.filter_by(category) \
        .order_by(Post.category) \
        .paginate(page=page, per_page=5)
    return render_template('category_posts.html', post=post, category=category)
