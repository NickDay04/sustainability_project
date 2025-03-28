# -*- coding: utf-8 -*-
"""
    users/forms.py
    ~~~~~~~~~~~~~~

    Outlines website forms for use in user actions.

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo


# Emails start with 1 or more characters, require a '@.' , then ends in characters
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter an email"),
        Email(message="Please enter a valid email."),
        Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
               message="Invalid email address. ")
    ])

    password = PasswordField(validators=[DataRequired(message="Please enter a password")])
    submit = SubmitField()


# Emails start with 1 or more characters, require a '@.' , then ends in characters
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter an email"),
        Email(message="Please enter a valid email."),
        Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
               message="Invalid email address. ")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password"),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{6,12}$',
               message='Password must be 6-12 characters long, include uppercase and lowercase letters, a number, '
                       'and a special character.')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords don't match")
    ])

    firstname = StringField('First Name', validators=[
        DataRequired(message="Please enter your first name"),
        Regexp(r"^[^*?!\'^+%&/()=}]{2,}$", message='Invalid characters in first name.')
    ])

    lastname = StringField('Last Name', validators=[
        DataRequired(message="Please enter your last name"),
        Regexp(r"^[^*?!\'^+%&/()=}]{2,}$", message="Invalid characters in last name.")

    ])

    # Username starts with  a letter, contains only letters and numbers, is at least 5 characters long
    username = StringField('Username', validators=[
        DataRequired(message="Please enter your username"),
        Regexp(r'^[a-zA-Z][a-zA-Z0-9]{4,}$', message="Invalid username.")
    ])
    submit = SubmitField()


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField(validators=[DataRequired(message="Please enter your old password")])

    newPassword = PasswordField(validators=[DataRequired(message="Please enter your new password"),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{6,12}$',
               message='Password must be 6-12 characters long, include uppercase and lowercase letters, a number, '
                       'and a special character.')])

    confirmNewPassword = PasswordField(validators=[DataRequired(message="Please confirm your new password"),
        EqualTo('newPassword', message="Passwords don't match")])
    submit = SubmitField()


class ChangeUsernameForm(FlaskForm):
    newUsername = StringField(validators=[DataRequired(message="Please enter your new username")])
    confirmNewUsername = StringField(validators=[DataRequired(message="Please confirm your new Username"),
        EqualTo('newUsername', message="Usernames must match")])
    submit = SubmitField()


class deleteAccountForm(FlaskForm):
    Username = StringField(validators=[DataRequired(message="Please enter your username")])
    Password = PasswordField(validators=[DataRequired(message="Please enter your password"), ])
    submit = SubmitField()


class Verify2FA(FlaskForm):
    code = StringField(validators=[DataRequired()])
    submit = SubmitField()


class DeleteAccountAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Delete Account')


class ChangePrivacySettingsForm(FlaskForm):
    submit = SubmitField()


