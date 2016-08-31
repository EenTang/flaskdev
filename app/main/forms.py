from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
    SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField
from flask import request, make_response, url_for, current_app
import os, datetime, random


class CKEditor(object):
    def __init__(self):
        pass

    def gen_rnd_filename(self):
        """generate a random filename"""
        filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))

    def upload(self, endpoint=current_app):
        """img or file upload methods"""
        error = ''
        url = ''
        callback = request.args.get("CKEditorFuncNum")

        if request.method == 'POST' and 'upload' in request.files:
            # /static/upload
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            rnd_name = '%s%s' % (self.gen_rnd_filename(), fext)

            filepath = os.path.join(endpoint.static_folder, 'upload', rnd_name)

            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                    error = 'ERROR_DIR_NOT_WRITEABLE'
            if not error:
                fileobj.save(filepath)
                url = url_for('main.static', filename='%s/%s' % ('upload', rnd_name))
        else:
            error = 'post error'

        res = """
                <script type="text/javascript">
                window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
                </script>
             """ % (callback, url, error)

        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response


class PostForm(Form, CKEditor):
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
