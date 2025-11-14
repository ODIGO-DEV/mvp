from flask_wtf import FlaskForm
from wtforms import SubmitField

class MealPlannerForm(FlaskForm):
    submit = SubmitField("Save Plan")