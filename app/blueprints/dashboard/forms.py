from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class AddRecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    public = BooleanField("Public", default=True)
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    origin_id = SelectField("Origin", coerce=int, validators=[Optional()])
    recipe_image = FileField("Recipe Image", validators=[Optional()])
    submit = SubmitField("Create Recipe")

class SettingsForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField("Email", validators=[DataRequired(), Length(min=3, max=150)])
    submit = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        super(AddRecipeForm, self).__init__(*args, **kwargs)

        # Populate category choices
        self.category_id.choices = [(0, 'Select a category')] + [
            (c.id, c.name) for c in Category.query.all()
        ]

        # Populate origin choices
        self.origin_id.choices = [(0, 'Select an origin')] + [
            (o.id, f"{o.country} - {o.culture}" if o.culture else o.country)
            for o in Origin.query.all()
        ]
