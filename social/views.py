from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required
from sqlalchemy import or_, and_, desc

from extensions import db
from models import Post, User, Friendships, Likes, Comments
from social.forms import CreatePostForm, CreateCommentForm
from better_profanity import profanity

social_blueprint = Blueprint('social', __name__, template_folder='templates')


@social_blueprint.route('/social/feed')
@login_required
def feed():
    user_likes = Likes.query.filter(Likes.user_id == current_user.id).all()
    list_of_liked_posts = []

    for i in range(0, len(user_likes)):
        list_of_liked_posts.append(int(user_likes[i].post_id))

    if request.args.get("add_like"):
        post_id = int(request.args.get("add_like"))

        # Check if the post has already been liked by the current user
        existing_like = Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()

        if existing_like is None and post_id not in list_of_liked_posts:
            # Like does not exist, add a new like
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post.likes_count += 1
                new_like = Likes(user_id=current_user.id, post_id=post_id)
                db.session.add(new_like)
                db.session.commit()
        elif existing_like:
            # Like exists, remove the like
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post.likes_count -= 1
                db.session.delete(existing_like)
                db.session.commit()

    posts = Post.query.filter(or_(and_(Post.user_id == Friendships.friend_id, Friendships.user_id == current_user.id), Post.user_id == current_user.id)).order_by(desc(Post.date_posted)).all()

    # [title, username, date posted, content, number of likes, post id, number of comments]
    posts_list = []
    for i in range(min(len(posts), 15)):
        username = User.query.filter(User.id == posts[i].user_id).first().username
        date_posted = posts[i].date_posted.strftime("%d/%m/%Y")
        comment_count = len(Comments.query.filter(Comments.post_id == posts[i].id).all())
        posts_list.append([posts[i].title, username, date_posted, posts[i].content, posts[i].likes_count, posts[i].id, comment_count])

    return render_template("social/personalised-feed.html", len=len(posts_list), posts=posts_list, current_user_id=current_user.id)


@social_blueprint.route('/social/view/<int:post_id>', methods=["GET", "POST"])
@login_required
def view(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    comments = Comments.query.filter(Comments.post_id == Post.id, Post.id == post_id).all()
    user_likes = Likes.query.filter(Likes.user_id == current_user.id).all()

    list_of_liked_posts = []
    for i in range(0, len(user_likes)):
        list_of_liked_posts.append(int(user_likes[i].post_id))

    if request.args.get("add_like"):
        post_id = int(request.args.get("add_like"))

        # Check if the post has already been liked by the current user
        existing_like = Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()

        if existing_like is None and post_id not in list_of_liked_posts:
            # Like does not exist, add a new like
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post.likes_count += 1
                new_like = Likes(user_id=current_user.id, post_id=post_id)
                db.session.add(new_like)
                db.session.commit()
        elif existing_like:
            # Like exists, remove the like
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post.likes_count -= 1
                db.session.delete(existing_like)
                db.session.commit()

    # list to pass to the template containing the name of the user that made the comment and the content of the comment
    comments_list = []
    for comment in comments:
        user = User.query.filter(User.id == comment.user_id).first()
        comments_list.append([user.username, comment.content])
    
    create_comment_form = CreateCommentForm()

    if create_comment_form.validate_on_submit():
        comment_content = create_comment_form.commentContent.data
        new_comment = Comments(current_user.id, post_id, comment_content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("social.view", post_id=post_id))
    number_of_comments = len(Comments.query.filter(Comments.post_id == post_id).all())
    return render_template("social/view-post.html", post=post, comments_len=len(comments_list),
                           comments=comments_list, create_comment_form=create_comment_form,
                           number_of_comments=number_of_comments)


@social_blueprint.route("/social/create_post", methods=["GET", "POST"])
@login_required
def create_post():

    create_post_form = CreatePostForm()

    if create_post_form.validate_on_submit():

        post_title = profanity.censor(create_post_form.postTitle.data)
        post_content = profanity.censor(create_post_form.postContent.data)

        new_post = Post(current_user.id, post_title, post_content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("social.feed"))
    
    return render_template("social/create_post.html", create_post_form=create_post_form)


@social_blueprint.route('/social/view_profile/<int:user_id>')
@login_required
def view_profile(user_id):

    existing_friendship = Friendships.query.filter_by(user_id=current_user.id, friend_id=user_id).first()
    query_user = User.query.filter(User.id == user_id).first()

    user_likes = Likes.query.filter(Likes.user_id == current_user.id).all()
    list_of_liked_posts = []

    for i in range(0, len(user_likes)):
        list_of_liked_posts.append(int(user_likes[i].post_id))

    if request.args.get("add_like"):
        post_id = int(request.args.get("add_like"))

        # Check if the post has already been liked by the current user
        existing_like = Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()

        if existing_like is None and post_id not in list_of_liked_posts:
            # Like does not exist, add a new like
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post.likes_count += 1
                new_like = Likes(user_id=current_user.id, post_id=post_id)
                db.session.add(new_like)
                db.session.commit()
        elif existing_like:
            # Like exists, remove the like
            post = Post.query.filter_by(id=post_id).first()
            if post:
                post.likes_count -= 1
                db.session.delete(existing_like)
                db.session.commit()

    posts = Post.query.filter(Post.user_id == user_id).order_by(desc(Post.date_posted)).all()

    # [title, username, date posted, content, number of likes, post id, number of comments]
    posts_list = []
    for i in range(min(len(posts), 15)):
        username = User.query.filter(User.id == posts[i].user_id).first().username
        date_posted = posts[i].date_posted.strftime("%d/%m/%Y")
        comment_count = len(Comments.query.filter(Comments.post_id == posts[i].id).all())
        posts_list.append(
            [posts[i].title, username, date_posted, posts[i].content, posts[i].likes_count, posts[i].id, comment_count])

    return render_template("social/view_profile.html", query_user=query_user, existing_friendship=existing_friendship,
                           len=len(posts_list), posts=posts_list, current_user_id=current_user.id, user_id=user_id)



@social_blueprint.route('/add_friends/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add_friends(user_id):
    existing_friendship = Friendships.query.filter_by(user_id=current_user.id, friend_id=user_id).first()
    if not existing_friendship:
        new_friendship = Friendships(user_id=current_user.id,
                                 friend_id=user_id)
        db.session.add(new_friendship)
        db.session.commit()
    return redirect('/social/view_profile/{}'.format(user_id))


@social_blueprint.route('/remove_friends/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove_friends(user_id):
    existing_friendship = Friendships.query.filter_by(user_id=current_user.id, friend_id=user_id).first()
    db.session.delete(existing_friendship)
    db.session.commit()
    return redirect('/social/view_profile/{}'.format(user_id))