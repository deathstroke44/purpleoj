from flask import Flask, render_template, request

from flask_wtf import FlaskForm

from flask_codemirror.fields import CodeMirrorField

from wtforms.fields import SubmitField, TextAreaField

from flask_codemirror import CodeMirror

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# mandatory

CODEMIRROR_LANGUAGES = ['python']

WTF_CSRF_ENABLED = True

SECRET_KEY = 'secret'

# optional

CODEMIRROR_THEME = '3024-day'

CODEMIRROR_ADDONS = (

    ('display', 'placeholder'),

('hint', 'anyword-hint'),

('hint', 'show-hint'),

)

app = Flask(__name__)

app.config.from_object(__name__)

codemirror = CodeMirror(app)





class MyForm(FlaskForm):

    source_code = CodeMirrorField(language='python', config={'lineNumbers': 'true'})

    submit = SubmitField('Submit')

    inputs = TextAreaField(u'inputs')







@app.route('/editor', methods=['GET', 'POST'])

def editor():

    form = MyForm(request.form)

    if request.method == 'POST':

        text = form.source_code.data

        fout=open("submissions/1.py","w")

        print(text,file=fout)

        fout.close()

        if "run" in request.form:

            if request.form.get('custom_input') != None:

                inputs=form.inputs.data

                finputs=open("custom_inputs/1.txt","w")

                print(inputs,file=finputs)

                finputs.close()

                error = os.system("python3 submissions/1.py<custom_inputs/1.txt")

                return render_template('editor.html', form=form, output=error)





        elif "submit" in request.form:

            print("submit")



    return render_template('editor.html', form=form)



if __name__ == '__main__':

    app.secret_key = 'SUPER SECRET KEY'

    app.debug = True

    app.run()
