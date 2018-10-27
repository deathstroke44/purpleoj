from bson import ObjectId
from flask import Flask, flash
from flask import request, redirect,url_for,render_template,session,Session
from flask_pymongo import PyMongo
from wtforms import Form,IntegerField,StringField, PasswordField, validators, FileField, FloatField,TextAreaField
from wtforms.widgets import TextArea
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor, CKEditorField

from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/home/aniomi/PycharmProjects/purpleoj/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
ALLOWED_CATEGORY=set(['ACM','IOI'])
import uuid
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI']='mongodb://red44:omi123@ds131963.mlab.com:31963/purpleoj'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400


ckeditor = CKEditor(app)
mongo = PyMongo(app)
import pymongo as pm
app.secret_key = "super secret key"
sess = Session()

class UploadForm(Form):
    time_limit = IntegerField("Time limit(ms)",[validators.DataRequired()])
    memory_limit = IntegerField("Memory Limit(MB)",[validators.DataRequired()])
    category = StringField("Problem Style(ACM,IOI)",[validators.DataRequired()])
    name = StringField('Problem name', [validators.DataRequired()])
    count = IntegerField('Number Of subtask(at least 1 at most 2)', [validators.DataRequired()])
    point1 = IntegerField('Point for Subtask 1')
    point2 = IntegerField('Point for Subtask 2')
    point3 = IntegerField('Point for Subtask 3')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class problem:
    def __init__(self,sub_task_count,id,pnt1,pnt2,pnt3,time_limit,memory_limit,stylee,name,acsub,sub,setter):
        self.sub_task_count=sub_task_count
        self.pnt1=pnt1
        self.pnt2=pnt2
        self.pnt3=pnt3
        self.id=id
        self.time_limit=time_limit
        self.memory_limit=memory_limit
        self.stylee=stylee
        self.name=name
        self.acsub= acsub
        self.sub= sub
        self.setter=setter


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    nameform=UploadForm(request.form)
    if request.method == 'POST':
        # check if the post request has the file part
        sbcnt=nameform.count.data
        if not valid(strr='file',request=request):
            return redirect(request.url)
        if sbcnt>=1:
            if not valid(strr='ifile1', request=request) or not valid(strr='ofile1', request=request) or nameform.point1.data==None:
                return redirect(request.url)
        if sbcnt>=2:
            if not valid(strr='ifile2', request=request) or not valid(strr='ofile2', request=request) or nameform.point2.data==None:
                return redirect(request.url)
        if sbcnt>=3:
            if not valid(strr='ifile3', request=request) or not valid(strr='ofile3', request=request) or nameform.point3.data==None:
                return redirect(request.url)

        gpb=uuid.uuid4().__str__()
        file= request.files['file']
        filename = gpb+'.pdf'#secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        for i in range(1,sbcnt+1):
            inp='ifile'+str(i)
            out='ofile'+str(i)
            file=request.files[inp]
            filename=gpb+'in'+str(i)+'.txt'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = request.files[out]
            filename = gpb + 'out' + str(i) + '.txt'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pnt1 ,pnt2,pnt3=0,0,0
        if not nameform.point1 == None:
            pnt1=nameform.point1.data
        if not nameform.point1 == None:
            pnt2=nameform.point2.data
        if not nameform.point1 == None:
            pnt3=nameform.point3.data

        pb=problem(sbcnt,gpb,pnt1,pnt2,pnt3,nameform.time_limit.data,nameform.memory_limit.data,nameform.category.data,nameform.name.data,0,0,session['username'])
        problemdb=mongo.db.problems
        problemdb.insert({
            'sub_task_count': pb.sub_task_count,
            'myid': pb.id,
            'pnt1':pb.pnt1,
            'pnt2':pb.pnt2,
            'pnt3':pb.pnt3,
            'author':session['username'],
            'name':nameform.name.data,
            'time_limit':pb.time_limit,
            'memory_limit':pb.memory_limit,
            'stylee':pb.stylee,
            'acsub':0,
            'sub':0,
            'setter':session['username']
        })

        return redirect(url_for('upload_file', filename=filename))


    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('upload_problem.html',nameform=nameform)


def valid(strr,request):
    if strr not in request.files:
        return False
    filee= request.files[strr]
    if filee.filename=='':
        return  False
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
    def __init__(self,xtitle, xtext, xdt, xuser_, xid_):
        self.title = xtitle
        self.text = xtext
        self.dt = xdt
        self.user_ = xuser_
        self.id_ = xid_

@app.route('/')
def index():
    list =[]
    postdb = mongo.db.posts
    existing_post= postdb.find({})
    i=0
    for posts in existing_post:
        print(posts)
        posttitle=posts['TITLE']
        posttext=posts['TEXT']
        postuser=posts['USER']
        postdate=posts['DATE']
        postid=posts['_id']
        ppp=postob(posttitle,posttext,postdate,postuser,postid)
        list.append(ppp)
        print(list[i].dt)
        i=i+1
    print(len(list))

    error = 'You are not logged in'
    dumb = 'dumb'
    if 'username' in session:
        msg = 'You are Logged in as ' + session['username']
        return render_template('home.html', msg=msg,posts=list)
    return render_template('home.html', error=error, dumb=dumb,posts=list)
    return 'Hello World!'

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
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

        #db = connection['purpleoj']
        #db.authenticate('red44', 'red123456789')
        existing_user = user.find_one({'USERNAME': usernames})
        dialoge= 'Your Account Is created Successfully'
        if existing_user:
            dialoge='There is alredy an account in this username'
            return render_template('register.html',form=form,dialoge=dialoge)
        else:
            user.insert({'NAMES' : names,
                         'USERNAME': usernames,
                         'MAIL': emails,
                         'PASSWORDS': passwords})
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

class create_article_form(Form):
    title = StringField(u'title',[validators.DataRequired()])
    text = TextAreaField(u'text',[validators.DataRequired()])

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
                return  redirect(url_for('index'))
            else:
                error='You are not logged in';
                if 'username' in session:
                    msg= 'You are Logged in as ' + session['username']
                dialogue = 'Wrong Password'
                #flash('Wrong password','error')
                if 'username' in session:
                    return render_template('login.html', msg=msg, form=form,dialogue=dialogue)

                return render_template('login.html', error=error, form=form, dialogue=dialogue)
        else:
            app.logger.info('No User')
            error = 'No such username exist'
            if 'username' in session:
                msg = 'You are Logged in as ' + session['username']
            if 'username' in session:
                return render_template('login.html', msg=msg, form=form, dialogue=error)
            #flash('Wrong Usename Or password', error)
            return render_template('login.html', error=error, form=form, dialogue=error)
    elif 'username' in session:
        msg = 'You are Logged in as ' + session['username']
        return render_template('login.html', msg=msg, form=form)
    else:
        error = 'You are not logged in'
        dialogue='Wrong password'
        return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/post',  methods=['GET', 'POST'])
def post():
    form = create_article_form(request.form)

    if request.method == 'POST':
        title= form.title.data
        print("Reach")
        text = form.text.data
        dt=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        ppt = mongo.db.posts
        user_= session['username']
        gpb = uuid.uuid4().__str__()
        gpb='static/posts/'+gpb+'.html'
        f=open(gpb,"w")
        print(text,file=f)
        f.close()
        #postt = postob(title=title,text=text,dt=dt,user_=user_)
        ppt.insert({
            'TITLE':title,
            'TEXT':gpb,
            'DATE':dt,
            'USER':user_
        })
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('create_post.html',form = form)

class prob_struct:
    def __init__(self,pn,tl,ml,id):
        self.pn=pn
        self.tl='Time Limit : '+str(tl)+'ms'
        self.ml='Memory Limit: '+str(ml)+'mb'
        self.id=id
@app.route('/about/<id>/submit/')
def prob_submit(id):
    return 'Submit '+id

@app.route('/about/<id>/')
def pdfviewers(id):
    pbdb=mongo.db.problems
    pb=pbdb.find_one({'myid': id})
    pbds=prob_struct(pb['name'],pb['time_limit'],pb['memory_limit'],id)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template("pdfviewer.html", pdf_src='/static/uploads/'+id+'.pdf',pbds=pbds)

@app.route('/about')
def postab():
    problemsdb=mongo.db.problems
    list = []
    existing_posts = problemsdb.find({})
    i = 0
    for existing_post in existing_posts:
        ppp= problem(existing_post['sub_task_count'],
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
    #lol
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('problem_list.html',obj=list)

#############################################################################################################
#-------------------                         CONTEST PART                                   ----------------#
#############################################################################################################


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
        time_obj = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
        new_contest = contestdata(contest_curr['_id'],
                              contest_curr['Contest Title'],
                              time_obj)
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
            new_prob = problem(i['sub_task_count'],i['myid'],i['pnt1'],i['pnt2'],i['pnt3'],i['time_limit'],
                               i['memory_limit'],i['stylee'],x+". "+i['name'],i['acsub'],i['sub'],i['setter'])
            problem_list.append(new_prob)
    if not ('username' in session):
        return redirect(url_for('login'))
    return render_template('contest.html', obj=problem_list,id=cc_id,name=cc_name,sdto=starting_datetime,edto=ending_datetime)


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


if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'
    app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app) # uncomment this

    app.debug = True
    app.run()


