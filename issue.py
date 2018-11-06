import datetime
import uuid

from flask import url_for, session
from werkzeug.utils import redirect

from app import mongo
from forms import IssueForm, CommentForm


class Issue:
    def __init__(self, id, username, title ,problemID, problemName, text, date,commentNumber):
        self.id = id
        self.username = username
        self.title = title
        self.problemID = problemID
        self.text = text
        self.problemName = problemName
        self.date = date
        self.commentNumber = commentNumber


class Comment:
    def __init__(self, id, username, issue ,problemID,text,date):
        self.id = id
        self.username = username
        self.issue = issue
        self.problemID = problemID
        self.text = text
        self.date = date


def issueCall():
    form = IssueForm()
    if not ('username' in session):
        return redirect(url_for('login'))

    problemsdb = mongo.db.problems
    existing_posts = problemsdb.find({}).sort('name')
    i = 0;
    list = []
    problem_id_array = []
    pair = (i, 'None')
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
                      'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                      'commentNumber': 0})
        # return redirect(url_for('issues'))

    issue_array = []
    i = mongo.db.Issues
    issuelist = i.find({}).sort('date', -1)
    for issue in issuelist:
        if issue['ProblemID'] != 'CodeFlask':
            pb = problemsdb.find_one({'myid': issue['ProblemID']})
            issue_array.append(
                Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], pb['name'],
                      issue['text'], issue['date'] , issue['commentNumber']))
        else:
            issue_array.append(
                Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], 'CodeFlask',
                      issue['text'], issue['date'],issue['commentNumber']))

    return form,issue_array


def singleIssueCall(id):
    form = CommentForm()
    if not ('username' in session):
        return redirect(url_for('login'))

    if form.validate_on_submit():
        text = form.text.data
        commentID = uuid.uuid1().__str__()
        issueID = id
        problemID = mongo.db.Issues.find_one({'IssueID': issueID})['ProblemID']
        user_name = session['username']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        issueToChange = mongo.db.Issues
        number = issueToChange.find_one({'IssueID': issueID})['commentNumber']
        issueToChange.update_one(
            {'IssueID': issueID},
            {
                '$set': {'commentNumber': number + 1}
            }
        )

        comments = mongo.db.Comment
        comments.insert({'ID': commentID,
                         'ProblemID': problemID,
                         'IssueID': issueID,
                         'UserName': user_name,
                         'Date': date,
                         'Text': text})
        # return redirect(url_for('singleIssue', id=issueID))

    issue = mongo.db.Issues.find_one({'IssueID': id})
    problemsdb = mongo.db.problems
    problemName = ''
    if issue['ProblemID'] != 'CodeFlask':
        problemName = problemsdb.find_one({'myid': issue['ProblemID']})['name']
    else:
        problemName = 'CodeFlask'

    comment_array = []
    comments = mongo.db.Comment.find({}).sort("Date", -1)
    for comment in comments:
        if id == comment['IssueID']:
            comment_array.append(Comment(comment['ID'],
                                         comment['UserName'],
                                         comment['IssueID'],
                                         comment['ProblemID'],
                                         comment['Text'],
                                         comment['Date']))

    issue = Issue(issue['IssueID'], issue['UserName'], issue['Title'],
                  issue['ProblemID'], problemName, issue['text'], issue['date'].split(" ")[0],issue['commentNumber'])

    return form,comment_array, issue