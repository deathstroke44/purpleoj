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
from FunctionList import allowed_file1,giveedge,givenode,edge_list,node_list,f,allowed_file,graph,adapter,jsonstring,problem_user_submissions,pair,valid,valid1
from forms import IssueForm, CommentForm,UploadForm,graph_input,create_article_form,LoginForm,RegisterForm
from ClassesList import *
from CreateContest import *
from UtilityFunctionsForEditor import *
from strategypatternforsubmission import *
app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
ALLOWED_CATEGORY = set(['ACM', 'IOI'])
import uuid

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = 'mongodb://red44:omi123@ds131963.mlab.com:31963/purpleoj'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
ckeditor = CKEditor(app)
mongo = PyMongo(app)

app.secret_key = "super secret key"
sess = Session()

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    nameform = UploadForm(request.form)
    if request.method == 'POST':
        # check if the post request has the file part
        sbcnt = int(request.form.get('cnt'))
        if not valid(strr='file', request=request):
            return redirect(request.url)
        if sbcnt >= 1:
            if not valid(strr='ifile1', request=request) or not valid(strr='ofile1',
                                                                      request=request) or nameform.point1.data == None:
                return redirect(request.url)
        if sbcnt >= 2:
            if not valid(strr='ifile2', request=request) or not valid(strr='ofile2',
                                                                      request=request) or nameform.point2.data == None:
                return redirect(request.url)
        if sbcnt >= 3:
            if not valid(strr='ifile3', request=request) or not valid(strr='ofile3',
                                                                      request=request) or nameform.point3.data == None:
                return redirect(request.url)
        checkerd =False
        if valid1(strr='checker',request=request):
            checkerd=True
        gpb = 'samin'+uuid.uuid4().__str__()
        file = request.files['file']
        filename = gpb + '.pdf'  # secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if checkerd==True:
            file = request.files['checker']
            filename = gpb + 'sol.cpp'  # secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        for i in range(1, sbcnt + 1):
            inp = 'ifile' + str(i)
            out = 'ofile' + str(i)
            file = request.files[inp]
            filename = gpb + 'in' + str(i) + '.txt'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = request.files[out]
            filename = gpb + 'out' + str(i) + '.txt'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pnt1, pnt2, pnt3 = 0, 0, 0
        if not nameform.point1 == None:
            pnt1 = nameform.point1.data
        if not nameform.point1 == None:
            pnt2 = nameform.point2.data
        if not nameform.point1 == None:
            pnt3 = nameform.point3.data

        pb = problem(sbcnt, gpb, pnt1, pnt2, pnt3, nameform.time_limit.data, nameform.memory_limit.data,
                     nameform.category.data, nameform.name.data, 0, 0, session['username'])
        problemdb = mongo.db.problems
        problemdb.insert({
            'sub_task_count': pb.sub_task_count,
            'myid': pb.id,
            'pnt1': pb.pnt1,
            'pnt2': pb.pnt2,
            'pnt3': pb.pnt3,
            'author': session['username'],
            'name': nameform.name.data,
            'time_limit': pb.time_limit,
            'memory_limit': pb.memory_limit,
            'stylee': pb.stylee,
            'acsub': 0,
            'sub': 0,
            'setter': session['username'],
            'checker':checkerd
        })

        return redirect(url_for('upload_file', filename=filename))

    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('upload_problem.html', nameform=nameform)


def valid(strr, request):
    if strr not in request.files:
        return False
    filee = request.files[strr]
    if filee.filename == '':
        return False
    if filee and allowed_file(filee.filename):
        print("Something")
        return True
    return False


def upload_prev():
    nameform = UploadForm(request.form)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template('upload_problem.html', nameform=nameform)




@app.route('/')
def index():
    contest_db = mongo.db.contests
    problem_db = mongo.db.problems
    list = []
    postdb = mongo.db.posts
    existing_post = postdb.find({}).sort('_id')
    contest_db = mongo.db.contests
    contest_cursor=contest_db.find({}).sort('Start Date')
    pclist=[]
    for pc in contest_cursor:
        starting_datetime = pc['Start Date']+"T"+pc['Start Time']+":00+06:00"
        ending_date = pc['Start Date']+"T"+pc['End Time']+":00+06:00"
        id = pc['_id']
        name=pc['Contest Title']
        dt=datetime.datetime.now()
        pcet=pc['End Time']
        rep=''
        flag=0
        for i in range(0,len(pcet)):
            if flag==1:
                rep+=pcet[i]
            if pcet[i]=='.':
                flag=1
        pcet.replace(rep,'')
        ds=datetime.datetime.strptime(pc['Start Date']+' '+pcet,"%Y-%m-%d %H:%M")
        xx=dt.strftime("%Y-%m-%d %H:%M")

        cd = datetime.datetime.strptime(xx,"%Y-%m-%d %H:%M")
        if ds>=dt:
            pclist.append(tripled(starting_datetime,ending_date,id,name))
    i = 0
    for posts in existing_post:
        posttitle = posts['TITLE']
        posttext = posts['TEXT']
        postuser = posts['USER']
        postdate = posts['DATE']
        postid = posts['_id']
        ppp = postob(posttitle, posttext, postdate, postuser, postid)
        list.append(ppp)
        i = i + 1
    list.reverse()

    error = 'You are not logged in'
    dumb = 'dumb'
    if 'username' in session:
        msg = 'You are Logged in as ' + session['username']
        return render_template('home.html', msg=msg, posts=list,PC=pclist)
    return render_template('home.html', error=error, dumb=dumb, posts=list,PC=pclist)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        names = form.name.data
        emails = form.email.data
        usernames = form.username.data
        passwords = form.password.data
        user = mongo.db.userlist
        existing_user = user.find_one({'USERNAME': usernames})
        print('lolllllllllll')
        dialoge = 'Your Account Is created Successfully'
        if existing_user:
            dialoge = 'There is alredy an account in this username'
            return render_template('register.html', form=form, dialoge=dialoge)
        else:
            user.insert({'NAMES': names,
                         'USERNAME': usernames,
                         'MAIL': emails,
                         'PASSWORDS': passwords})
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('st')
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = mongo.db.userlist
        existing_user = user.find_one({'USERNAME': username})
        print(username)
        if existing_user:
            if existing_user['PASSWORDS'] == password:
                print('Password Matched')
                session['logged_in'] = True
                session['username'] = username
                print(session['username'])
                return redirect(url_for('index'))
            else:
                error = 'You are not logged in';
                if 'username' in session:
                    msg = 'You are Logged in as ' + session['username']
                dialogue = 'Wrong Password'
                # flash('Wrong password','error')
                if 'username' in session:
                    return render_template('login.html', msg=msg, form=form, dialogue=dialogue)

                return render_template('login.html', error=error, form=form, dialogue=dialogue)
        else:
            app.logger.info('No User')
            error = 'No such username exist'
            if 'username' in session:
                msg = 'You are Logged in as ' + session['username']
            if 'username' in session:
                return render_template('login.html', msg=msg, form=form, dialogue=error)
            # flash('Wrong Usename Or password', error)
            return render_template('login.html', error=error, form=form, dialogue=error)
    elif 'username' in session:
        msg = 'You are Logged in as ' + session['username']
        return render_template('login.html', msg=msg, form=form)
    else:
        error = 'You are not logged in'
        dialogue = 'Wrong password'
        return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))


@app.route('/post', methods=['GET', 'POST'])
def post():
    form = create_article_form(request.form)

    if request.method == 'POST':
        title = form.title.data
        print("Reach")
        text = form.text.data
        dt = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        ppt = mongo.db.posts
        user_ = session['username']
        gpb = uuid.uuid4().__str__()
        gpb = 'static/posts/' + gpb + '.html'
        f = open(gpb, "w")
        print(text, file=f)
        f.close()
        # postt = postob(title=title,text=text,dt=dt,user_=user_)
        ppt.insert({
            'TITLE': title,
            'TEXT': gpb,
            'DATE': dt,
            'USER': user_
        })
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('create_post.html', form=form)

@app.route('/about/<id>/submit/')
def prob_submit(id):
    return 'Submit ' + id


@app.route('/about/<id>/')
def pdfviewers(id):
    pbdb = mongo.db.problems
    pb = pbdb.find_one({'myid': id})
    pbds = prob_struct(pb['name'], pb['time_limit'], pb['memory_limit'], id)
    if not ('username' in session):
        return redirect(url_for('login'))
    Previous = problem_user_submissions(mongo,session['username'],id)
    for i in range(0,len(Previous)):
        print(Previous[i].first)
    #Previous=[]
    Previous.reverse()
    return render_template("pdfviewer.html", pdf_src='/static/uploads/' + id + '.pdf', pbds=pbds,Previous=Previous)


@app.route('/about')
def postab():
    problemsdb = mongo.db.problems
    list = []
    existing_posts = problemsdb.find({})
    i = 0
    for existing_post in existing_posts:
        ppp = problem(existing_post['sub_task_count'],
                      existing_post['myid'],
                      existing_post['pnt1'],
                      existing_post['pnt2'],
                      existing_post['pnt3'],
                      existing_post['time_limit'],
                      existing_post['memory_limit'],
                      existing_post['stylee'],
                      existing_post['name'],
                      existing_post['acsub'],
                      existing_post['sub'],
                      existing_post['setter'])
        list.append(ppp)
        i = i + 1
    print(len(list))
    # lol
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('problem_list.html', obj=list)

#*******************************************
#   ASIF AHMED*******************************
@app.route('/profile/<id>')
def profile(id):
    from profile import profileCall
    if not ('username' in session):
        return redirect(url_for("login"))
    user,form=profileCall(id)
    userNow = session['username']
    canEdit = 0
    if userNow == id or id == 'myself':
        canEdit = 1

    print(canEdit)
    return render_template('profile.html', form=form,user=user,canEdit=canEdit)


@app.route('/posts/<id>')
def posts(id):
    if not ('username' in session):
        return redirect(url_for('login'))

    from profile import profilePostCall
    post_array,user=profilePostCall(id)
    return render_template('user_post.html', post_array=post_array,user=user)


@app.route('/issues', methods=['GET', 'POST'])
def issues():
    from issue import issueCall
    form,issue_array = issueCall()
    return render_template('issues.html', form=form,issue_array=issue_array)


@app.route('/issues/<id>',methods=['GET', 'POST'])
def singleIssue(id):
    from issue import singleIssueCall
    form,comment_array,issue = singleIssueCall(id)
    return render_template('issue_page.html',form=form,comment_array=comment_array,issue=issue)


@app.route('/news')
def news():
    from newsScrapping import newsCall
    from newsStrategy import article_array
    article_array = []
    return render_template('news.html',article_array=newsCall())


@app.route('/submission/<id>')
def submissions(id):
    if not ('username' in session):
        return redirect(url_for('login'))
    from profile import profileSubmissionCall
    submission_array,user = profileSubmissionCall(id)
    return render_template('user_submission.html', submission_array=submission_array,user=user)

@app.route('/contests/<id>')
def userContests(id):
    from profile import profileContestsCall
    user= profileContestsCall(id)
    return render_template('user_contests.html',user=user)

@app.route('/issue/<id>')
def userIssues(id):
    from profile import profileIssueCall
    user,issue_array= profileIssueCall(id)
    return render_template('user_issues.html',user=user,issue_array=issue_array)


#   ASIF AHMED*******************************
# ***************************************************************************
dir_path = os.path.dirname(os.path.realpath(__file__))
languages = ["Java", "C", "Python"]
# CODEMIRROR_LANGUAGES = ['python','c']
#
# CODEMIRROR_THEME = 'base16-dark'
#
# CODEMIRROR_ADDONS = (
#
#     ('display', 'placeholder'),
#     ('hint', 'anyword-hint'),
#     ('hint', 'show-hint'),
#
# )
# app.config.from_object(__name__)
# codemirror = CodeMirror(app)
from codemirrorform import CodemirrorForm

def runPython(auxForm):
    pass
    # form = CodemirrorForm(auxForm)
    # text = form.source_code.data
    # now=time.time()
    # then=time.time()
    # fout = open(getProgramFileName("Python"), "w")
    # print(text, file=fout)
    # fout.close()
    #
    # if auxForm.get("custom_input") != None:
    #     inputs = form.inputs.data
    #     finputs = open(getCustomInputsFileName(), "w")
    #     print(inputs, file=finputs)
    #     finputs.close()
    #     now=time.time()
    #     os.system("python3 "+ getProgramFileName("Python")+" < "+getCustomInputsFileName()+" 1>"+
    #               getOutputFileName()+ " 2>"
    #               +getErrorFileName())
    #     then=time.time()
    #
    # else:
    #     now = time.time()
    #     os.system("python3 " + getProgramFileName(
    #         "Python") + " 1>" + getOutputFileName() + " 2>"
    #               + getErrorFileName())
    #     then = time.time()
    # finputs = open(getOutputFileName(), "r")
    # timeElapsed = then - now
    # outputs = finputs.readlines()
    # outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    # finputs.close()
    # finputs = open(getErrorFileName(), "r")
    # errors = finputs.readlines()
    # finputs.close()
    # #os.system("rm -r submissions/" + getUserId())
    # if len(errors) == 0:
    #     # print(outputs)
    #     return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    # else:
    #     print(errors)
    #     return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                            languages=languages)


def runJava(auxForm):
    pass
    # form = CodemirrorForm(auxForm)
    # text = form.source_code.data
    # now = time.time()
    # then = time.time()
    # fout = open(getProgramFileName("Java"), "w")
    # print(text, file=fout)
    # fout.close()
    # # compiling the program
    # os.system("javac "  + getProgramFileName("Java") + " 2>" + getErrorFileName())
    # # reading errors
    # finputs = open(getErrorFileName(), "r")
    # errors = finputs.readlines()
    # finputs.close()
    # print(errors)
    # # running with user defined inputs
    # if auxForm.get("custom_input") != None:
    #     inputs = form.inputs.data
    #     finputs = open(getCustomInputsFileName(), "w")
    #     print(inputs, file=finputs)
    #     finputs.close()
    #     if len(errors)==0:
    #         now = time.time()
    #         os.system("java -cp "+getExecutibleFileName("Java")+" Main <"+ getCustomInputsFileName() +
    #                   " 1> "+getOutputFileName()+ " 2> " +getErrorFileName())
    #         then= time.time()
    #     else:
    #         print(errors)
    #         #os.system("rm -r submissions/" + getUserId())
    #         return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                                languages=languages)
    # # running without inputs
    # else:
    #     if len(errors)==0:
    #         now = time.time()
    #         os.system("java -cp " + getExecutibleFileName("Java") + " Main " +" 1> " +
    #                   getOutputFileName() + " 2> " + getErrorFileName())
    #         then = time.time()
    #
    #     else:
    #         print(errors)
    #         #os.system("rm -r submissions/" + getUserId())
    #         return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                                languages=languages)
    # finputs = open(getOutputFileName(), "r")
    # outputs = finputs.readlines()
    # finputs.close()
    # timeElapsed = then - now
    # # outputs=list("")
    # outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    # finputs = open(getErrorFileName(), "r")
    # # print(finputs)
    # errors = finputs.readlines()
    # finputs.close()
    # #os.system("rm -r submissions/" + getUserId())
    # if len(errors) == 0:
    #     print(outputs)
    #     return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    # else:
    #     print(errors)
    #     return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                            languages=languages)
    #

def runC(auxForm):
    pass
    # form = CodemirrorForm(auxForm)
    # text = form.source_code.data
    # now = time.time()
    # then = time.time()
    # fout = open(getProgramFileName("C"), "w")
    # print(text, file=fout)
    # fout.close()
    # # compiling the program
    # os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
    # # reading errors
    # finputs = open(getErrorFileName(), "r")
    # errors = finputs.readlines()
    # finputs.close()
    # print(errors)
    # # running with user defined inputs
    # if auxForm.get("custom_input") != None:
    #     inputs = form.inputs.data
    #     finputs = open(getCustomInputsFileName(), "w")
    #     print(inputs, file=finputs)
    #     finputs.close()
    #     # checking for compile errors
    #     if len(errors) == 0:
    #         now=time.time()
    #         os.system(" ./"+ getExecutibleFileName("C") +" < "+getCustomInputsFileName()+
    #                   " 1> "+getOutputFileName()+" 2> "+getErrorFileName())
    #         then=time.time()
    #
    #     else:
    #         #os.system("rm -r submissions/" + getUserId())
    #         return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                                languages=languages)
    # # running without inputs
    # else:
    #     if len(errors) == 0:
    #         now=time.time()
    #         os.system(" ./" + getExecutibleFileName("C") +" 1> " + getOutputFileName() + " 2> " + getErrorFileName())
    #         then=time.time()
    #     else:
    #         #os.system("rm -r submissions/" + getUserId())
    #         return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                                languages=languages)
    # # reading program outputs
    # finputs = open(getOutputFileName(), "r")
    # outputs = finputs.readlines()
    # finputs.close()
    # timeElapsed = then - now
    # outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
    # # reading RTE
    # finputs = open(getErrorFileName(), "r")
    # errors = finputs.readlines()
    # finputs.close()
    # #os.system("rm -r submissions/" + getUserId())
    # # checking for RTE
    # if len(errors) == 0:
    #     print(outputs)
    #     return render_template('editor.html', form=form, status="Program Output", outputs=outputs, languages=languages)
    # else:
    #     print(errors)
    #     return render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
    #                            languages=languages)


#
# def getProblemSolution():
#     return 12
#
# def getProgramFileName(language):
#     if language=="Python":
#         return "submissions/" + getUserId() + "/" + getProblemId()+"/1.py"
#     elif language=="Java":
#         return "submissions/" + getUserId() + "/" + getProblemId() + "/Main.java"
#     else:
#         return "submissions/" + getUserId() + "/" + getProblemId()+"/1.cpp"
#
# def getExecutibleFileName(language):
#     if language=="Python":
#         return "submissions/" + getUserId() + "/" + getProblemId()+"/a"
#     elif language=="Java":
#         return "submissions/" + getUserId() + "/" + getProblemId()
#     else:
#         return "submissions/" + getUserId() + "/" + getProblemId()+"/a"
#
# def getOutputFileName():
#     return "submissions/" + getUserId() + "/" + getProblemId()+"/outputs/1.txt"
# def getErrorFileName():
#     return "submissions/" + getUserId() + "/" + getProblemId()+"/outputs/error.txt"
#
# def getCustomInputsFileName():
#     return "submissions/" + getUserId() + "/" + getProblemId()+"/custom_inputs/1.txt"
#
# def getUserId():
#     return session['username']
#
# def getProblemId():
#     return "TestProblem"
#
# def getExpectedOutputFileName(problemId):
#     return "static/uploads/"+problemId+"out1.txt"
#
# def getTestCaseFileName(problemId):
#     return "static/uploads/" + problemId + "in1.txt"
#
#
# def doesOutputMatch(userOutputFile,expectedOutputFile):
#     try:
#         userOutput=open(userOutputFile)
#     except:
#         return False
#     expectedOutput=open(expectedOutputFile)
#     for (x,y) in zip(userOutput.readlines(),expectedOutput.readlines()):
#         if x !=y:
#             userOutput.close()
#             expectedOutput.close()
#             return False
#     userOutput.close()
#     expectedOutput.close()
#     return True
#
#
# def makeSubmissionFolders():
#     os.system("mkdir submissions/" + getUserId())
#     os.system("mkdir submissions/" + getUserId() + "/" + getProblemId())
#     os.system("mkdir submissions/" + getUserId() + "/" + getProblemId()+"/outputs")
#     os.system("mkdir submissions/" + getUserId() + "/" + getProblemId() + "/custom_inputs")
#
# def runCode(form):
#     selectedLanguage = form.get('languages')
#     print(selectedLanguage)
#     makeSubmissionFolders()
#     from strategypatternforsubmission import RunJava,RunPython,RunC
#     if selectedLanguage == "Python":
#         runMode=RunPython()
#         # return runPython(form)
#     elif selectedLanguage == "C":
#         runMode=RunC()
#         # return runC(form)
#     elif selectedLanguage == "Java":
#         runMode=RunJava()
#         # return runJava(form)
#     return runMode.performRun(form)
#
# def submitCode(auxform,problemId):
#     selectedLanguage = auxform.get('languages')
#     print(selectedLanguage)
#     makeSubmissionFolders()
#     submissionInfo=dict()
#     submissionInfo["Language"]=selectedLanguage
#     submissionInfo["Submission Time"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#     form = CodemirrorForm(auxform)
#     text = form.source_code.data.replace("\t","    ")
#     submissionInfo["Code"] = text
#     now=time.time()
#     then=time.time()
#     fout = open(getProgramFileName(selectedLanguage), "w")
#     print(text, file=fout)
#     fout.close()
#     #compiling
#     if selectedLanguage=="Java":
#         os.system("javac " + getProgramFileName("Java") + " 2>" + getErrorFileName())
#     elif selectedLanguage=="C":
#         os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
#     # reading compile errors
#     if selectedLanguage!="Python":
#         finputs = open(getErrorFileName(), "r")
#         errors = finputs.readlines()
#         finputs.close()
#
#         if (len(errors) != 0):
#             print(errors)
#             submissionInfo["Comilation Status"] = "CE"
#             return submissionInfo
#     # running the program
#     if selectedLanguage=="Python":
#         now = time.time()
#         os.system("python3 " + getProgramFileName("Python") + " < " + getTestCaseFileName(problemId) + " 1>" +
#                   getOutputFileName() + " 2>" + getErrorFileName())
#         then = time.time()
#     elif selectedLanguage=="Java":
#         now = time.time()
#         os.system("java -cp " + getExecutibleFileName("Java") + " Main <" + getTestCaseFileName(problemId) +
#                   " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
#         then = time.time()
#     elif selectedLanguage=="C":
#         now = time.time()
#         os.system(" ./" + getExecutibleFileName("C") + " < " + getTestCaseFileName(problemId) +
#                   " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
#         then = time.time()
#
#     # reading runtime errors
#     finputs = open(getErrorFileName(), "r")
#     errors = finputs.readlines()
#     finputs.close()
#     if len(errors)!=0:
#         submissionInfo["Run Status"]="RTE"
#         return submissionInfo
#     timeElapsed=then-now
#     submissionInfo["Execution Time"]=timeElapsed
#     # if timeElapsed>2:
#     #     return "TLE"
#     if doesOutputMatch(getExpectedOutputFileName(problemId),getOutputFileName()) == False :
#         submissionInfo["Result Verdict"]="WA"
#         return submissionInfo
#     else:
#         submissionInfo["Result Verdict"] ="Passed"
#         return submissionInfo
#
#
# def cleanup():
#     os.system("rm -r submissions/" + getUserId())
#
# from bson.objectid import ObjectId
# def getProblemNumber(problemId,contestId):
#     print(ObjectId(contestId))
#     contest=mongo.db.contests.find({"_id": ObjectId(contestId)})[0]
#     problemList=contest.get('Problem ID')
#     for x in problemList:
#         for y,z in x.items():
#             if z==problemId:
#                 return y
#         # return x
#     print(problemList)
@app.route('/editor/<problemId>', methods=['GET', 'POST'])
def editor(problemId):

    print("not for contest")
    problemsDatabase=mongo.db.problems
    submissionDatabase=mongo.db.submissions
    problemsdb = ProblemsDatabase()
    if request.method == 'POST':
        if "run" in request.form:
            template = runCode(request.form)
            cleanup()
            return template

        elif "submit" in request.form:
            submitNormal = SubmitNormal()
            return submitNormal.performSubmit(problemId, request.form)

    return render_template('editor.html', form=CodemirrorForm(request.form), languages=languages)
@app.route('/editor/<contestId>/<problemId>', methods=['GET', 'POST'])
def contestEditor(problemId, contestId):
    problemsDatabase=mongo.db.problems
    submissionDatabase=mongo.db.submissions
    problemsdb=ProblemsDatabase()
    print("for contest")
    if request.method == 'POST':
        if "run" in request.form:
            template = runCode(request.form)
            cleanup()
            return template

        elif "submit" in request.form:
            from strategypatternforsubmission import SubmitContest
            id = list()
            id.append(problemId)
            id.append(contestId)
            submitContest = SubmitContest()
            submitContest.performSubmit(id, request.form)
            # submissionInfo=submitCode(request.form,problemId)
            # problemsdb.incrementSumissionCount(problemsDatabase,problemId)
            # print(submissionInfo)
            # problemTimeLimit=problemsDatabase.find_one({"myid":problemId}).get("time_limit")
            # verdict=dict()
            # verdict["Submission Time"]=submissionInfo.get("Submission Time")
            # verdict["Language"]=submissionInfo.get("Language")
            # if submissionInfo.get("Compilation Status") !=None:
            #     verdict["Status"]=submissionInfo.get("Compilation Status")
            # elif submissionInfo.get("Run Status")!=None:
            #     verdict["Status"]=submissionInfo.get("Run Status")
            # else:
            #     if float(problemTimeLimit)<float(submissionInfo.get("Execution Time")):
            #         verdict["Status"]="TLE"
            #     else:
            #         if submissionInfo.get("Result Verdict")=="Passed":
            #             verdict["Status"]="AC"
            #             problemsdb.incrementAcSumissionCount(problemsDatabase, problemId)
            #         else:
            #             verdict["Status"]="WA"
            # verdict["Execution Time"]=submissionInfo.get("Execution Time")
            # verdict["Problem Id"]=problemId
            # verdict["Problem Number"]=getProblemNumber(problemId,contestId)
            # verdict["User Id"]=session["username"]
            # verdict["Code"]=submissionInfo.get("Code")
            # verdict["Contest Id"]=contestId
            # verdict["Submission Id"]=uuid.uuid4().__str__()
            # submissionDatabase.insert(verdict)
            # return render_template('editor.html', form=CodemirrorForm(request.form), status=verdict.get("Status"),
            #                        languages=languages, check_submissions="Check Submissions")
    return render_template('editor.html', form=CodemirrorForm(request.form), languages=languages,check_submissions="Check Submissions")



from Submission import Submission

@app.route('/submissions',methods=['GET', 'POST'])
def view_submissions():
    submissionsDatabase=mongo.db.submissions
    problemsDatabase=mongo.db.problems
    print(submissionsDatabase)
    submissionsCursor = submissionsDatabase.find({}).limit(50).sort([('Submission Time', -1)])

    submissions=list()
    for submission in submissionsCursor:
        submissions.append(Submission(submission,problemsDatabase))
    for submission in submissions:
        print(submission.submissionTime)

    return render_template('submissions.html',submissions=submissions)

@app.route('/submissions/<submissionId>',methods=['GET', 'POST'])
def view_submission_details(submissionId):
    file = open("static/css/styles/styles.txt", "r")
    themes = list()
    for line in file:
        themes.append(line[:-1])
    file.close()
    # print(request.form)
    if request.form.get("themes") != None:
        preferedTheme = request.form.get("themes")
    else:
        preferedTheme = "atom-one-dark"
    submissionsDatabase = mongo.db.submissions
    submission=Submission(submissionsDatabase.find({"Submission Id":submissionId})[0],mongo.db.problems)
    language = str(submission.language).lower()
    return render_template('submitted_Code_viewer.html', submission=submission, language=language, themes=themes,
                           preferedTheme=preferedTheme)

@app.route('/user/<userName>',methods=['GET', 'POST'])
def userProfile(userName):
    class User:
        def __init__(self, name, username, mail):
            self.name = name
            self.username = username
            self.mail = mail
    users = mongo.db.userlist
    existing_user = users.find_one({'USERNAME': userName})
    user = User(existing_user['NAMES'], existing_user['USERNAME'], existing_user['MAIL'])
    return render_template('profile.html', user=user)
    
@app.route('/onlineide', methods=['GET', 'POST'])
def onlineide():
    if request.method == 'POST':
        if "run" in request.form:
            template = runCode(request.form)
            cleanup()
            print(CodemirrorForm(request.form).source_code.data)
            return template
    return render_template('editor.html', form=CodemirrorForm(request.form), languages=languages)


@app.route('/udebug', methods=['GET', 'POST'])
def problemList():
    problemsdb = mongo.db.problems
    list = []
    existing_posts = problemsdb.find({})
    i = 0
    for existing_post in existing_posts:
        ppp = problem(existing_post['sub_task_count'],
                      existing_post['myid'],
                      existing_post['pnt1'],
                      existing_post['pnt2'],
                      existing_post['pnt3'],
                      existing_post['time_limit'],
                      existing_post['memory_limit'],
                      existing_post['stylee'],
                      existing_post['name'],
                      existing_post['acsub'],
                      existing_post['sub'],
                      existing_post['setter'])
        list.append(ppp)
        i = i + 1
    print(len(list))
    # lol
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('problem_list_for_udebug.html', obj=list)


# def runForUbebug(inputs, text):
#     makeSubmissionFolders()
#     fout = open(getProgramFileName("C"), "w")
#     print(text, file=fout)
#     fout.close()
#     # compiling the program
#     os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
#     # reading errors
#     finputs = open(getErrorFileName(), "r")
#     errors = finputs.readlines()
#     finputs.close()
#     print(errors)
#     # running with user defined inputs
#     if True:
#         finputs = open(getCustomInputsFileName(), "w")
#         print(inputs, file=finputs)
#         finputs.close()
#         # checking for compile errors
#         if len(errors) == 0:
#
#             os.system(" ./" + getExecutibleFileName("C") + " < " + getCustomInputsFileName() +
#                       " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
#
#
#         else:
#             # os.system("rm -r submissions/" + getUserId())
#             return errors
#
#     # reading program outputs
#     finputs = open(getOutputFileName(), "r")
#     outputs = finputs.readlines()
#     finputs.close()
#     # reading RTE
#     finputs = open(getErrorFileName(), "r")
#     errors = finputs.readlines()
#     finputs.close()
#     # os.system("rm -r submissions/" + getUserId())
#     # checking for RTE
#     output = ""
#     cleanup()
#     for x in outputs:
#         output += x
#     if len(errors) == 0:
#         print(output)
#         return output
#     else:
#         print(errors)
#         return errors
#
#
# def getCode(filename):
#     codelist = open(filename).readlines()
#     code = ""
#     for x in codelist:
#         code += x + "\n"
#     return code
#
#
# def getInputFileListForUdebug(problemId):
#     os.system("cd static/inputs_for_udebug &&ls | grep " + problemId + ">" + getUserId() + ".txt")
#     return open("static/inputs_for_udebug/" + getUserId() + ".txt").readlines()
#
#
# def getInputsForUdebug(filename):
#     codelist = open(filename).readlines()
#     code = ""
#     for x in codelist:
#         code += x
#     return code
#
#
# def extractInputName(x, problemId):
#     return x.replace(problemId, "").replace(".txt", "")
#

@app.route('/udebug/<problemId>', methods=['GET', 'POST'])
def udebug(problemId):
    acceptedOutput = ""
    yourOutputs = ""
    inputs = ""
    mismatchNumber = -1
    results = list()
    inputFiles = getInputFileListForUdebug(problemId)
    selectedinputFile = ""
    usableInputFiles = list()
    for x in inputFiles:
        usableInputFiles.append(extractInputName(x, problemId))
    print(inputFiles)
    if "get_accepted_output_button" in request.form:
        acceptedOutput = request.form["accepted_output_textarea"]
        inputs = request.form["input_textarea"]
        code = getCode("static/solutions/" + problemId + ".c")
        acceptedOutput = runForUbebug(inputs, code)
        print(code)
        print(acceptedOutput)

    elif "compare_outputs_button" in request.form:
        print(request.form)
        acceptedOutput = request.form["accepted_output_textarea"]
        inputs = request.form["input_textarea"]
        yourOutputs = request.form["your_output_textarea"]
        code = getCode("static/solutions/" + problemId + ".c")
        acceptedOutput = runForUbebug(inputs, code)
        # print(code)
        # print(acceptedOutput)
        yourOutputList = list()
        acceptedOutputList = list()
        for x in acceptedOutput.split("\n"):
            if x == None:
                acceptedOutputList.append("")
            else:
                acceptedOutputList.append(x)
        for x in yourOutputs.split("\n"):
            if x == None:
                yourOutputList.append("")
            else:
                yourOutputList.append(x)
        acceptedOutputLineNumber = len(acceptedOutputList)
        yourOutputLineNumber = len(yourOutputList)
        if (len(acceptedOutputList) > len(yourOutputList)):
            for i in range(len(acceptedOutputList) - len(yourOutputList)):
                yourOutputList.append("")
        elif (len(acceptedOutputList) < len(yourOutputList)):
            for i in range(-len(acceptedOutputList) + len(yourOutputList)):
                acceptedOutputList.append("")
        outputpair = zip(acceptedOutputList, yourOutputList)
        mismatchNumber = 0
        for i, (x, y) in enumerate(outputpair):
            if x != y[:-1]:
                mismatchNumber += 1
                if (i < acceptedOutputLineNumber and i < yourOutputLineNumber):
                    results.append((int(i + 1), x, int(i + 1), y))
                elif (i < acceptedOutputLineNumber):
                    results.append((int(i + 1), x, "", y))
                else:
                    results.append(("", x, int(i + 1), y))
    if "inputstorer" in request.form and len(request.form["inputstorer"]) > 0:
        selectedinputFile = "static/inputs_for_udebug/" + problemId + str(request.form["inputstorer"]).replace("\n",
                                                                                                               "").replace(
            "\r", "").strip(" ") + ".txt"
        inputs = getInputsForUdebug(selectedinputFile)
    return render_template('udebug.html', selectedinput=inputs, acceptedOutput=acceptedOutput, yourOutput=yourOutputs,
                           results=results, mismatchNumber=mismatchNumber, inputs=usableInputFiles)





@app.route('/udebug', methods=['GET', 'POST'])
def problemList():
    problemsdb = mongo.db.problems
    list = []
    existing_posts = problemsdb.find({})
    i = 0
    for existing_post in existing_posts:
        ppp = problem(existing_post['sub_task_count'],
                      existing_post['myid'],
                      existing_post['pnt1'],
                      existing_post['pnt2'],
                      existing_post['pnt3'],
                      existing_post['time_limit'],
                      existing_post['memory_limit'],
                      existing_post['stylee'],
                      existing_post['name'],
                      existing_post['acsub'],
                      existing_post['sub'],
                      existing_post['setter'])
        list.append(ppp)
        i = i + 1
    print(len(list))
    # lol
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('problem_list_for_udebug.html', obj=list)


def runForUbebug(inputs, text):
    makeSubmissionFolders()
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
    if True:
        finputs = open(getCustomInputsFileName(), "w")
        print(inputs, file=finputs)
        finputs.close()
        # checking for compile errors
        if len(errors) == 0:

            os.system(" ./" + getExecutibleFileName("C") + " < " + getCustomInputsFileName() +
                      " 1> " + getOutputFileName() + " 2> " + getErrorFileName())


        else:
            # os.system("rm -r submissions/" + getUserId())
            return errors

    # reading program outputs
    finputs = open(getOutputFileName(), "r")
    outputs = finputs.readlines()
    finputs.close()
    # reading RTE
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    # os.system("rm -r submissions/" + getUserId())
    # checking for RTE
    output = ""
    cleanup()
    for x in outputs:
        output += x
    if len(errors) == 0:
        print(output)
        return output
    else:
        print(errors)
        return errors


def getCode(filename):
    codelist = open(filename).readlines()
    code = ""
    for x in codelist:
        code += x + "\n"
    return code


def getInputFileListForUdebug(problemId):
    os.system("cd static/inputs_for_udebug &&ls | grep " + problemId + ">" + getUserId() + ".txt")
    return open("static/inputs_for_udebug/" + getUserId() + ".txt").readlines()


def getInputsForUdebug(filename):
    codelist = open(filename).readlines()
    code = ""
    for x in codelist:
        code += x
    return code


def extractInputName(x, problemId):
    return x.replace(problemId, "").replace(".txt", "")


@app.route('/udebug/<problemId>', methods=['GET', 'POST'])
def udebug(problemId):
    acceptedOutput = ""
    yourOutputs = ""
    inputs = ""
    mismatchNumber = -1
    results = list()
    inputFiles = getInputFileListForUdebug(problemId)
    selectedinputFile = ""
    usableInputFiles = list()
    for x in inputFiles:
        usableInputFiles.append(extractInputName(x, problemId))
    print(inputFiles)
    if "get_accepted_output_button" in request.form:
        acceptedOutput = request.form["accepted_output_textarea"]
        inputs = request.form["input_textarea"]
        code = getCode("static/solutions/" + problemId + ".c")
        acceptedOutput = runForUbebug(inputs, code)
        print(code)
        print(acceptedOutput)

    elif "compare_outputs_button" in request.form:
        print(request.form)
        acceptedOutput = request.form["accepted_output_textarea"]
        inputs = request.form["input_textarea"]
        yourOutputs = request.form["your_output_textarea"]
        code = getCode("static/solutions/" + problemId + ".c")
        acceptedOutput = runForUbebug(inputs, code)
        # print(code)
        # print(acceptedOutput)
        yourOutputList = list()
        acceptedOutputList = list()
        for x in acceptedOutput.split("\n"):
            if x == None:
                acceptedOutputList.append("")
            else:
                acceptedOutputList.append(x)
        for x in yourOutputs.split("\n"):
            if x == None:
                yourOutputList.append("")
            else:
                yourOutputList.append(x)
        acceptedOutputLineNumber = len(acceptedOutputList)
        yourOutputLineNumber = len(yourOutputList)
        if (len(acceptedOutputList) > len(yourOutputList)):
            for i in range(len(acceptedOutputList) - len(yourOutputList)):
                yourOutputList.append("")
        elif (len(acceptedOutputList) < len(yourOutputList)):
            for i in range(-len(acceptedOutputList) + len(yourOutputList)):
                acceptedOutputList.append("")
        outputpair = zip(acceptedOutputList, yourOutputList)
        mismatchNumber = 0
        for i, (x, y) in enumerate(outputpair):
            if x != y[:-1]:
                mismatchNumber += 1
                if (i < acceptedOutputLineNumber and i < yourOutputLineNumber):
                    results.append((int(i + 1), x, int(i + 1), y))
                elif (i < acceptedOutputLineNumber):
                    results.append((int(i + 1), x, "", y))
                else:
                    results.append(("", x, int(i + 1), y))
    if "inputstorer" in request.form and len(request.form["inputstorer"]) > 0:
        selectedinputFile = "static/inputs_for_udebug/" + problemId + str(request.form["inputstorer"]).replace("\n",
                                                                                                               "").replace(
            "\r", "").strip(" ") + ".txt"
        inputs = getInputsForUdebug(selectedinputFile)
    return render_template('udebug.html', selectedinput=inputs, acceptedOutput=acceptedOutput, yourOutput=yourOutputs,
                           results=results, mismatchNumber=mismatchNumber, inputs=usableInputFiles)





# *****************************************************************************************

class Facade:

    def __init__(self):
        self.contest = Contest()

    def createContest(self,form,list):
        list=self.getProblemList()
        return self.contest.createContest(mongo,form,list)

    def getProblemList(self):
        problemdb = mongo.db.problems
        list = []
        existing_pbs = problemdb.find({})
        for existing_pb in existing_pbs:
            list.append(Create(existing_pb['myid'], existing_pb['name'], existing_pb['acsub'], existing_pb['sub'],
                                existing_pb['myid']))
        return list


@app.route('/contest',methods=['GET', 'POST'])
def contest():
    form = create_contest_form(request.form)
    facade= Facade()

    if request.method == 'POST':
        if facade.createContest(form,facade.getProblemList())==0:
            flash('You have to Choose at least 1 problem to set a contest.','failure')
            return render_template('create_contest.html',obj=facade.getProblemList(),form=form)
        else:
            return redirect(url_for('contests'))

    return render_template('create_contest.html',obj=facade.getProblemList(),form=form)
@app.route('/currentcontest/<contestID>/ranklist')
def ranklist(contestID):
    # #total_problem=['A','B','C','D','E','F']
    # submission_history=[{'name':'A','status':'AC','total_submission':3}]
    # submission_history.append({'name':'B','status':'WA','total_submission':2})
    # submission_history.append({'name': 'E', 'status': 'RTE', 'total_submission': 6})
    # submission_history.append({'name': 'C', 'status': 'WA', 'total_submission': 2})
    # submission_history.append({'name': 'D', 'status': 'TLE', 'total_submission': 2})
    # submission_history.append({'name': 'F', 'status': 'NS', 'total_submission': 0})
    # contestant1={'name':'SALAM','acc':3,'penalty':120,'submission_history':submission_history}
    # contestant2 = {'name': 'Borkot', 'acc': 2, 'penalty': 110, 'submission_history': submission_history}
    # Total_contestant=[contestant1,contestant2]
    Total_contestant=[]
    submission=mongo.db.submissions
    contestant_wise_submission=submission_formatter(submission,contestID)
    contests=mongo.db.contests
    contt=contests.find({'_id':ObjectId(contestID)})

    problem_cnt=0
    contestant_start_date=""
    contestant_start_time=""
    for cont in contt:
        problem_cnt=cont['Problem Count']
        contestant_start_date=cont['Start Date']
        contestant_start_time=cont['Start Time']
    print(problem_cnt)
    total_problem=problem_subname_generator(problem_cnt,submission.find({'Contest Id':contestID}))

    for eachcontestant in contestant_wise_submission:
        Total_contestant.append(contestant_wise_submission_formatter(eachcontestant,total_problem,contestant_start_date,contestant_start_time))

    return render_template('ranklist.html',total_problem=total_problem,Total_contestant=Total_contestant)

def problem_subname_generator(problem_cnt,all_submission):
    total=[]
    for i in range(0,problem_cnt):
        total.append(forward_letter('A',i))
    total_with_cnt=[]
    submission = []
    for each in all_submission:
        submission.append(each)
    for eachproblem in total:
        cnt=0
        ac_cnt=0
        for each in submission:
            if each['Problem Number']==eachproblem:
                cnt+=1
                if each['Status']=='AC':
                    ac_cnt+=1
            print(eachproblem)
        total_with_cnt.append({'problem_name':eachproblem, 'ac_cnt':ac_cnt,'total_cnt':cnt})
    return total_with_cnt

def submission_formatter(submission,contestID):
    contestant_wise_submission=[]
    User=[]
    total=0
    all_submission=submission.find({'Contest Id':contestID})
    for dict in all_submission:
        submissions=submission.find({'Contest Id':contestID,'User Id':dict["User Id"]})
        if dict['User Id'] not in User:
            contestant_wise_submission.append(submissions)
            User.append(dict['User Id'])

    return contestant_wise_submission

def contestant_wise_submission_formatter(submissions,total_problem,contest_start_date,contest_start_time):
    submission_history=[]
    penalty=0
    acc = 0
    name=""
    submission=[]
    for each in submissions:
            submission.append(each)
    for eachproblem in total_problem:

        each_prboblem_sub=[]
        for each in submission:
            if each['Problem Number']==eachproblem['problem_name']:
                each_prboblem_sub.append(each)

        status="NS"
        submission_time=0
        cnt=0
        execution_time=0
        all_submissions=[]
        for eachsub in each_prboblem_sub:
            all_submissions.append({'Status':eachsub['Status'], 'Submission_time':eachsub['Submission Time']})

        for eachsub in each_prboblem_sub:
            name=eachsub['User Id']
            if eachsub['Status'] =='AC':
                status='AC'
                submission_time=eachsub['Submission Time']
                acc+=1
                execution_time=eachsub['Execution Time']
                penalty+=20*cnt+execution_time*100-100
                cnt+=1
                break
            cnt+=1
            status=eachsub['Status']

        if submission_time!=0:
            dif=get_datetime_to_sec(submission_time,contest_start_date,contest_start_time)
            penalty+=dif/60

        submission_history.append({'name': eachproblem['problem_name'], 'status':status , 'total_submission': cnt ,'all_submissions':all_submissions})
    contestant = {'name': name, 'acc': acc, 'penalty': int(penalty), 'submission_history': submission_history}
    return contestant

def get_datetime_to_sec(submission_time,contest_start_date,contest_start_time):
    dt = submission_time.split()

    subd = dt[0].split('-')
    subt = dt[1].split(':')
    startd = contest_start_date.split('-')
    startt = contest_start_time.split(':')
    dt1 = datetime.datetime(int(subd[0]), int(subd[1]), int(subd[2]), int(subt[0]), int(subt[1]))
    dt2 = datetime.datetime(int(startd[0]), int(startd[1]), int(startd[2]), int(startt[0]), int(startt[1]))

    subsec = time.mktime(dt1.timetuple())
    startsec = time.mktime(dt2.timetuple())
    return  subsec-startsec

############################################


class contest:
    def __init__(self, c_id, title, start_date, start_time, end_time, IDs):
        self.c_id = c_id
        self.title = title
        self.start_date = start_date
        self.start_time = start_time
        self.end_time = end_time
        self.IDs = IDs


class contestdata:
    def __init__(self, c_id, title, time):
        self.c_id = c_id
        self.title = title
        self.time = time


@app.route('/contests')
def contests():
    contest_db = mongo.db.contests
    contest_list = []
    loaded_contests = contest_db.find({})
    for contest_curr in loaded_contests:
        time_string = contest_curr['Start Date'] + ' ' + contest_curr['Start Time']
        # time_obj = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
        subd = contest_curr['Start Date'].split('-')
        subt = contest_curr['Start Time'].split(':')
        dt1 = datetime.datetime(int(subd[0]), int(subd[1]), int(subd[2]), int(subt[0]), int(subt[1]))
        new_contest = contestdata(contest_curr['_id'],
                                  contest_curr['Contest Title'],
                                  dt1)
        contest_list.append(new_contest)
    contest_list.sort(key=lambda r: r.time, reverse=True)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('contests.html', obj=contest_list)

class PasswordForm(Form):
    password = StringField('Password')


# Password check for contest
@app.route('/contest/<id>/verify', methods=['GET', 'POST'])
def verify_contest(id):
    form = PasswordField(request.form)
    contest_db = mongo.db.contests
    contest_now = contest_db.find({"_id": ObjectId(id)})[0]
    c_pass = contest_now.get('Password')
    c_name = contest_now.get('Contest Title')
    print("p : " + c_pass)
    if not c_pass:
        print("no password")
        url = "http://127.0.0.1:5000/currentcontest/" + id + "/landing"
        return redirect(url, 302)
    if request.method == 'POST':
        password = request.form['password']
        print(password)
        print(c_pass)
        if c_pass == password:
            url = "http://127.0.0.1:5000/currentcontest/" + id + "/landing"
            return redirect(url, 302)
        else:
            error = "You need to enter the password for this contest"
            return render_template('contest_verify.html', error=error, form=form, name=c_name)
    else:
        return render_template('contest_verify.html', form=form, name=c_name)


# Contest Page
@app.route('/currentcontest/<cc_id>')
def load_contest(cc_id):
    contest_db = mongo.db.contests
    problem_db = mongo.db.problems
    contest_now = contest_db.find({"_id": ObjectId(cc_id)})[0]
    starting_datetime = contest_now.get('Start Date') + "T" + contest_now.get('Start Time') + ":00+06:00"
    ending_datetime = contest_now.get('Start Date') + "T" + contest_now.get('End Time') + ":00+06:00"
    cc_name = contest_now.get('Contest Title')
    print(starting_datetime)
    print(ending_datetime)
    problems = contest_now.get('Problem ID')
    problem_list = []
    for p in problems:
        for x, y in p.items():
            i = problem_db.find_one({'myid': y})
            print(i)
            new_prob = problem(i['sub_task_count'], i['myid'], i['pnt1'], i['pnt2'], i['pnt3'], i['time_limit'],
                               i['memory_limit'], i['stylee'], i['name'], i['acsub'], i['sub'], i['setter'])
            problem_list.append(new_prob)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('contest.html', obj=problem_list, id=cc_id, name=cc_name, sdto=starting_datetime,
                           edto=ending_datetime)


# Problem pages of contest
@app.route('/currentcontest/<contest_id>/<id2>')
def load_contest_problem(contest_id, id2):
    pbdb = mongo.db.problems
    pb = pbdb.find_one({'myid': id2})
    pbds = prob_struct(pb['name'], pb['time_limit'], pb['memory_limit'], id2)

    contest_db = mongo.db.contests
    contest_now = contest_db.find({"_id": ObjectId(contest_id)})[0]
    end_time = contest_now.get('Start Date') + "T" + contest_now.get('End Time') + ":00+06:00"
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template("problem_viewer.html", pdf_src='/static/uploads/' + id2 + '.pdf', pbds=pbds, cid=contest_id,
                           et=end_time)


# landing page if contest is not started yet
@app.route('/currentcontest/<contst_id>/landing')
def check_contest(contst_id):
    current_time = datetime.datetime.now()
    print(current_time)
    contest_db = mongo.db.contests
    contest_now = contest_db.find({"_id": ObjectId(contst_id)})[0]
    cc_name = contest_now.get('Contest Title')
    starting_datetime = contest_now.get('Start Date') + "T" + contest_now.get('Start Time') + ":00+06:00"
    time_string = contest_now.get('Start Date') + " " + contest_now.get('Start Time')
    start_time_p = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M")
    if not ('username' in session):
        return redirect(url_for('login'))
    if start_time_p < current_time:
        url = "http://127.0.0.1:5000/currentcontest/" + contst_id
        return redirect(url, 302)
    else:
        return render_template("contest_landing.html", cid=contst_id, st=starting_datetime, name=cc_name)


######################################################################################################

@app.route('/graph', methods=['GET', 'POST'])
def graphbuild():
    form=graph_input(request.form)
    if request.method=='POST':
        directed= True
        if request.form.get('choice')=='Undirected':
            directed= False
        if directed == True:
            idd=uuid.uuid4().__str__()
            fst=open('static/graph/samplestart.txt',"r")
            stst=fst.read()
            fed=open('static/graph/sampleend.txt',"r")
            sted=fed.read()
            f = open('templates/'+idd+'.html', "w+")
            f1 = open('templates/'+'checker.txt', "w+")
            print(stst,file=f)

            nd_list=FunctionList.node_list(st=form.nodes_desc.data.replace('\n', ' '), nd_cnt=form.nodes_cnt.data)
            ed_list=FunctionList.edge_list(st=form.ed_desc.data.replace('\n', ' '), ed_cnt=form.ed_cnt.data)
            gp=FunctionList.graph(nd_list, ed_list)
            ad=FunctionList.adapter(gp)
            js=FunctionList.jsonstring(ad)
            print(js.getstring(),file=f)

            print(sted,file=f)
            print(form.nodes_desc.data)
            f.close()
            return render_template(idd+'.html')
        else:
            idd = uuid.uuid4().__str__()
            fst = open('static/graph/undirectedstart.txt', "r")
            stst = fst.read()
            fed = open('static/graph/undirectedent.txt', "r")
            sted = fed.read()
            f = open('templates/' + idd + '.html', "w+")
            f1 = open('templates/' + 'checker.txt', "w+")
            print(stst, file=f)

            nd_list = FunctionList.node_list(st=form.nodes_desc.data.replace('\n', ' '), nd_cnt=form.nodes_cnt.data)
            ed_list = FunctionList.edge_list(st=form.ed_desc.data.replace('\n', ' '), ed_cnt=form.ed_cnt.data)
            sz=len(ed_list)
            for i in range(0,sz,2):
                if ed_list[i]<=ed_list[i+1]:
                    xx=ed_list[i]
                    ed_list[i]=ed_list[i+1]
                    ed_list[i+1]=xx
            gp = FunctionList.graph(nd_list, ed_list)
            ad = FunctionList.adapter(gp)
            js = FunctionList.jsonstring(ad)
            print(js.getstring(), file=f)

            print(sted, file=f)
            print(form.nodes_desc.data)
            f.close()
            return render_template(idd + '.html')

    return render_template('input_graph.html',form=form)
from ProblemsDatabase import ProblemsDatabase
@app.route('/test')
def test():
    problemsDatabase=ProblemsDatabase()
    problemsDatabase.incrementSumissionCount(mongo.db.problems,'ceed47bd-95a0-4297-bc75-6b46cc2b54c7')
    print("done")
    return "done"
if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'
    app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app) # uncomment this

    app.debug = True
    app.run()
