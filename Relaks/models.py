from Relaks import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # function that get user id
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    fav = db.relationship('Favourite', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    time = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fav = db.relationship('Favourite', backref='fav', lazy=True)

    def __repr__(self):
        return f"Post('{self.name}', '{self.category}', '{self.time}')"


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Favourite('{self.id}')"


