from flask import Flask, render_template, request
from flask import request, redirect,url_for,render_template,session,Session
from wtforms import Form, IntegerField, StringField, PasswordField, validators, FileField, FloatField, TextAreaField
from flask_wtf import FlaskForm
import time
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField, TextAreaField
from flask_codemirror import CodeMirror
import os
import uuid
import datetime
from flask_pymongo import PyMongo

from flask_testing import TestCase


# mandatory



WTF_CSRF_ENABLED = True

SECRET_KEY = 'secret'

# optional



app = Flask(__name__)

# ***************************************************************************
dir_path = os.path.dirname(os.path.realpath(__file__))
languages = ["Java", "C", "Python"]
CODEMIRROR_LANGUAGES = ['python']

CODEMIRROR_THEME = '3024-day'

CODEMIRROR_ADDONS = (

    ('display', 'placeholder'),
    ('hint', 'anyword-hint'),
    ('hint', 'show-hint'),

)
app.config['MONGO_URI']='mongodb://red44:omi123@ds131963.mlab.com:31963/purpleoj'
app.config.from_object(__name__)
codemirror = CodeMirror(app)
mongo = PyMongo(app)
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
        finputs = open(getCustomInputsFileName(), "w")
        print(inputs, file=finputs)
        finputs.close()
        now=time.time()
        os.system("python3 "+ getProgramFileName("Python")+" < "+getCustomInputsFileName()+" 1>"+
                  getOutputFileName()+ " 2>"
                  +getErrorFileName())
        then=time.time()

    else:
        now = time.time()
        os.system("python3 " + getProgramFileName(
            "Python") + " 1>" + getOutputFileName() + " 2>"
                  + getErrorFileName())
        then = time.time()
    finputs = open(getOutputFileName(), "r")
    timeElapsed = then - now
    outputs = finputs.readlines()
    outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    finputs.close()
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    #os.system("rm -r submissions/" + getUserId())
    if len(errors) == 0:
        # print(outputs)
        return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    else:
        print(errors)
        return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                               languages=languages)


def runJava(auxForm):
    form = MyForm(auxForm)
    text = form.source_code.data
    now = time.time()
    then = time.time()
    fout = open(getProgramFileName("Java"), "w")
    print(text, file=fout)
    fout.close()
    # compiling the program
    os.system("javac "  + getProgramFileName("Java") + " 2>" + getErrorFileName())
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
        if len(errors)==0:
            now = time.time()
            os.system("java -cp "+getExecutibleFileName("Java")+" Main <"+ getCustomInputsFileName() +
                      " 1> "+getOutputFileName()+ " 2> " +getErrorFileName())
            then= time.time()
        else:
            print(errors)
            #os.system("rm -r submissions/" + getUserId())
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    # running without inputs
    else:
        if len(errors)==0:
            now = time.time()
            os.system("java -cp " + getExecutibleFileName("Java") + " Main " +" 1> " +
                      getOutputFileName() + " 2> " + getErrorFileName())
            then = time.time()

        else:
            print(errors)
            #os.system("rm -r submissions/" + getUserId())
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    finputs = open(getOutputFileName(), "r")
    outputs = finputs.readlines()
    finputs.close()
    timeElapsed = then - now
    # outputs=list("")
    outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    finputs = open(getErrorFileName(), "r")
    # print(finputs)
    errors = finputs.readlines()
    finputs.close()
    #os.system("rm -r submissions/" + getUserId())
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
            now=time.time()
            os.system(" ./"+ getExecutibleFileName("C") +" < "+getCustomInputsFileName()+
                      " 1> "+getOutputFileName()+" 2> "+getErrorFileName())
            then=time.time()

        else:
            #os.system("rm -r submissions/" + getUserId())
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    # running without inputs
    else:
        if len(errors) == 0:
            now=time.time()
            os.system(" ./" + getExecutibleFileName("C") +" 1> " + getOutputFileName() + " 2> " + getErrorFileName())
            then=time.time()
        else:
            #os.system("rm -r submissions/" + getUserId())
            return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                   languages=languages)
    # reading program outputs
    finputs = open(getOutputFileName(), "r")
    outputs = finputs.readlines()
    finputs.close()
    timeElapsed = then - now
    outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    # reading RTE
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    #os.system("rm -r submissions/" + getUserId())
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

def getOutputFileName():
    return "submissions/" + getUserId() + "/" + getProblemId()+"/outputs/1.txt"
def getErrorFileName():
    return "submissions/" + getUserId() + "/" + getProblemId()+"/outputs/error.txt"

def getCustomInputsFileName():
    return "submissions/" + getUserId() + "/" + getProblemId()+"/custom_inputs/1.txt"

def getUserId():
    return "User1"

def getProblemId():
    return "TestProblem"

def getExpectedOutputFileName(problemId):
    return "static/uploads/"+problemId+"out1.txt"

def getTestCaseFileName(problemId):
    return "static/uploads/" + problemId + "in1.txt"


def doesOutputMatch(userOutputFile,expectedOutputFile):
    try:
        userOutput=open(userOutputFile)
    except:
        return False
    expectedOutput=open(expectedOutputFile)
    for (x,y) in zip(userOutput.readlines(),expectedOutput.readlines()):
        if x !=y:
            userOutput.close()
            expectedOutput.close()
            return False
    userOutput.close()
    expectedOutput.close()
    return True


def makeSubmissionFolders():
    os.system("mkdir submissions/" + getUserId())
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId())
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId()+"/outputs")
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId() + "/custom_inputs")

def runCode(form):
    selectedLanguage = form.get('languages')
    print(selectedLanguage)
    makeSubmissionFolders()
    if selectedLanguage == "Python":
        return runPython(form)
    elif selectedLanguage == "C":
        return runC(form)
    elif selectedLanguage == "Java":
        return runJava(form)

def submitCode(auxform,problemId):
    selectedLanguage = auxform.get('languages')
    print(selectedLanguage)
    makeSubmissionFolders()
    submissionInfo=dict()
    submissionInfo["Language"]=selectedLanguage
    submissionInfo["Submission Time"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    form = MyForm(auxform)
    text = form.source_code.data.replace("\t","    ")
    submissionInfo["Code"] = text
    now=time.time()
    then=time.time()
    fout = open(getProgramFileName(selectedLanguage), "w")
    print(text, file=fout)
    fout.close()
    #compiling
    if selectedLanguage=="Java":
        os.system("javac " + getProgramFileName("Java") + " 2>" + getErrorFileName())
    elif selectedLanguage=="C":
        os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
    # reading compile errors
    if selectedLanguage!="Python":
        finputs = open(getErrorFileName(), "r")
        errors = finputs.readlines()
        finputs.close()

        if (len(errors) != 0):
            print(errors)
            submissionInfo["Comilation Status"] = "CE"
            return submissionInfo
    # running the program
    if selectedLanguage=="Python":
        now = time.time()
        os.system("python3 " + getProgramFileName("Python") + " < " + getTestCaseFileName(problemId) + " 1>" +
                  getOutputFileName() + " 2>" + getErrorFileName())
        then = time.time()
    elif selectedLanguage=="Java":
        now = time.time()
        os.system("java -cp " + getExecutibleFileName("Java") + " Main <" + getTestCaseFileName(problemId) +
                  " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        then = time.time()
    elif selectedLanguage=="C":
        now = time.time()
        os.system(" ./" + getExecutibleFileName("C") + " < " + getTestCaseFileName(problemId) +
                  " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        then = time.time()

    # reading runtime errors
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    if len(errors)!=0:
        submissionInfo["Run Status"]="RTE"
        return submissionInfo
    timeElapsed=then-now
    submissionInfo["Execution Time"]=timeElapsed
    # if timeElapsed>2:
    #     return "TLE"
    if doesOutputMatch(getExpectedOutputFileName(problemId),getOutputFileName()) == False :
        submissionInfo["Result Verdict"]="WA"
        return submissionInfo
    else:
        submissionInfo["Result Verdict"] ="Passed"
        return submissionInfo


def cleanup():
    os.system("rm -r submissions/" + getUserId())

@app.route('/editor/<problemId>', methods=['GET', 'POST'])
def editor(problemId):
    problemsDatabase=mongo.db.problems
    submissionDatabase=mongo.db.submissions
    if request.method == 'POST':
        if "run" in request.form:
            template = runCode(request.form)
            cleanup()
            return template

        elif "submit" in request.form:
            submissionInfo=submitCode(request.form,problemId)
            print(submissionInfo)
            problemTimeLimit=problemsDatabase.find_one({"myid":problemId}).get("time_limit")
            verdict=dict()
            verdict["Submission Time"]=submissionInfo.get("Submission Time")
            verdict["Language"]=submissionInfo.get("Language")
            if submissionInfo.get("Compilation Status") !=None:
                verdict["Status"]=submissionInfo.get("Compilation Status")
            elif submissionInfo.get("Run Status")!=None:
                verdict["Status"]=submissionInfo.get("Run Status")
            else:
                if float(problemTimeLimit)<float(submissionInfo.get("Execution Time")):
                    verdict["Status"]="TLE"
                else:
                    if submissionInfo.get("Result Verdict")=="Passed":
                        verdict["Status"]="AC"
                    else:
                        verdict["Status"]="WA"
            verdict["Execution Time"]=submissionInfo.get("Execution Time")
            verdict["Problem Id"]=problemId
            verdict["User Id"]=session["username"]
            verdict["Code"]=submissionInfo.get("Code")
            verdict["Contest Id"]=""
            verdict["Submission Id"]=uuid.uuid4().__str__()
            submissionDatabase.insert(verdict)
            print(verdict)
            cleanup()

    return render_template('editor.html', form=MyForm(request.form), languages=languages)
@app.route('/editor/<contestId>/<problemId>', methods=['GET', 'POST'])
def contestEditor(problemId, contestId):
    problemsDatabase=mongo.db.problems
    submissionDatabase=mongo.db.submissions
    print("for contest")
    if request.method == 'POST':
        if "run" in request.form:
            template = runCode(request.form)
            cleanup()
            return template

        elif "submit" in request.form:
            submissionInfo=submitCode(request.form,problemId)
            print(submissionInfo)
            problemTimeLimit=problemsDatabase.find_one({"myid":problemId}).get("time_limit")
            verdict=dict()
            verdict["Submission Time"]=submissionInfo.get("Submission Time")
            verdict["Language"]=submissionInfo.get("Language")
            if submissionInfo.get("Compilation Status") !=None:
                verdict["Status"]=submissionInfo.get("Compilation Status")
            elif submissionInfo.get("Run Status")!=None:
                verdict["Status"]=submissionInfo.get("Run Status")
            else:
                if float(problemTimeLimit)<float(submissionInfo.get("Execution Time")):
                    verdict["Status"]="TLE"
                else:
                    if submissionInfo.get("Result Verdict")=="Passed":
                        verdict["Status"]="AC"
                    else:
                        verdict["Status"]="WA"
            verdict["Execution Time"]=submissionInfo.get("Execution Time")
            verdict["Problem Id"]=problemId
            verdict["User Id"]=session["username"]
            verdict["Code"]=submissionInfo.get("Code")
            verdict["Contest Id"]=contestId
            verdict["Submission Id"]=uuid.uuid4().__str__()
            submissionDatabase.insert(verdict)
            print(verdict)
            cleanup()

    return render_template('editor.html', form=MyForm(request.form), languages=languages)


# *****************************************************************************************



if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'

    app.debug = True

    app.run()
