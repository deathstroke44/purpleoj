from flask import session, url_for,request
from werkzeug.utils import redirect
from forms import UpdateProfileForm

from app import mongo
from issue import Issue
from bson.objectid import ObjectId
import app


class User:
    def __init__(self, name, username, mail):
        self.name = name
        self.username = username
        self.mail = mail


def profileCall(id):
    user_name = session['username']
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': id})
    if id == 'myself':
        exiting_user = users.find_one({'USERNAME': user_name})
        user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])
    else:
        user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])

    form = UpdateProfileForm(request.form)
    if form.validate_on_submit():
        users.update_one(
            {'USERNAME':user_name},
            {
                '$set':
                    {
                        'NAMES':form.name.data,
                        'PASSWORDS':form.password.data
                    }
            }
        )
        #print(request.files['userpic'])
        app.upload_picture(request=request,user=session['username'])

    return user,form,request


def profilePostCall(id):
    class post_object:
        def __init__(self, title, text):
            self.title = title
            self.text = text

    post_array = []
    user_name = id
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': user_name})
    user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])

    posts = mongo.db.posts.find({})
    for post in posts:
        if post['USER'] == user_name:
            post_array.append(post_object(post['TITLE'], "/"+post['TEXT']))

    return post_array,user

def profileSubmissionCall(id):
    class problem_object:
        def __init__(self, name, id):
            self.name = name
            self.id = id

    class submission_object:
        def __init__(self, sID,pID, date, who, lan, verdict, time):
            self.sID = sID
            self.pID = pID
            self.date = date
            self.who = who
            self.lan = lan
            self.verdict = verdict
            self.time = time

    submission_array = []
    user_name = id
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': user_name})
    user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])
    submissions = mongo.db.submissions.find({})
    for submission in submissions:
        if submission['User Id'] == user_name:
            problem_set = mongo.db.problems.find_one({'myid': submission['Problem Id']})
            submission_array.append(submission_object(submission['Submission Id'],
                                                      problem_object(problem_set['name'], problem_set['myid']),
                                                      submission['Submission Time'],
                                                      submission['User Id'],
                                                      submission['Language'],
                                                      submission['Status'],
                                                      submission['Execution Time']))

    return submission_array,user


def profileContestsCall(id):
    class contest_object:
        def __init__(self, title, id):
            self.title = title
            self.id = id

    contest_array=[]
    user_name = id
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': user_name})
    user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])

    submissions = mongo.db.submissions.find({})
    contests = mongo.db.contests
    contestId_array=[]
    for submission in submissions:
        if submission['Contest Id'] != '' and submission['User Id'] == id and  submission['Contest Id'] not in contestId_array:
            contestId = submission['Contest Id']
            contestTitle = contests.find({"_id": ObjectId(contestId)})[0].get('Contest Title')
            contest = contest_object(contestTitle,contestId)
            contest_array.append(contest)
            contestId_array.append(contestId)

    return user,contest_array


def profileIssueCall(id):
    user_name = id
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': user_name})
    user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])

    issue_array = []
    i = mongo.db.Issues
    issuelist = i.find({}).sort('date', -1)
    problemsdb = mongo.db.problems
    for issue in issuelist:
        if issue['UserName'] == id:
            if issue['ProblemID'] != 'CodeFlask':
                pb = problemsdb.find_one({'myid': issue['ProblemID']})
                issue_array.append(
                    Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], pb['name'],
                          issue['text'], issue['date'], issue['commentNumber']))
            else:
                issue_array.append(
                    Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], 'CodeFlask',
                          issue['text'], issue['date'], issue['commentNumber']))

    return user, issue_array
