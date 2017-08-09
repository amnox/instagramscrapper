from flask_wtf import FlaskForm
from wtforms import StringField , IntegerField
from wtforms.validators import DataRequired


class InstaForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('name', validators=[DataRequired()])
    depth = IntegerField('depth')
    min_likes = IntegerField('min_likes')
