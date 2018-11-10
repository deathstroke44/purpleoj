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
import FunctionList
from FunctionList import allowed_file1,giveedge,givenode,edge_list,node_list,f,allowed_file,graph,adapter,jsonstring,problem_user_submissions,pair,valid,valid1,valid2
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

PDF=set(['pdf'])
TXT=set(['txt'])

def upload_picture(request,user):
    print('reach')
    if valid2(strr='userpic',request=request):
        print('reach')
        file = request.files['userpic']
        print(file.filename)
        filename = user + '.jpeg'  # secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def allowed_file_pdf(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in PDF

def allowed_file_txt(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in TXT


def pdfvalid(strr, request):
    if strr not in request.files:
        return False
    filee = request.files[strr]
    if filee.filename == '':
        return False
    if filee and allowed_file_pdf(filee.filename):
        print("Something")
        return True
    return False


def txtvalid(strr, request):
    if strr not in request.files:
        return False
    filee = request.files[strr]
    if filee.filename == '':
        return False
    if filee and allowed_file_txt(filee.filename):
        print("Something")
        return True
    return False


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    nameform = UploadForm(request.form)
    if request.method == 'POST' and nameform.validate():
        # check if the post request has the file part
        sbcnt = int(request.form.get('cnt'))
        if not pdfvalid(strr='file', request=request):
            return render_template('upload_problem.html', error='WA', nameform=nameform)
        if sbcnt >= 1:
            if not txtvalid(strr='ifile1', request=request) or not txtvalid(strr='ofile1',
                                                                      request=request) or nameform.point1.data == None:
                return render_template('upload_problem.html',error='WA',nameform=nameform)
        if sbcnt >= 2:
            if not txtvalid(strr='ifile2', request=request) or not txtvalid(strr='ofile2',
                                                                      request=request) or nameform.point2.data == None:
                return render_template('upload_problem.html',error='WA',nameform=nameform)
        if sbcnt >= 3:
            if not txtvalid(strr='ifile3', request=request) or not txtvalid(strr='ofile3',
                                                                      request=request) or nameform.point3.data == None:
                return render_template('upload_problem.html', error='WA',nameform=nameform)
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
        return render_template('upload_problem.html',error='AC',nameform=nameform)
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
    print("lllllllllllllllll")
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
    contest_cursor=contest_db.find({}).sort([['Start Date', 1], ['Start Time', 1]])
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
    if request.method == 'POST' and form.validate():
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
    print("hello world")
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
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
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('problem_list.html', obj=list)

#*******************************************
#   ASIF AHMED*******************************
@app.route('/profile/<id>',methods=['GET', 'POST'])
def profile(id):
    from profile import profileCall
    if not ('username' in session):
        return redirect(url_for("login"))
    user,form,request=profileCall(id)
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
    article_array,pclist=newsCall()
    return render_template('news.html',article_array=article_array,PC=pclist)


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
    user,contest_array= profileContestsCall(id)
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
@app.route('/editor/<problemId>', methods=['GET', 'POST'])
def editor(problemId):
    print("not for contest")
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
            print("submitting")
            return submitContest.performSubmit(id, request.form)
    return render_template('editor.html', form=CodemirrorForm(request.form), languages=languages,check_submissions="Check Submissions")
@app.route('/submissions',methods=['GET', 'POST'])
def view_submissions():
    import UtilityFunctionsForSubmissionList
    return UtilityFunctionsForSubmissionList.submissions()
@app.route('/submissions/<submissionId>',methods=['GET', 'POST'])
def view_submission_details(submissionId):
    import UtilityFunctionsForSubmissionList
    return UtilityFunctionsForSubmissionList.viewOneSubmissions(submissionId, request.form)
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
    return render_template('editor.html', form=CodemirrorForm(request.form), languages=languages,
                           check_submissions="false")
@app.route('/udebug', methods=['GET', 'POST'])
def problemList():
    problemsdb = mongo.db.problems
    list = []
    existing_posts = problemsdb.find({'checker': True})
    print(existing_posts)
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
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('problem_list_for_udebug.html', obj=list)
@app.route('/udebug/<problemId>', methods=['GET', 'POST'])
def udebug(problemId):
    from UtilityFunctionsForUdebug import udebugUtil
    return udebugUtil(problemId, request.form)
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
    # print(problem_cnt)
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
            # print(eachproblem)
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
                penalty+=20*cnt+execution_time*100
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
    # print("p : " + c_pass)
    if not c_pass:
        # print("no password")
        url = "http://127.0.0.1:5000/currentcontest/" + id + "/landing"
        return redirect(url, 302)
    if request.method == 'POST':
        password = request.form['password']
        # print(password)
        # print(c_pass)
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
    all_submission = mongo.db.submissions
    contest_now = contest_db.find({"_id": ObjectId(cc_id)})[0]
    starting_datetime = contest_now.get('Start Date') + "T" + contest_now.get('Start Time') + ":00+06:00"
    ending_datetime = contest_now.get('Start Date') + "T" + contest_now.get('End Time') + ":00+06:00"
    cc_name = contest_now.get('Contest Title')
    # print(starting_datetime)
    # print(ending_datetime)
    problems = contest_now.get('Problem ID')
    problem_list = []
    for p in problems:
        for x, y in p.items():
            i = problem_db.find_one({'myid': y})
            # print(i)
            status = FunctionList.problem_status(all_submission,cc_id,i['myid'],session["username"])
            new_prob = problem(i['sub_task_count'], i['myid'], i['pnt1'], i['pnt2'], i['pnt3'], i['time_limit'],
                               i['memory_limit'], i['stylee'], x + ".    " + i['name'], i['acsub'], status, i['setter'])
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
    # print(current_time)
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


# clarification
@app.route('/currentcontest/<cntst_id>/clarifications')
def clarifications(cntst_id):
    pass
    # plist = FunctionList.get_clarifications(cntst_id)
    # return render_template("clarifications.html",selectmenu=plist,clarifications=plist)


# add new clarification
@app.route('/currentcontest/<cntest_id>/clarifications/add', methods=['GET', 'POST'])
def new_clarification(cntest_id):
    pass


# submissions of an individual problem in a contest
@app.route('/submissions/<contestID>/<problemID>')
def show_my_contest(contestID,problemID):
    submission_db = mongo.db.submissions
    problems_db = mongo.db.problems
    contests_db = mongo.db.contests
    name, submission_list = FunctionList.get_my_submissions(submission_db,problems_db,contests_db,contestID,problemID,session["username"])
    return render_template("contest_submissions.html",title=name, submissions=submission_list)

# all submissions of a contest
@app.route('/currentcontest/<cntst_id>/submissions')
def show_contest_submissions(cntst_id):
    submission_db = mongo.db.submissions
    problems_db = mongo.db.problems
    contests_db = mongo.db.contests
    name, submission_list = FunctionList.get_contest_submissions(submission_db,problems_db,contests_db,cntst_id)
    return render_template("submissions.html",title=name, submissions=submission_list)


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
