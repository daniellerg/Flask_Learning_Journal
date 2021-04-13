from flask_wtf import Form
from wtforms import (StringField, PasswordField, DateTimeField, 
                    DateField, IntegerField, TextAreaField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

import models
import datetime


def name_exists(form, field):
    if (models.User.select().where(
        models.User.username == field.data).exists()):
        raise ValidationError('User already exists by that name.')


def email_exists(form, field):
    if models.User.select().where(models.User.email == field.data).exists():
        raise ValidationError('User already exists with that email.')


class RegisterForm(Form):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Regexp(r'^[a-zA-Z0-9_]+$',
            message=("Username should be one word, letters,"
                    "numbers, and underscores only")
                    ),
            name_exists
            ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
            ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4),
            EqualTo('password2', message='Passwords must match.')
            ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()]
            )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EntryForm(Form):
    title = StringField('Title of Entry', validators=[DataRequired()])
    entry_date = DateField('mm/dd/yyyy', 
                        format='%m/%d/%Y', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent-Minutes', 
                            validators=[DataRequired()])
    learned = TextAreaField('Things Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources to Remember', 
                            validators=[DataRequired()])
