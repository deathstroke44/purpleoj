from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import datetime
import os
import time

from flask import Flask, render_template, request
from flask import flash
from flask import redirect, url_for, session, Session
from flask_ckeditor import CKEditor, CKEditorField
from flask_codemirror import CodeMirror
from flask_codemirror.fields import CodeMirrorField
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import Form, IntegerField, StringField, PasswordField, validators
from wtforms.fields import SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
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

class UploadForm(Form):
    time_limit = IntegerField("Time limit(ms)", [validators.DataRequired()])
    memory_limit = IntegerField("Memory Limit(MB)", [validators.DataRequired()])
    category = StringField("Problem Style(ACM,IOI)", [validators.DataRequired()])
    name = StringField('Problem name', [validators.DataRequired()])
    count = IntegerField('Number Of subtask(at least 1 at most 3)',
                         [validators.DataRequired()] and [validators.number_range(1, 3)])
    point1 = IntegerField('Point for Subtask 1')
    point2 = IntegerField('Point for Subtask 2')
    point3 = IntegerField('Point for Subtask 3')

class graph_input(Form):
    nodes_cnt=IntegerField("Number of Nodes",[validators.DataRequired()])
    nodes_desc=TextAreaField("Nodes",[validators.DataRequired])
    ed_cnt=IntegerField("Number of Edgs",[validators.DataRequired()])
    ed_desc=TextAreaField("Edges",[validators.DataRequired()])

class create_article_form(Form):
    title = StringField('Post Title', [validators.DataRequired()])
    text = CKEditorField('Post Body', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class UpdateProfileForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    username = StringField('Username', [validators.optional()])
    email = EmailField('Email', [validators.optional()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Submit')


