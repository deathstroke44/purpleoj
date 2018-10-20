from flask import Flask, render_template, request
from wtforms import Form, IntegerField, StringField, PasswordField, validators, FileField, FloatField, TextAreaField
from flask_wtf import FlaskForm

from flask_codemirror.fields import CodeMirrorField

from wtforms.fields import SubmitField, TextAreaField

from flask_codemirror import CodeMirror

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
languages = ["Java", "C", "Python"]
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


def runPython(auxForm):
    form = MyForm(auxForm)
    text = form.source_code.data
    fout = open("submissions/1.py", "w")
    print(text, file=fout)
    fout.close()
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open("submissions/custom_inputs/1.txt", "w")
        print(inputs, file=finputs)
        finputs.close()
        os.system("cd submissions && python3 1.py<custom_inputs/1.txt 1>outputs/1.txt 2> outputs/error.txt")
        finputs = open("submissions/outputs/1.txt", "r")
        outputs = finputs.readlines()
        finputs.close()
        finputs = open("submissions/outputs/error.txt", "r")
        errors = finputs.readlines()
        finputs.close()
        os.remove("submissions/outputs/1.txt")
        os.remove("submissions/outputs/error.txt")
    else:
        os.system("cd submissions &&  python3 1.py 1>outputs/1.txt 2> outputs/error.txt")
        finputs = open("submissions/outputs/1.txt", "r")
        outputs = finputs.readlines()
        finputs.close()
        finputs = open("submissions/outputs/error.txt", "r")
        errors = finputs.readlines()
        finputs.close()
        os.remove("submissions/outputs/1.txt")
        os.remove("submissions/outputs/error.txt")
    if len(errors) == 0:
        print(outputs)
        return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    else:
        print(errors)
        return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                               languages=languages)


def runJava(auxForm):
    form = MyForm(auxForm)
    text = form.source_code.data
    text = "public class a{\n" + text + "\n}"
    print(text)
    fout = open("submissions/a.java", "w")
    print(text, file=fout)
    fout.close()
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open("submissions/custom_inputs/1.txt", "w")
        print(inputs, file=finputs)
        finputs.close()
        os.system("cd submissions && javac a.java 2> outputs/error.txt")
        finputs = open("submissions/outputs/error.txt", "r")
        print(finputs)
        errors = finputs.readlines()
        finputs.close()
        if len(errors)==0:
            os.system("cd submissions && java a <custom_inputs/1.txt 1>outputs/1.txt 2> outputs/error.txt")
            finputs = open("submissions/outputs/1.txt", "r")
            outputs = finputs.readlines()
            finputs.close()
            finputs = open("submissions/outputs/error.txt", "r")
            print(finputs)
            errors = finputs.readlines()
            finputs.close()
        else:
            print(errors)
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)

        try:
            os.remove("submissions/outputs/1.txt")
            os.remove("submissions/outputs/error.txt")
            os.system("rm submissions/a.class")
            os.remove("submissions/a.java")
        except:
            print("")
    else:
        os.system("cd submissions && javac a.java 2> outputs/error.txt")
        finputs = open("submissions/outputs/error.txt", "r")
        print(finputs)
        errors = finputs.readlines()
        finputs.close()
        if len(errors)==0:
            os.system("cd submissions && java a <custom_inputs/1.txt 1>outputs/1.txt 2> outputs/error.txt")
            finputs = open("submissions/outputs/1.txt", "r")
            outputs = finputs.readlines()
            finputs.close()
            finputs = open("submissions/outputs/error.txt", "r")
            errors = finputs.readlines()
            finputs.close()
        else:
            try:
                os.remove("submissions/outputs/1.txt")
                os.remove("submissions/outputs/error.txt")
                os.system("rm submissions/a.class")
                os.remove("submissions/a.java")
            except:
                print("error occured")
            print(errors)
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
        try:
            os.remove("submissions/outputs/1.txt")
            os.remove("submissions/outputs/error.txt")
            os.system("rm submissions/a.class")
            os.system("rm submissions/a.java")
        except:
            print("error occured")
    if len(errors) == 0:
        print(outputs)
        return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    else:
        print(errors)
        return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                               languages=languages)


def runC(auxForm):
    form = MyForm(auxForm)
    text = form.source_code.data
    print(text)
    fout = open("submissions/1.cpp", "w")
    print(text, file=fout)
    fout.close()
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open("submissions/custom_inputs/1.txt", "w")
        print(inputs, file=finputs)
        finputs.close()
        os.system(" g++ -o submissions/1 submissions/1.cpp 2>submissions/outputs/error.txt")
        # checking for compile time errors
        finputs = open("submissions/outputs/error.txt", "r")
        errors = finputs.readlines()
        finputs.close()
        print(errors)
        if len(errors) == 0:
            os.system(
                " ./submissions/1 <submissions/custom_inputs/1.txt 1>submissions/outputs/1.txt 2> submissions/outputs/error.txt")
            finputs = open("submissions/outputs/1.txt", "r")
            outputs = finputs.readlines()
            finputs.close()
            finputs = open("submissions/outputs/error.txt", "r")
            errors = finputs.readlines()
            finputs.close()
        else:
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
        os.remove("submissions/outputs/1.txt")
        os.remove("submissions/outputs/error.txt")
        os.system("rm submissions/1")
        os.remove('submissions/1.cpp')
    else:
        os.system("cd submissions && g++ -o 1 1.cpp  2>outputs/error.txt")
        finputs = open("submissions/outputs/error.txt", "r")
        errors = finputs.readlines()
        finputs.close()
        if len(errors) == 0:
            os.system("./submissions/1 1>submissions/outputs/1.txt 2>submissions/outputs/error.txt")
            finputs = open("submissions/outputs/1.txt", "r")
            outputs = finputs.readlines()
            finputs.close()
            finputs = open("submissions/outputs/error.txt", "r")
            errors = finputs.readlines()
            finputs.close()
        else:
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
        os.remove("submissions/outputs/1.txt")
        os.remove("submissions/outputs/error.txt")
        os.system("rm submissions/1")
        os.remove('submissions/1.cpp')

    if len(errors) == 0:
        print(outputs)
        return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    else:
        print(errors)
        return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                               languages=languages)


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    selectedLanguage = request.form.get('languages')
    print(selectedLanguage)
    if request.method == 'POST':
        if "run" in request.form:
            if selectedLanguage == "Python":
                return runPython(request.form)
            elif selectedLanguage == "C":
                return runC(request.form)
            elif selectedLanguage == "Java":
                return runJava(request.form)

        elif "submit" in request.form:

            print("submit")

    return render_template('editor.html', form=MyForm(request.form), languages=languages)


if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'

    app.debug = True

    app.run()
