from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
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
    category = SelectField('Kategoria', validators=[DataRequired()], choices=[('oddechowe'), ('mięśniowe'),
                                                                              ('mindfullness'), ('wizualizacje'),
                                                                              ('inne')])
    time = IntegerField('Czas trwania', validators=[DataRequired()])
    content = TextAreaField('Zawartość', validators=[DataRequired()])
    submit = SubmitField('Post')


class QuizForm(FlaskForm):
    q1 = SelectField('Ile czasu możesz poświęcić na praktykę?', validators=[DataRequired()],
                     choices=[('a', '3-5 minut dziennie'), ('b', 'około 30 minut'),
                              ('c', 'różnie'), ('d', '10 minut'), ])
    q2 = SelectField('Czego najbardziej potrzebujesz?', validators=[DataRequired()],
                     choices=[('a', 'ograniczyć lęk'), ('b', 'rozluźnić się'),
                              ('c', 'zregenerować umysł'), ('d', 'poprawić jakość snu'), ])
    q3 = SelectField('Czy jesteś systematyczny?', validators=[DataRequired()],
                     choices=[('a', 'Staram się, ale różnie bywa'), ('b', 'Raczej tak'),
                              ('c', 'Tak'), ('d', 'Raczej nie'), ])
    q4 = SelectField('Gdzie spędzasz więcej czasu?', validators=[DataRequired()],
                     choices=[('a', 'W pracy'), ('b', 'W domu'),
                              ('c', 'W pracy i w domu '), ('d', 'Dużo podróżuję, więc bywam w wielu miejscach'), ])
    q5 = SelectField('Jak często się relaksowałeś do tej pory?', validators=[DataRequired()],
                     choices=[('a', 'Prawie nigdy'), ('b', 'Czasami'),
                              ('c', 'systematycznie'), ('d', 'Nigdy'), ])
    q6 = SelectField('Jak wygląda twój czas wolny?', validators=[DataRequired()],
                     choices=[('a', 'Spędzam czas z rodziną'), ('b', 'Ćwiczę'),
                              ('c', 'Oglądam filmy/seriale'), ('d', 'Wyjeżdżam w ciekawe miejsce'), ])
    q7 = SelectField('Który opis najlepiej do ciebie pasuje?', validators=[DataRequired()],
                     choices=[('a', 'Jestem nerwowy, mam problem z uspokojeniem się. '),
                              ('b', 'Prowadzę siedzący tryb życia, dużo czasu spędzam przed komputerem.'),
                              ('c', 'Ma problem z koncentracją, nie mogę się skupić na wykonywanych czynnościach'),
                              ('d', 'To, co najbardziej mnie motywuje do pracy to goniące terminy'), ])
    q8 = SelectField('Które dolegliwości występują u ciebie najczęściej?', validators=[DataRequired()],
                     choices=[('a', 'Mam wysokie ciśnienie'), ('b', 'Bóle kręgosłupa, stawów'),
                              ('c', 'Bóle głowy'), ('d', 'Bezsenność'), ])
    q9 = SelectField('Czy jesteś otwarty na nowe doświadczenia?', validators=[DataRequired()],
                     choices=[('a', 'Raczej tak'), ('b', 'Raczej nie'),
                              ('c', 'Tak'), ('d', 'To zależy'), ])
    q10 = SelectField('Czy wiesz, że pozytywna zmiana wymaga regularnej pracy?', validators=[DataRequired()],
                      choices=[('a', 'Tak'), ('b', 'Raczej tak'),
                               ('c', 'Oczywiście, regularność to moje drugie imię'),
                               ('d', 'Postaram się być regularny'), ])


class FavForm(FlaskForm):
    submit = SubmitField('Ulubione')


class AddCommentForm(FlaskForm):
    body = StringField("Treść", validators=[DataRequired()])
    submit = SubmitField("Dodaj")