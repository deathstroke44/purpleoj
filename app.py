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

from forms import IssueForm, CommentForm
from newsScrapping import HackerRankMainPage, CodeForces, atcoder, topcoder, thecrazyprogrammer, LoadSoup

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class problem:
    def __init__(self, sub_task_count, id, pnt1, pnt2, pnt3, time_limit, memory_limit, stylee, name, acsub, sub,
                 setter):
        self.sub_task_count = sub_task_count
        self.pnt1 = pnt1
        self.pnt2 = pnt2
        self.pnt3 = pnt3
        self.id = id
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.stylee = stylee
        self.name = name
        self.acsub = acsub
        self.sub = sub
        self.setter = setter


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    nameform = UploadForm(request.form)
    if request.method == 'POST':
        # check if the post request has the file part
        sbcnt = nameform.count.data
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

        gpb = uuid.uuid4().__str__()
        file = request.files['file']
        filename = gpb + '.pdf'  # secure_filename(file.filename)
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
            'setter': session['username']
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


class postob:
    def __init__(self, xtitle, xtext, xdt, xuser_, xid_):
        self.title = xtitle
        self.text = xtext
        self.dt = xdt
        self.user_ = xuser_
        self.id_ = xid_


@app.route('/')
def index():
    list = []
    postdb = mongo.db.posts
    existing_post = postdb.find({}).sort('_id')
    i = 0
    for posts in existing_post:
        print(posts)
        posttitle = posts['TITLE']
        posttext = posts['TEXT']
        postuser = posts['USER']
        postdate = posts['DATE']
        postid = posts['_id']
        ppp = postob(posttitle, posttext, postdate, postuser, postid)
        list.append(ppp)
        print(list[i].dt)
        i = i + 1
        list.reverse()
    print(len(list))

    error = 'You are not logged in'
    dumb = 'dumb'
    if 'username' in session:
        msg = 'You are Logged in as ' + session['username']
        return render_template('home.html', msg=msg, posts=list)
    return render_template('home.html', error=error, dumb=dumb, posts=list)
    return 'Hello World!'


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=50)])
    email = EmailField('Email', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.Length(min=5,max=10),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        names = form.name.data
        emails = form.email.data
        usernames = form.username.data
        passwords = form.password.data
        user = mongo.db.userlist

        # db = connection['purpleoj']
        # db.authenticate('red44', 'red123456789')
        existing_user = user.find_one({'USERNAME': usernames})
        dialoge = 'Your Account Is created Successfully'
        if existing_user:
            dialoge = 'There is alredy an account in this username'
            return render_template('register.html', form=form, dialoge=dialoge)
        else:
            user.insert({'NAMES': names,
                         'USERNAME': usernames,
                         'MAIL': emails,
                         'PASSWORDS': passwords})
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


class create_article_form(Form):
    title = StringField('Post Title', [validators.DataRequired()])
    text = CKEditorField('Post Body', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


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


class prob_struct:
    def __init__(self, pn, tl, ml, id):
        self.pn = pn
        self.tl = 'Time Limit : ' + str(tl) + 'ms'
        self.ml = 'Memory Limit: ' + str(ml) + 'mb'
        self.id = id


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
    return render_template("pdfviewer.html", pdf_src='/static/uploads/' + id + '.pdf', pbds=pbds)


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


@app.route('/profile')
def profile():
    if not ('username' in session):
        return redirect(url_for('login'))

    class User:
        def __init__(self, name, username, mail):
            self.name = name
            self.username = username
            self.mail = mail

    user_name = session['username']
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': user_name})
    user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])
    return render_template('profile.html', user=user)


@app.route('/posts')
def posts():
    if not ('username' in session):
        return redirect(url_for('login'))

    class post_object:
        def __init__(self, title, text):
            self.title = title
            self.text = text

    post_array = []
    user_name = session['username']
    posts = mongo.db.posts.find({})
    for post in posts:
        if post['USER'] == user_name:
            post_array.append(post_object(post['TITLE'], post['TEXT']))

    return render_template('user_post.html', post_array=post_array)


@app.route('/issues', methods=['GET', 'POST'])
def issues(existing_post=None):

    class Issue:
        def __init__(self, id, username, title ,problemID,problemName,text,date):
            self.id = id
            self.username = username
            self.title = title
            self.problemID = problemID
            self.text = text
            self.problemName = problemName
            self.date = date

    form = IssueForm()
    if not ('username' in session):
        return redirect(url_for('login'))

    problemsdb = mongo.db.problems
    existing_posts = problemsdb.find({}).sort('name')
    i = 0;
    list = []
    problem_id_array = []
    pair = (i,'None')
    list.append(pair)
    problem_id_array.append('CodeFlask')
    for existing_post in existing_posts:
        i = i + 1
        pair1 = (i, existing_post['name'])
        list.append(pair1)
        problem_id_array.append(existing_post['myid'])

    form.problemName.choices = list

    if form.validate_on_submit():
        title = form.title.data
        problemName = form.problemName.data
        problemID = problem_id_array[problemName]
        print(problemID)
        text = form.text.data
        user_name = session['username']
        issueID = uuid.uuid1().__str__()

        issue = mongo.db.Issues
        issue.insert({'IssueID': issueID,
                      'UserName': user_name,
                      'Title': title,
                      'ProblemID': problemID,
                      'text': text,
                      'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
        return redirect(url_for('issues'))

    issue_array = []
    i = mongo.db.Issues
    issuelist = i.find({}).sort('date',-1)
    for issue in issuelist:
        if issue['ProblemID'] != 'CodeFlask':
            pb = problemsdb.find_one({'myid': issue['ProblemID']})
            issue_array.append(Issue(issue['IssueID'],issue['UserName'],issue['Title'],issue['ProblemID'],pb['name'],issue['text'],issue['date']))
        else:
            issue_array.append(
                Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], 'CodeFlask',
                      issue['text'], issue['date']))

    print(issue_array[0].title)
    return render_template('issues.html', form=form,issue_array=issue_array)


@app.route('/issues/<id>',methods=['GET', 'POST'])
def singleIssue(id):
    class Issue:
        def __init__(self, id, username, title ,problemID,problemName,text,date):
            self.id = id
            self.username = username
            self.title = title
            self.problemID = problemID
            self.text = text
            self.problemName = problemName
            self.date = date

    class Comment:
        def __init__(self, id, username, issue ,problemID,text,date):
            self.id = id
            self.username = username
            self.issue = issue
            self.problemID = problemID
            self.text = text
            self.date = date

    form = CommentForm()
    if not ('username' in session):
        return redirect(url_for('login'))

    if form.validate_on_submit():
        text = form.text.data
        commentID = uuid.uuid1().__str__()
        issueID = id
        problemID = mongo.db.Issues.find_one({'IssueID':issueID})['ProblemID']
        user_name = session['username']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        comments = mongo.db.Comment
        comments.insert({'ID':commentID,
                        'ProblemID':problemID,
                        'IssueID':issueID,
                        'UserName':user_name,
                        'Date':date,
                         'Text':text})
        return redirect(url_for('singleIssue', id=issueID))

    issue = mongo.db.Issues.find_one({'IssueID':id})
    problemsdb = mongo.db.problems
    problemName = ''
    if issue['ProblemID'] != 'CodeFlask':
        problemName = problemsdb.find_one({'myid': issue['ProblemID']})['name']
    else:
        problemName = 'CodeFlask'

    comment_array=[]
    comments = mongo.db.Comment.find({}).sort("Date",-1)
    for comment in comments:
        if id == comment['IssueID']:
            comment_array.append(Comment(comment['ID'],
                                         comment['UserName'],
                                         comment['IssueID'],
                                         comment['ProblemID'],
                                         comment['Text'],
                                         comment['Date']))

    return render_template('issue_page.html',form=form,comment_array=comment_array,
                           issue=Issue(issue['IssueID'],issue['UserName'],issue['Title'],
                                       issue['ProblemID'],problemName,issue['text'],issue['date'].split(" ")[0]))


@app.route('/news')
def news():
    class Article:
        def __init__(self, title_filename, content_filename):
            self.title_filename = title_filename
            self.content_filename = content_filename

    article_array = []
    #********
    # LoadRawHtmlFiles()  #Has to call this at a certain time of the day
    #******

    soup0, soup1, soup2, soup3, soup4, soup5, soup6 = LoadSoup()

    atcoderMain = soup0.find_all('div', class_='panel panel-default')
    atcoderPage2 = soup1.find_all('div', class_='panel panel-default')
    CodeForceMain = soup2.find_all('div', class_='topic')
    CodeForcePage2 = soup3.find_all('div', class_='topic')
    HackerRankMain = soup4.find_all('div', class_='blog-content')
    TopCoderMain = soup5.find_all('div', class_='story-content')
    thecrazyprogrammerMain = soup6.find_all('article')

    index = 0
    for i in HackerRankMain:
        file_name_title ,file_name_content= HackerRankMainPage(HackerRankMain[index])
        article_array.append(Article(file_name_title, file_name_content))
        index=index+1

    for i in CodeForceMain:
        file_name_title, file_name_content = CodeForces(i)
        article_array.append(Article(file_name_title,file_name_content))

    for i in TopCoderMain:
        file_name_title,file_name_content = topcoder(i)
        article_array.append(Article(file_name_title, file_name_content))

    for i in CodeForcePage2:
        file_name_title, file_name_content = CodeForces(i)
        article_array.append(Article(file_name_title, file_name_content))

    for i in atcoderMain:
        file_name_title, file_name_content = atcoder(i)
        article_array.append(Article(file_name_title, file_name_content))

    for i in thecrazyprogrammerMain:
        file_name_title,file_name_content = thecrazyprogrammer(i)
        article_array.append(Article(file_name_title, file_name_content))

    import random
    random.shuffle(article_array)
    print(article_array.__len__())
    return render_template('news.html', article_array=article_array)


@app.route('/submission')
def submissions():
    if not ('username' in session):
        return redirect(url_for('login'))

    class problem_object:
        def __init__(self, name, id):
            self.name = name
            self.id = id

    class submission_object:
        def __init__(self, pID, date, who, lan, verdict, time):
            self.pID = pID
            self.date = date
            self.who = who
            self.lan = lan
            self.verdict = verdict
            self.time = time

    submission_array = []
    user_name = session['username']
    submissions = mongo.db.submissions.find({})
    for submission in submissions:
        if submission['User Id'] == user_name:
            problem_set = mongo.db.problems.find_one({'myid': submission['Problem Id']})
            submission_array.append(submission_object(problem_object(problem_set['name'], problem_set['myid']),
                                                      submission['Submission Time'],
                                                      submission['User Id'], submission['Language'],
                                                      submission['Status'], submission['Execution Time']))

    print(submission_array)
    return render_template('user_submission.html', submission_array=submission_array)


# ***************************************************************************
dir_path = os.path.dirname(os.path.realpath(__file__))
languages = ["Java", "C", "Python"]
CODEMIRROR_LANGUAGES = ['python']

CODEMIRROR_THEME = 'base16-dark'

CODEMIRROR_ADDONS = (

    ('display', 'placeholder'),
    ('hint', 'anyword-hint'),
    ('hint', 'show-hint'),

)
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
    return session['username']

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

from bson.objectid import ObjectId
def getProblemNumber(problemId,contestId):
    print(ObjectId(contestId))
    contest=mongo.db.contests.find({"_id": ObjectId(contestId)})[0]
    problemList=contest.get('Problem ID')
    for x in problemList:
        for y,z in x.items():
            if z==problemId:
                return y
        # return x
    print(problemList)
@app.route('/editor/<problemId>', methods=['GET', 'POST'])
def editor(problemId):
    print("not for contest")
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
            print(submissionDatabase.insert(verdict))
            print(verdict)
            cleanup()
            return render_template('editor.html', form=MyForm(request.form), status=verdict.get("Status"),
                                   languages=languages,check_submissions="Check Submissions")
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
            verdict["Problem Number"]=getProblemNumber(problemId,contestId)
            verdict["User Id"]=session["username"]
            verdict["Code"]=submissionInfo.get("Code")
            verdict["Contest Id"]=contestId
            verdict["Submission Id"]=uuid.uuid4().__str__()
            submissionDatabase.insert(verdict)
            return render_template('editor.html', form=MyForm(request.form), status=verdict.get("Status"),
                                   languages=languages, check_submissions="Check Submissions")
    return render_template('editor.html', form=MyForm(request.form), languages=languages,check_submissions="Check Submissions")



from Submission import Submission

@app.route('/submissions',methods=['GET', 'POST'])
def view_submissions():
    submissionsDatabase=mongo.db.submissions
    problemsDatabase=mongo.db.problems
    print(submissionsDatabase)
    submissionsCursor=submissionsDatabase.find({}).limit(50) .sort([('Submission Time',1)])
    submissions=list()
    for submission in submissionsCursor:
        submissions.append(Submission(submission,problemsDatabase))
        print(submissions[0].submissionId)

    return render_template('submissions.html',submissions=submissions)

@app.route('/submissions/<submissionId>',methods=['GET', 'POST'])
def view_submission_details(submissionId):
    submissionsDatabase = mongo.db.submissions
    submission=Submission(submissionsDatabase.find({"Submission Id":submissionId})[0],mongo.db.problems)

    language = str(submission.language).lower()
    return render_template('submitted_Code_viewer.html', submission=submission, language=language)

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
            return template
    return render_template('editor.html', form=MyForm(request.form), languages=languages)


# *****************************************************************************************

class lol:
    def __init__(self,id,name,acc,sc,box):
        self.id=id
        self.name=name
        self.acc=acc
        self.sc=sc
        self.box=box

class create_contest_form(Form):
    contestname=StringField("Contest Name",[validators.DataRequired()])

def forward_letter(letter, positions):
    if letter.islower():
        unicode_point = ord('a')
    else:
        unicode_point = ord('A')
    start = ord(letter) - unicode_point
    offset = ((start + positions)) + unicode_point
    current_letter = chr(offset)
    return current_letter

@app.route('/contest',methods=['GET', 'POST'])
def contest():
    form = create_contest_form(request.form)

    problemdb=mongo.db.problems
    list=[]
    existing_pbs=problemdb.find({})
    for existing_pb in existing_pbs:
        list.append(lol(existing_pb['myid'],existing_pb['name'],existing_pb['acsub'],existing_pb['sub'],existing_pb['myid']))
    if request.method == 'POST':
        print(request.form[form.contestname.name])
        cnt=0;
        selected_problem_id=[]
        name='A'
        for prblm in list:
            if request.form.get(prblm.id):
                cnt+=1
                selected_problem_id.append({forward_letter(name,cnt-1):prblm.id});
                print(prblm.name)
        if cnt==0:
            flash('You have to Choose at least 1 problem to set a contest.','failure')
            return render_template('create_contest.html',obj=list,form=form)
        else:
            contests=mongo.db.contests
            contests.insert({'Contest Title':form.contestname.data,'Start Date':request.form['date'],
                             'Start Time':request.form['start_time'],'End Time':request.form['end_time'],
                             'Problem Count':cnt,'Problem ID':selected_problem_id})
            return redirect(url_for('contests'))

    return render_template('create_contest.html',obj=list,form=form)

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
    total_problem=problem_subname_generator(problem_cnt)

    for eachcontestant in contestant_wise_submission:
        Total_contestant.append(contestant_wise_submission_formatter(eachcontestant,total_problem,contestant_start_date,contestant_start_time))

    return render_template('ranklist.html',total_problem=total_problem,Total_contestant=Total_contestant)

def problem_subname_generator(problem_cnt):
    total=[]
    for i in range(0,problem_cnt):
        total.append(forward_letter('A',i))
    print(total)
    return total

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
            if each['Problem Number']==eachproblem:
                each_prboblem_sub.append(each)

        status="NS"
        submission_time=0
        cnt=0
        execution_time=0
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

        submission_history.append({'name': eachproblem, 'status':status , 'total_submission': cnt})
    contestant = {'name': name, 'acc': acc, 'penalty': int(dif+penalty), 'submission_history': submission_history}
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
        #time_obj = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
        subd = contest_curr['Start Date'].split('-')
        subt = contest_curr['Start Time'].split(':')
        dt1 = datetime.datetime(int(subd[0]), int(subd[1]), int(subd[2]), int(subt[0]), int(subt[1]))
        new_contest = contestdata(contest_curr['_id'],
                              contest_curr['Contest Title'],
                              dt1)
        contest_list.append(new_contest)
    contest_list.sort(key=lambda r:r.time, reverse=True)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('contests.html', obj=contest_list)

class PasswordForm(Form):
    password = StringField('Password')


# Password check for contest
@app.route('/contest/<id>/verify', methods=['GET', 'POST'])
def verify_contest(id):
    form = PasswordForm(request.form)
    contest_db = mongo.db.contests
    contest_now = contest_db.find({"_id": ObjectId(id)})[0]
    c_pass = contest_now.get('Password')
    c_name = contest_now.get('Contest Title')
    if request.method == 'POST':
        password = form.password.data
        print(password)
        print(c_pass)
        if c_pass == password:
            url = "http://127.0.0.1:5000/currentcontest/" + id
            return  redirect(url, 302)
        else:
            error = "You need to enter the password for this contest"
            return render_template('contest_verify.html', error=error, form=form)
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
            new_prob = problem(i['sub_task_count'], i['myid'], i['pnt1'], i['pnt2'], i['pnt3'], i['time_limit'],
                               i['memory_limit'], i['stylee'], x + ". " + i['name'], i['acsub'], i['sub'], i['setter'])
            problem_list.append(new_prob)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('contest.html', obj=problem_list, id=cc_id, name=cc_name, sdto=starting_datetime,
                           edto=ending_datetime)


# Problem pages of contest
@app.route('/currentcontest/<id1>/<id2>')
def load_contest_problem(id1, id2):
    pbdb = mongo.db.problems
    pb = pbdb.find_one({'myid': id2})
    pbds = prob_struct(pb['name'], pb['time_limit'], pb['memory_limit'], id2)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template("problem_viewer.html", pdf_src='/static/uploads/' + id2 + '.pdf', pbds=pbds, cid=id1)


######################################################################################################


#############################################
class graph_input(Form):
    nodes_cnt=IntegerField("Number of Nodes",[validators.DataRequired()])
    nodes_desc=TextAreaField("Nodes",[validators.DataRequired])
    ed_cnt=IntegerField("Number of Edgs",[validators.DataRequired()])
    ed_desc=TextAreaField("Edges",[validators.DataRequired()])


def givenode(node_name):
    node_name = node_name.replace('\n','')
    print(repr(node_name),end=' ')
    s='{ data: { id: '+ '\'' +node_name+ '\''+' } },'
    return s

def f(s):
    s = s.replace('\n','')
    return '\''+s+'\''

def giveedge(st,ed,ed_name):
    st = st.replace('\n','')
    ed = ed.replace('\n','')
    s='{\n'+'data: {\n'+'id: '+f(ed_name)+',\n'+'source : '+ f(st) +',\n'+'target: ' + f(ed) + ',\n}\n},\n'
    return s

def node_list(st,nd_cnt):
    st = st.replace('\n', ' ')
    st=st.replace('\r',' ')
    ar = st.split(' ')
    filter_list = []
    for i in range(0, len(ar)):
        if not (ar[i] == ''):
            filter_list.append(ar[i].replace('\n',''))
    filter_list2= []
    nd_cnt=min(nd_cnt,len(filter_list))
    for i in range(0, nd_cnt):
        filter_list2.append(filter_list[i])
    return filter_list2

def edge_list(st,ed_cnt):
    st=st.replace('\n',' ')
    st=st.replace('\r',' ')
    ar = st.split(' ')
    filter_list = []
    for i in range(0, len(ar)):
        if not (ar[i] == ''):
            filter_list.append(ar[i].replace('\n',''))
    ed_cnt*=2
    edcc=len(filter_list)
    for i in range(0,len(filter_list)):
        print(filter_list[i])

    if edcc%2==1:
        edcc-=1

    ed_cnt=min(edcc,ed_cnt)
    filter_list2=[]
    for i in range(0,ed_cnt):
        filter_list2.append(filter_list[i])
    return filter_list2

class graph:
    def __init__(self,nodelist,edgelist):
        self.nodelist=nodelist
        self.edgelist=edgelist
class adapter:
    graphh=None
    def __init__(self,graphh):
        self.graphh=graphh
        print(str(len(self.graphh.nodelist))+" omi")
    def getjson(self):
        jsonstring=''
        nodelen=len(self.graphh.nodelist)
        for i in range(0,nodelen):
            s=givenode(self.graphh.nodelist[i])
            jsonstring+='\n'
            jsonstring+=s
        edgelen = len(self.graphh.edgelist)
        for i in range(0, edgelen,2):
            s = giveedge(self.graphh.edgelist[i],self.graphh.edgelist[i+1],self.graphh.edgelist[i]+'#'+
                         self.graphh.edgelist[i+1])
            jsonstring += '\n'
            jsonstring += s
        return jsonstring
class jsonstring:
    _adapter=None
    def __init__(self,_adapter):
        self._adapter=_adapter
    def getstring(self):
        return self._adapter.getjson()


@app.route('/graph', methods=['GET', 'POST'])
def graphbuild():
    #return render_template('graphcheck.html')
    #print(givenode('a'))
    #print(giveedge('a','b','ab'))
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

            nd_list=node_list(st=form.nodes_desc.data.replace('\n',' '),nd_cnt=form.nodes_cnt.data)
            ed_list=edge_list(st=form.ed_desc.data.replace('\n',' '),ed_cnt=form.ed_cnt.data)
            gp=graph(nd_list,ed_list)
            ad=adapter(gp)
            js=jsonstring(ad)
            print(js.getstring(),file=f)
            #f.close()
            #for i in range (0,len(nd_list)):
            #    print(givenode(nd_list[i]),file=f)
            #for i in range (0,len(ed_list),2):
            #    print(giveedge(ed_list[i],ed_list[i+1],ed_list[i]+'#'+ed_list[i+1]),file=f)
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

            nd_list = node_list(st=form.nodes_desc.data.replace('\n', ' '), nd_cnt=form.nodes_cnt.data)
            ed_list = edge_list(st=form.ed_desc.data.replace('\n', ' '), ed_cnt=form.ed_cnt.data)
            sz=len(ed_list)
            for i in range(0,sz,2):
                if ed_list[i]<=ed_list[i+1]:
                    xx=ed_list[i]
                    ed_list[i]=ed_list[i+1]
                    ed_list[i+1]=xx
            gp = graph(nd_list, ed_list)
            ad = adapter(gp)
            js = jsonstring(ad)
            print(js.getstring(), file=f)
            # f.close()
            # for i in range (0,len(nd_list)):
            #    print(givenode(nd_list[i]),file=f)
            # for i in range (0,len(ed_list),2):
            #    print(giveedge(ed_list[i],ed_list[i+1],ed_list[i]+'#'+ed_list[i+1]),file=f)
            print(sted, file=f)
            print(form.nodes_desc.data)
            f.close()
            return render_template(idd + '.html')

    return render_template('input_graph.html',form=form)

if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'
    app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app) # uncomment this

    app.debug = True
    app.run()
