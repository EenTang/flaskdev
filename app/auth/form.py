# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, \
    ValidationError
from wtforms.validators import Required, Regexp, Email, Length, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField("Email", validators=[Required(),
                        Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required()])
    rememberme = BooleanField("Keep me logged in")
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField("Email", validators=[Required(),
                        Length(1, 64), Email()])
    username = StringField("Username", validators=[Required(), Length(1, 64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                  'Usernames must have only letters, '
                                  'numbers, dots or underscores')])
    password = PasswordField("Password", validators=[Required(),
                             EqualTo('password2',
                             message="Password must match!")])
    password2 = PasswordField("Password", validators=[Required()])
    submit = SubmitField('Register')

    # Required 可以保存和checkdata是否符合，所以可以调用。
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


class ChangePasswordForm(Form):
    oldpassword = PasswordField("Old Password", validators=[Required()])
    newpassword = PasswordField("New Password", validators=[Required(),
                                EqualTo('newpassword2',
                                message="Password must match!")])
    newpassword2 = PasswordField("New Password Confirm",
                                 validators=[Required()])
    submit = SubmitField('Change Password')


class ChangeEmailForm(Form):
    email = StringField("New Email", validators=[Required(),
                        Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField('Change Email')


class PasswordResetRequestForm(Form):
    email = StringField("Email", validators=[Required(),
                        Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField("Email", validators=[Required(),
                        Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required(),
                             EqualTo('password2',
                             message="Password must match!")])
    password2 = PasswordField("Password Confirm", validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):  # 这个确认邮箱是怎么调用出来确认的？
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Email already registered.')
