from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

import models


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User already exists by that name.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
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
            Length(min=5),
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