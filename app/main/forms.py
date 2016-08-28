from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
    SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User
from flask.ext.pagedown.fields import PageDownField


class PostForm(Form):
    body = PageDownField('What on your mind?', validators=[Required()])
    submit = SubmitField('Post')


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('comment')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(1, 64)])
    location = StringField('Location', validators=[Length(1, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('Submit')


class EditAdminstratorProfileForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                        Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                  'Usernames must have only letters, '
                                  'numbers, dots or underscores')])
    confirm = BooleanField('Confirmed')
    Role = SelectField('Role', core=int)
    name = StringField('Real name', validators=[Length(1, 64)])
    location = StringField('Location', validators=[Length(1, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('Submit')

    def __init__(self, user, *agrs, **kwagrs):
        super(EditAdminstratorProfileForm, self).__init__(*agrs, **kwagrs)
        self.user = user
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]

        def validate_email(self, field):
            if field.data != self.user.email and \
                    User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered.')

        def validate_username(self, field):
            if field.data != self.user.username and \
                    User.query.filter_by(email=field.data).first():
                raise ValidationError('Username already in user')
