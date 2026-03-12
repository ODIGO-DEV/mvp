from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class PostForm(FlaskForm):
    title = StringField("Title", validators=[Optional()])
    content = TextAreaField("Content", validators=[DataRequired()])
    images = MultipleFileField("Images", validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    comment_text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")
