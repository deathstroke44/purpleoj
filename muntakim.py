from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from flask_codemirror import CodeMirror

# mandatory
CODEMIRROR_LANGUAGES = ['python', 'html']
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'
# optional
CODEMIRROR_THEME = '3024-day'
CODEMIRROR_ADDONS = (
    ('display', 'placeholder'),
)
app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)


class MyForm(FlaskForm):
    source_code = CodeMirrorField(language='python', config={'lineNumbers': 'true'})
    submit = SubmitField('Submit')


@app.route('/editor.html', methods=['GET', 'POST'])
def editor():
    form = MyForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            text = form.source_code.data
            print(text)
            return text
    return render_template('editor.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'
    app.debug = True
    app.run()
