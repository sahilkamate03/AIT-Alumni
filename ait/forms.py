from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from firebase_admin import auth

from ait.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    role = RadioField('Role',choices=[('Student'),('Alumini')], validators=[InputRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

        if '@' in email.data:
            ait = email.data.split('@')[1]
        else: 
            raise ValidationError('Enter valid email.')
        if ait != 'aitpune.edu.in':
            raise ValidationError('Only @aitpune.edu.in email address allowed.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role',choices=[('Student'),('Alumini')], validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name = StringField('Username')
    about = StringField('About')
    address = StringField('Address')
    phone = StringField('Phone')
    twitter = StringField('Twitter')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    linkedin = StringField('LinkedIn')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Media', validators=[FileAllowed(['jpg', 'png','mp4','jpeg','svg','webp'])])
    submit = SubmitField('Post')