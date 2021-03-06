# -*-coding: utf-8-*-
from . import main
from flask import render_template, url_for, redirect, flash, abort, request, \
    current_app, make_response
from .forms import PostForm, EditProfileForm, EditAdminstratorProfileForm, \
    CommentForm
from ..models import User, db, Role, Post, Permission, Comment
from flask_login import current_user, login_required
from ..decorators import adminstrator_required, permission_required
from flask_sqlalchemy import get_debug_queries


@main.route('/', methods=['GET', 'POST'])
def index():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           show_followed=show_followed, pagination=pagination)

@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    form = PostForm()
    response = form.upload(endpoint=main)
    return response

@main.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit() and \
            current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        flash('Your blog have been posted')
        return redirect(url_for('.index'))
    return render_template('edit_post.html', form=form)



@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment have been published')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    # 为什么要设置posts=[post]?
    return render_template('post.html', comments=comments, posts=[post],
                           form=form, pagination=pagination)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


# 传入page 确保更改后还在原来的page
@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disable = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                    page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable():
    comment = Comment.query.get_or_404(id)
    comment.disable = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                    page=request.args.get('page', 1, type=int)))


@main.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINSTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('Your post have been update!')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit_profile', methods=['Get', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        flash('Your profile have been update')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/ediit_profile/<int:id>', methods=['Get', 'POST'])
@login_required
@adminstrator_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditAdminstratorProfileForm(user)
    if form.validate_on_submit():
        user.role = Role.query.get(form.role.data)
        user.email = form.email.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me
        user.username = form.username.data
        user.confirm = form.confirm.data
        db.session.add(user)
        flash('The profile has been updated')
        return redirect(url_for('.user', username=user.username))
    form.role.data = user.role_id
    form.email.data = user.email
    form.name.data = user.name
    form.location.data = user.location
    form.about_me = user.about_me
    form.username = user.username
    form.name = user.name
    form.confirm = user.confirm
    return render_template('edit_profile.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid username')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You have already following this user')
        return redirect(url_for('.index'))
    current_user.follow(user)
    flash('You are now following %s' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid username')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You have not following this user yet')
        return redirect(url_for('.index'))
    current_user.unfollow(user)
    flash('You are not following %s anymore' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid username')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u'的关注者',
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid username')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u'关注的人',
                           endpoint='.followed', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


# 在request之后对数据库查询的时间进行比较，低于设定时间则会提示，从而知道哪一块数据库可以优化
# 传入response，只为了得到数据库查询时间，但是不会对response进行加工
@main.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %f\nContext: %s\n' %
                (query.statement, query.parameters, query.duration,
                 query.context))
    return response
