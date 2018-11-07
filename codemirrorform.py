from flask_codemirror.fields import CodeMirrorField
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class CodemirrorForm(FlaskForm):
    source_code = CodeMirrorField(language='python', config={'lineNumbers': 'true'})
    submit = SubmitField('Submit')
    inputs = TextAreaField(u'inputs')
