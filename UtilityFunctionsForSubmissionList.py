import app
from Submission import Submission


def submissions():
    submissionsDatabase = app.mongo.db.submissions
    problemsDatabase = app.mongo.db.problems
    print(submissionsDatabase)
    submissionsCursor = submissionsDatabase.find({}).limit(100).sort([('Submission Time', -1)])

    submissions = list()
    for submission in submissionsCursor:
        submissions.append(Submission(submission, problemsDatabase))
    for submission in submissions:
        print(submission.submissionTime)

    return app.render_template('submissions.html', submissions=submissions)


def viewOneSubmissions(submissionId, form):
    file = open("static/css/styles/styles.txt", "r")
    themes = list()
    for line in file:
        themes.append(line[:-1])
    file.close()

    if form.get("themes") != None:
        preferedTheme = form.get("themes")
    else:
        preferedTheme = "atom-one-dark"
    submissionsDatabase = app.mongo.db.submissions
    submission = Submission(submissionsDatabase.find({"Submission Id": submissionId})[0], app.mongo.db.problems)
    language = str(submission.language).lower()
    return app.render_template('submitted_Code_viewer.html', submission=submission, language=language, themes=themes,
                               preferedTheme=preferedTheme)
