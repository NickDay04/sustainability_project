from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    postTitle = StringField("post_title", validators=[DataRequired()])
    postContent = TextAreaField("post_content", validators=[DataRequired()])
    submit = SubmitField()


class CreateCommentForm(FlaskForm):
    commentContent = TextAreaField("comment_content", validators=[DataRequired()])
    submit = SubmitField()