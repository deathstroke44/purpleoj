from flask import session, url_for
from werkzeug.utils import redirect

from app import mongo


class User:
    def __init__(self, name, username, mail):
        self.name = name
        self.username = username
        self.mail = mail


def profileCall():
    user_name = session['username']
    users = mongo.db.userlist
    exiting_user = users.find_one({'USERNAME': user_name})
    user = User(exiting_user['NAMES'], exiting_user['USERNAME'], exiting_user['MAIL'])

    return user


def profilePostCall():
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

    return post_array

def profileSubmissionCall():
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
    user_name = session['username']
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

    return submission_array
