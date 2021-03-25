from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Relaks.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa uzytkownika',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ta nazwa jest zajęta. Wybierz inną.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten email jest zajęty. Wybierz inny')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Zmień zdjęcie profilowe', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Zmień')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ta nazwa jest zajęta. Wybierz inną.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ten email jest zajęty. Wybierz inny')


class PostForm(FlaskForm):
    name = StringField('Tytuł', validators=[DataRequired()])
    category = StringField('Kategoria', validators=[DataRequired()])
    time = IntegerField('Czas trwania', validators=[DataRequired()])
    content = TextAreaField('Zawartość', validators=[DataRequired()])
    submit = SubmitField('Post')