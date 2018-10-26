from flask import Flask, flash
from flask import request, redirect, url_for, render_template, session, Session
from flask_pymongo import PyMongo
from wtforms import Form, IntegerField, StringField, PasswordField, validators, FileField, FloatField, TextAreaField
from wtforms.widgets import TextArea
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor, CKEditorField
import requests
from bs4 import BeautifulSoup
from wtforms.fields.html5 import EmailField
import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/home/aniomi/PycharmProjects/purpleoj/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
ALLOWED_CATEGORY = set(['ACM', 'IOI'])
import uuid

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = 'mongodb://red44:omi123@ds131963.mlab.com:31963/purpleoj'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
ckeditor = CKEditor(app)
mongo = PyMongo(app)
import pymongo as pm

app.secret_key = "super secret key"
sess = Session()


class UploadForm(Form):
    time_limit = IntegerField("Time limit(ms)", [validators.DataRequired()])
    memory_limit = IntegerField("Memory Limit(MB)", [validators.DataRequired()])
    category = StringField("Problem Style(ACM,IOI)", [validators.DataRequired()])
    name = StringField('Problem name', [validators.DataRequired()])
    count = IntegerField('Number Of subtask(at least 1 at most 3)', [validators.DataRequired()] and [validators.number_range(1, 3)])
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
    existing_post = postdb.find({})
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


@app.route('/news')
def news():
    class Article:
        def __init__(self, title_filename, content_filename):
            self.title_filename = title_filename
            self.content_filename = content_filename

    article_array = []
    source0 = requests.get('https://atcoder.jp/').text
    source1 = requests.get('https://atcoder.jp/?p=2').text
    source2 = requests.get('http://codeforces.com/').text
    source3 = requests.get('http://codeforces.com/page/2').text
    source4 = requests.get('https://csacademy.com/blog/ceoi-2018/').text

    soup0 = BeautifulSoup(source0, 'lxml')
    soup1 = BeautifulSoup(source1, 'lxml')
    soup2 = BeautifulSoup(source2, 'lxml')
    soup3 = BeautifulSoup(source3, 'lxml')
    soup4 = BeautifulSoup(source4, 'lxml')

    div0 = soup0.find_all('div', class_='panel panel-default')
    div1 = soup1.find_all('div', class_='panel panel-default')
    div2 = soup2.find_all('div', class_='topic')
    div3 = soup3.find_all('div', class_='topic')

    for i in div2:
        title = i.find('div', class_='title')
        content = i.find('div', class_='ttypography')
        content2 = content

        uid1 = uuid.uuid1()
        file_name_title = 'static/news/' + str(uid1) + '.html'
        f = open(file_name_title, 'a', encoding='utf8')
        f.write(str(title).replace('<p>', '').replace('</p>', '').replace('div', 'h4').replace(title.a['href'],
                                                                                               'http://codeforces.com/' +
                                                                                               title.a['href']))
        f.close()

        print(title.a['href'])

        for a in content.find_all('img'):
            if a:
                imageSource = a['src']
                st = 'http'
                if imageSource.find(st) == -1:
                    content = str(content).replace(imageSource, 'http://codeforces.com/' + imageSource)

        for link in content2.find_all('a'):
            if link:
                linkSource = link['href']
                st = 'http'
                if linkSource.find(st) == -1:
                    content = str(content).replace(linkSource, 'http://codeforces.com/' + linkSource)

        uid2 = uuid.uuid1()
        file_name_content = 'static/news/' + str(uid2) + '.html'
        f = open(file_name_content, 'a', encoding='utf8')
        f.write(str(content))
        f.close()

        article_array.append(Article(file_name_title, file_name_content))
        # print(content)

    for i in div3:
        title = i.find('div', class_='title')
        content = i.find('div', class_='ttypography')
        # content = reformatContent(content)

        uid1 = uuid.uuid1()
        file_name_title = 'static/news/' + str(uid1) + '.html'
        f = open(file_name_title, 'a', encoding='utf8')
        f.write(str(title).replace('<p>', '').replace('</p>', ''))
        f.close()

        for a in content.find_all('img'):
            if a:
                imageSource = a['src']
                st = 'http'
                if imageSource.find(st) == -1:
                    content = str(content).replace(imageSource, 'http://codeforces.com/' + imageSource)
                    print(a['src'])

        uid2 = uuid.uuid1()
        file_name_content = 'static/news/' + str(uid2) + '.html'
        f = open(file_name_content, 'a', encoding='utf8')
        f.write(str(content))
        f.close()

        article_array.append(Article(file_name_title, file_name_content))
        # print(content)

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
            submission_array.append(submission_object(problem_object(problem_set['name'], problem_set['myid']), submission['Submission Time'],
                                                      submission['User Id'], submission['Language'],
                                                      submission['Status'], submission['Execution Time']))

    print(submission_array)
    return render_template('user_submission.html', submission_array=submission_array)


if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'
    app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app) # uncomment this

    app.debug = True
    app.run()
