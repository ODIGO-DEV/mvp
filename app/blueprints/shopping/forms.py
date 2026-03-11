from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ShoppingListItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired(), Length(max=200)])
    quantity = StringField("Quantity", validators=[Length(max=50)])
    category = SelectField(
        "Category",
        choices=[
            ("produce", "Produce"),
            ("dairy", "Dairy"),
            ("meat", "Meat & Seafood"),
            ("bakery", "Bakery"),
            ("pantry", "Pantry"),
            ("frozen", "Frozen"),
            ("beverages", "Beverages"),
            ("snacks", "Snacks"),
            ("other", "Other"),
        ],
    )
    notes = TextAreaField("Notes", validators=[Length(max=500)])
    submit = SubmitField("Add Item")
