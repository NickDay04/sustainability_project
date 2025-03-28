# from flask_login import LoginManager
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.init_app(app)

# from models import User
# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# if form.validate_on_submit():
# user = User.query.filter_by(username=form.username.data).first()
# if not user or not user.verify_password ...
# # Code handling invalid login credentials
# login_user(user)
# return redirect(url_for('blog.blog'))
# return render_template('users/login.html', form=form)
