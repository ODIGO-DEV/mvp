from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    comment_text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")
