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
from FunctionList import *
from forms import IssueForm, CommentForm,UploadForm,graph_input,create_article_form,LoginForm,RegisterForm
from ClassesList import problem,postob

class Create:
    def __init__(self,id,name,acc,sc,box):
        self.id=id
        self.name=name
        self.acc=acc
        self.sc=sc
        self.box=box

class Contest:

    def createContest(self,mongo,form,list):

        print(request.form[form.contestname.name])
        cnt = 0;
        selected_problem_id = []
        name = 'A'
        for prblm in list:
            if request.form.get(prblm.id):
                cnt += 1
                selected_problem_id.append({forward_letter(name, cnt - 1): prblm.id});
                print(prblm.name)
        if cnt>0:
            contests = mongo.db.contests
            contests.insert({'Contest Title': form.contestname.data, 'Start Date': request.form['date'],
                         'Start Time': request.form['start_time'], 'End Time': request.form['end_time'],
                         'Password': request.form['password'], 'Problem Count': cnt, 'Problem ID': selected_problem_id})
        return cnt


class create_contest_form(Form):
    contestname=TextAreaField("Contest Name",[validators.DataRequired()])

def forward_letter(letter, positions):
        if letter.islower():
            unicode_point = ord('a')
        else:
            unicode_point = ord('A')
        start = ord(letter) - unicode_point
        offset = ((start + positions)) + unicode_point
        current_letter = chr(offset)
        return current_letter