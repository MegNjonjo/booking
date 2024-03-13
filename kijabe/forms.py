from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from kijabe.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please use a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please use a different one')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class DoctorForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class AppointmentForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    description = TextAreaField('Description',
                             validators=[DataRequired()])
    date = DateField('Date',
                             validators=[DataRequired()])
    submit = SubmitField('Book Appointment')


    def validate_date(self, date):
        if date.data <= datetime.now().date():
            raise ValidationError('Please choose a future date.')


class AdminForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class DoctorRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    department = StringField('Department',
                           validators=[DataRequired()])
    contact = StringField('Contact',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Sign Up')



