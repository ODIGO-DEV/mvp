from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, FileField, SubmitField, FieldList, FormField, IntegerField, FloatField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional
from app.models.category import Category
from app.models.origin import Origin


class IngredientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    quantity = FloatField("Quantity", validators=[Optional()])
    unit = StringField("Unit")

class StepForm(FlaskForm):
    step_number = IntegerField("Step Number", validators=[DataRequired()])
    instruction = TextAreaField("Instruction", validators=[DataRequired()])

class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    public = BooleanField("Public", default=True)
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    origin_id = SelectField("Origin", coerce=int, validators=[Optional()])
    recipe_images = MultipleFileField("Recipe Images", validators=[Optional()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(FormField(StepForm), min_entries=1)
    submit = SubmitField("Create Recipe")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id.choices = [(0, '-- Select Category --')] + [(c.id, c.name) for c in Category.query.all()]
        self.origin_id.choices = [(0, '-- Select Origin --')] + [(o.id, o.country) for o in Origin.query.all()]

class SettingsForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField("Email", validators=[DataRequired(), Length(min=3, max=150)])
    submit = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommentForm(FlaskForm):
    comment_text = TextAreaField("Comment", validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField("Post Comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
