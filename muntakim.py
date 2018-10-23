from flask import Flask, render_template, request
from wtforms import Form, IntegerField, StringField, PasswordField, validators, FileField, FloatField, TextAreaField
from flask_wtf import FlaskForm
import time
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
    now=time.time()
    then=time.time()
    fout = open(getProgramFileName("Python"), "w")
    print(text, file=fout)
    fout.close()
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open(getCustomInputsFileName("Python"), "w")
        print(inputs, file=finputs)
        finputs.close()
        now=time.time()
        os.system("python3 "+ getProgramFileName("Python")+" < "+getCustomInputsFileName("Python")+" 1>"+getOutputFileName("Python")+ " 2>"
                  +getErrorFileName("Python"))
        then=time.time()

    else:
        now = time.time()
        os.system("python3 " + getProgramFileName(
            "Python") + " 1>" + getOutputFileName("Python") + " 2>"
                  + getErrorFileName("Python"))
        then = time.time()
        # timeElapsed = then - now
        # finputs = open(getOutputFileName(), "r")
        # outputs = finputs.readlines()
        # outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
        # finputs.close()
        # finputs = open(getErrorFileName(), "r")
        # errors = finputs.readlines()
        # finputs.close()
        # os.system("rm -r submissions/" + getUserId())
    finputs = open(getOutputFileName("Python"), "r")
    timeElapsed = then - now
    outputs = finputs.readlines()
    outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    finputs.close()
    finputs = open(getErrorFileName("Python"), "r")
    errors = finputs.readlines()
    finputs.close()
    os.system("rm -r submissions/" + getUserId())
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
    text = "public class Main{\n" + text + "\n}"
    now = time.time()
    then = time.time()
    fout = open(getProgramFileName("Java"), "w")
    print(text, file=fout)
    fout.close()
    # compiling the program
    os.system("javac "  + getProgramFileName("Java") + " 2>" + getErrorFileName("Java"))
    # reading errors
    finputs = open(getErrorFileName("Java"), "r")
    errors = finputs.readlines()
    finputs.close()
    print(errors)
    # running with user defined inputs
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open(getCustomInputsFileName(), "w")
        print(inputs, file=finputs)
        finputs.close()
        if len(errors)==0:
            os.system("cd "+getExecutibleFileName()+" && java Main <"+ getCustomInputsFileName() +
                      " 1> "+getOutputFileName()+ " 2> " +getErrorFileName("Java"))
        else:
            print(errors)
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    # running without inputs
    else:
        if len(errors)==0:
            os.system("cd "+getExecutibleFileName("Java") + " && java Main"  +
                      " 1> " + getOutputFileName("Java") + " 2> " + getErrorFileName("Java"))
            print("cd "+getExecutibleFileName("Java") + " && java Main"  +
                      " 1> " + getOutputFileName("Java") + " 2> " + getErrorFileName("Java"))
        else:
            print(errors)
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    finputs = open(getOutputFileName(), "r")
    outputs = finputs.readlines()
    finputs.close()
    finputs = open(getErrorFileName(), "r")
    # print(finputs)
    errors = finputs.readlines()
    finputs.close()
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
    now = time.time()
    then = time.time()
    fout = open(getProgramFileName("C"), "w")
    print(text, file=fout)
    fout.close()
    # compiling the program
    os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
    # reading errors
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    print(errors)
    # running with user defined inputs
    if auxForm.get("custom_input") != None:
        inputs = form.inputs.data
        finputs = open(getCustomInputsFileName(), "w")
        print(inputs, file=finputs)
        finputs.close()
        # checking for compile errors
        if len(errors) == 0:
            os.system(" ./"+ getExecutibleFileName("C") +" < "+getCustomInputsFileName()+
                      " 1> "+getOutputFileName()+" 2> "+getErrorFileName())

        else:
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    # running without inputs
    else:
        if len(errors) == 0:
            os.system(" ./" + getExecutibleFileName("C") +" 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        else:
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    # reading program outputs
    finputs = open(getOutputFileName(), "r")
    outputs = finputs.readlines()
    finputs.close()
    # reading RTE
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()

    # checking for RTE
    if len(errors) == 0:
        print(outputs)
        return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    else:
        print(errors)
        return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                               languages=languages)

def getProblemSolution():
    return 12

def getProgramFileName(language):
    if language=="Python":
        return "submissions/" + getUserId() + "/" + getProblemId()+"/1.py"
    elif language=="Java":
        return "submissions/" + getUserId() + "/" + getProblemId() + "/Main.java"
    else:
        return "submissions/" + getUserId() + "/" + getProblemId()+"/1.cpp"
def getExecutibleFileName(language):
    if language=="Python":
        return "submissions/" + getUserId() + "/" + getProblemId()+"/a"
    elif language=="Java":
        return "submissions/" + getUserId() + "/" + getProblemId()
    else:
        return "submissions/" + getUserId() + "/" + getProblemId()+"/a"
def getOutputFileName(language):
    if language=="java":
        return "outputs/1.txt"
    return "submissions/" + getUserId() + "/" + getProblemId()+"/outputs/1.txt"
def getErrorFileName(language):
    if language=="java":
        return "outputs/error.txt"
    return "submissions/" + getUserId() + "/" + getProblemId()+"/outputs/error.txt"

def getCustomInputsFileName(language):
    if language=="java":
        return "custom_inputs/1.txt"
    return "submissions/" + getUserId() + "/" + getProblemId()+"/custom_inputs/1.txt"

def getUserId():
    return "User1"

def getProblemId():
    return "TestProblem"

def makeSubmissionFolders():
    os.system("mkdir submissions/" + getUserId())
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId())
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId()+"/outputs")
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId() + "/custom_inputs")


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    selectedLanguage = request.form.get('languages')
    print(selectedLanguage)
    print(dir_path)
    if request.method == 'POST':
        if "run" in request.form:
            makeSubmissionFolders()
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
