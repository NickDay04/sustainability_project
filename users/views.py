# -*- coding: utf-8 -*-
"""
    users/views.py
    ~~~~~~~~~~~~~~

    Contains routing and rendering user pages.

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""

from flask import Blueprint, request, render_template, redirect, session, url_for, flash, app
from markupsafe import Markup
import pyotp
from sqlalchemy import or_
from users.forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeUsernameForm, deleteAccountForm, \
    ChangePrivacySettingsForm, DeleteAccountAdminForm, Verify2FA, ChangeUsernameForm, deleteAccountForm
from models import Activity, Comments, Likes, Post, User, Friendships
from flask_login import current_user, login_required, login_user, logout_user
from app import db, requires_roles
from search.search import search_users

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if not session.get("authentication_attempts"):
        session["authentication_attempts"] = 0
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect("/")
        else:
            session["authentication_attempts"] += 1
            if session["authentication_attempts"] >= 3:
                flash(Markup(
                    'Number of incorrect login attempts exceeded. Please click <a href="/reset">here</a> to reset'))
                return render_template("users/login.html")
            flash("Please check your login details and try again.")
    return render_template("users/login.html", form=form)


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # checks if email address is already present in db
        if user:
            flash("That email already exists!")
            return render_template('users/register.html', form=form)
        new_user = User(email=form.email.data,
                        password=form.password.data,
                        username=form.username.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        role="user")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        session["username"] = new_user.username
        return redirect(url_for("users.setup_2fa"))

    return render_template("users/register.html", form=form)

def add_friends():
    selected_friend = db.session.query(User.id).filter_by(firstname="Joshua").first()
    selected_friend_id = int(selected_friend[0])
    new_friendship = Friendships(user_id=current_user.id,
                                 friend_id=selected_friend_id)
    db.session.add(new_friendship)
    db.session.commit()


@users_blueprint.route('/account', methods=["GET", "POST"])
@login_required
def account():
    return render_template("users/account.html")


@users_blueprint.route('/search', methods=["GET", "POST"])
@login_required
def search():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter(User.username == username, User.private == "0").first()
        if user:
            return redirect("/social/view_profile/" + str(user.id))
        else:
            flash("That user does not exist!")
    return render_template("search/search.html")


@users_blueprint.route('/change_password', methods=["GET", "POST"])
@login_required
def ChangePassword():
    if "2fa_validated" not in session:
        return redirect("/verify_2fa?redirect_to=" + request.path)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()

        if not user.verify_password(form.oldPassword.data):
            flash("Old password is incorrect.")
            return render_template("users/change_password.html", form=form)

        User.query.filter(User.email == current_user.email).update(
            dict(password=user.hash_password(form.newPassword.data)))
        db.session.commit()
        flash("Password changed!")
        del session["2fa_validated"]
        return redirect(url_for("users.account"))
    return render_template("users/change_password.html", form=form)


@users_blueprint.route('/privacy_settings', methods=["GET", "POST"])
@login_required
def ChangePrivacySettings():
    form = ChangePrivacySettingsForm()
    if form.validate_on_submit():
        private_or_not = User.query.filter(User.id == current_user.id).first()
        p = int(private_or_not.private)
        new_p = 1 - p
        final_p = str(new_p)
        User.query.filter(User.id == current_user.id).update(dict(private=final_p))
        db.session.commit()
        flash("Privacy settings changed!")
    user_object = User.query.filter(User.id == current_user.id).first()
    if user_object.private == "1":
        privacy_setting = "Private"
    elif user_object.private == "0":
        privacy_setting = "public"
    else:
        privacy_setting = "Error"
    return render_template("users/privacy_settings.html", form=form, privacy_setting=privacy_setting)


@users_blueprint.route('/change_username', methods=["GET", "POST"])
@login_required
def changeUsername():
    if "2fa_validated" not in session:
        return redirect("/verify_2fa?redirect_to=" + request.path)
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        User.query.filter(User.email == current_user.email).update(
            dict(username=form.newUsername.data))
        db.session.commit()
        flash("Username changed!")
        del session["2fa_validated"]
        return redirect(url_for("users.account"))
    return render_template("users/change_username.html", form=form)


@users_blueprint.route('/delete_account', methods=["GET", "POST"])
@login_required
def deleteAccount():
    form = deleteAccountForm()
    user = User.query.filter_by(email=current_user.email).first()

    if form.validate_on_submit():
        if not user.verify_password(form.Password.data):
            flash("Password is incorrect.")
            return render_template("users/delete_account.html", form=form)
        db.session.delete(user)
        db.session.commit()
        flash("Account deleted!")
        return redirect(url_for("index.index"))

    return render_template("users/delete_account.html", form=form)


@users_blueprint.route('/delete_account_admin', methods=["GET", "POST"])
@login_required
def deleteAccountAdmin():
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for("index.index"))

    form = DeleteAccountAdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            likes = Likes.query.filter(Likes.user_id == user.id).all()
            for like in likes:
                db.session.delete(like)
            db.session.commit()
            comments = Comments.query.filter(Comments.user_id == user.id).all()
            for comment in comments:
                db.session.delete(comment)
            db.session.commit()
            friendships = Friendships.query.filter(or_(Friendships.user_id == user.id, Friendships.friend_id == user.id)).all()
            for friendship in friendships:
                db.session.delete(friendship)
            db.session.commit()
            activities = Activity.query.filter(Activity.user_id == user.id).all()
            for activity in activities:
                db.session.delete(activity)
            db.session.commit()
            posts = Post.query.filter(Post.user_id == user.id).all()
            for post in posts:
                likes = Likes.query.filter(Likes.post_id == post.id).all()
                for like in likes:
                    db.session.delete(like)
                db.session.commit()
                comments = Comments.query.filter(Comments.post_id == post.id).all()
                for comment in comments:
                    db.session.delete(comment)
                db.session.commit()
                db.session.delete(post)
            db.session.commit()
            db.session.delete(user)
            db.session.commit()
            flash("User account deleted!")
            return redirect(url_for("index.index"))
        else:
            flash("User not found.")

    return render_template("users/delete_account_admin.html", form=form)


@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index.index"))


@users_blueprint.route("/reset")
def reset():
    session["authentication_attempts"] = 0
    return redirect(url_for("users.login"))


@users_blueprint.route("/setup_2fa")
def setup_2fa():
    if "username" not in session:
        return redirect(url_for("index.index"))
    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return redirect(url_for("index.index"))
    del session["username"]
    return render_template("users/setup_2fa.html", username=user.username, uri=user.get_2fa_uri()), 200, {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }


@users_blueprint.route("/verify_2fa", methods=["GET", "POST"])
@login_required
def verify_2fa():
    form = Verify2FA()
    if form.validate_on_submit():
        entered_pin = form.code.data
        user = User.query.filter_by(id=current_user.id).first()
        if pyotp.TOTP(user.pin_key).verify(entered_pin):
            session["2fa_validated"] = True
            return redirect(request.args.get("redirect_to"))
        else:
            flash("Invalid pin. Please try again.")
    return render_template("users/verify_2fa.html", form=form)
