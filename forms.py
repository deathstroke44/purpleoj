from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_pymongo import PyMongo


class IssueForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=2, max=10000)])
    problemName = SelectField('Select Problem', coerce=int)
    text = TextAreaField('Details',
                       validators=[DataRequired(), Length(min=2, max=50000)])

    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    text = TextAreaField('Details',validators=[DataRequired(), Length(min=2, max=50000)])
