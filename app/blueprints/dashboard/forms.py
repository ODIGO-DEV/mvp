from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from app.models.category import Category
from app.models.origin import Origin


class AddRecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    origin_id = SelectField('Origin', coerce=int, validators=[Optional()])
    public = BooleanField('Make this recipe public', default=True)

    # Image upload
    recipe_image = FileField('Recipe Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])

    submit = SubmitField('Create Recipe')

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
