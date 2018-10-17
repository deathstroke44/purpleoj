from flask import Flask, flash
from flask import request, redirect,url_for,render_template,session,Session
from flask_pymongo import PyMongo
from wtforms import Form,IntegerField,StringField, PasswordField, validators, FileField, FloatField,TextAreaField
from wtforms.widgets import TextArea
from werkzeug.utils import secure_filename
import datetime
import os
app = Flask(__name__)
UPLOAD_FOLDER = '/home/aniomi/PycharmProjects/purpleoj/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI']='mongodb://red44:omi123@ds131963.mlab.com:31963/purpleoj'
mongo = PyMongo(app)
import pymongo as pm
app.secret_key = "super secret key"
sess = Session()

class UploadForm(Form):
    name = StringField('name', [validators.DataRequired()])
    count = IntegerField('count', [validators.DataRequired()])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    nameform=UploadForm(request.form)
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
            return redirect(url_for('upload_file',filename=filename))
    return render_template('upload_problem.html',nameform=nameform)

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
        text = form.text.data
        dt=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        ppt = mongo.db.posts
        user_= session['username']
        #postt = postob(title=title,text=text,dt=dt,user_=user_)
        ppt.insert({
            'TITLE':title,
            'TEXT':text,
            'DATE':dt,
            'USER':user_
        })
    return render_template('create_post.html',form = form)

if __name__ == '__main__':
    app.secret_key = 'SUPER SECRET KEY'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)

    app.debug = True
    app.run()
