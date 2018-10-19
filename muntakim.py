from flask import Flask, render_template, request
from wtforms import Form,IntegerField,StringField, PasswordField, validators, FileField, FloatField,TextAreaField
from flask_wtf import FlaskForm

from flask_codemirror.fields import CodeMirrorField

from wtforms.fields import SubmitField, TextAreaField

from flask_codemirror import CodeMirror

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
languages=["Java","C","Python"]
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




def runPython(form,auxForm):
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open("custom_inputs/1.txt", "w")
        print(inputs, file=finputs)
        finputs.close()
        os.system("python3 submissions/1.py<custom_inputs/1.txt 1>outputs/1.txt 2> outputs/error.txt")
        finputs = open("outputs/1.txt", "r")
        outputs = finputs.readlines()
        finputs.close()
        finputs = open("outputs/error.txt", "r")
        errors = finputs.readlines()
        finputs.close()
        os.remove("outputs/1.txt")
        os.remove("outputs/error.txt")
    else:
        os.system("python3 submissions/1.py 1>outputs/1.txt 2> outputs/error.txt")
        finputs = open("outputs/1.txt", "r")
        outputs = finputs.readlines()
        finputs.close()
        finputs = open("outputs/error.txt", "r")
        errors = finputs.readlines()
        finputs.close()
        os.remove("outputs/1.txt")
        os.remove("outputs/error.txt")
    if len(errors) == 0:
        print(outputs)
        return render_template('editor.html', form=form, status="Program Output", outputs=outputs)
    else:
        print(errors)
        return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors
                              )


@app.route('/editor', methods=['GET', 'POST'])

def editor():

    form = MyForm(request.form)

    if request.method == 'POST':

        text = form.source_code.data

        fout=open("submissions/1.py","w")

        print(text,file=fout)

        fout.close()

        if "run" in request.form:
            runPython(form,request.form)

        elif "submit" in request.form:

            print("submit")



    return render_template('editor.html', form=form,languages=languages)



if __name__ == '__main__':

    app.secret_key = 'SUPER SECRET KEY'

    app.debug = True

    app.run()
