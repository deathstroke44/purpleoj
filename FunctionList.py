from app import *
import datetime
from Submission import *
from bson import ObjectId
import app
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
import ClassesList
A_CAT=set(['cpp'])
SC=set(['jpeg'])


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

class pair:
    def __init__(self,first,second,third):
        self.first=first
        self.second=second
        th=''
        for i in range(0,16):
            th+=first[i]
        for i in range(0,3):
            th+='.'
        self.third=third

class graphInterface:
    def getNodes(self):
        pass
    def getEdge(self):
        pass

class graph(graphInterface):
    def __init__(self,nodelist,edgelist):
        self.nodelist=nodelist
        self.edgelist=edgelist
    def getNodes(self):
        return self.nodelist
    def getEdge(self):
        return self.edgelist

class adapterInterface:
    def getjson(self):
        pass

class adapter(adapterInterface):
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in A_CAT

def problem_user_submissions(mongo,user_name,problem_id):
    submissionsDatabase = mongo.db.submissions
    submissionsCursor = submissionsDatabase.find({
        'User Id':user_name,
        'Problem Id':problem_id
    }).limit(10).sort([('Submission Time', 1)])
    submissions = list()
    for submission in submissionsCursor:
        submissions.append(pair(submission['Submission Id'], submission['Status'],submission['Submission Time']))
    print(user_name)
    print(len(submissions))
    print('omi')
    return submissions

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

def valid1(strr, request):
    if strr not in request.files:
        return False
    filee = request.files[strr]
    if filee.filename == '':
        return False
    if filee and allowed_file1(filee.filename):
        print("Something")
        return True
    return False

def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in SC

def valid2(strr, request):
    #lol
    if strr not in request.files:
        return False
    filee = request.files[strr]
    print(filee.filename+'omi')
    if filee.filename == '':
        return False
    if filee and allowed_file2(filee.filename):
        print("Something")
        return True
    return False

def problem_status(submission,contest_id, problem_id, user_id):
    any_submission=submission.find_one({'Contest Id':contest_id,"Problem Id":problem_id,'User Id':user_id})
    # print(any_submission)
    ac_submission=submission.find_one({'Contest Id':contest_id,"Problem Id":problem_id,'User Id':user_id,'Status': "AC"})
    # print(ac_submission)
    if any_submission == None:
        return "none"
    elif ac_submission == None:
        return "null"
    else:
        return "AC"


def get_my_submissions(submission_db,problems_db,contests_db,contestID,problemID,userID):
    my_submissions = submission_db.find({'Contest Id':contestID,"Problem Id":problemID,'User Id':userID}).sort([('Submission Time', -1)])
    submission_list = []
    for i in my_submissions:
        submission_list.append(ContestSubmission(i))
    name = problems_db.find({"myid":problemID})[0].get('name') + " Submissions"
    return name , submission_list


def get_contest_submissions(submission_db,problems_db,contests_db,contestID):
    submissions = submission_db.find({'Contest Id':contestID}).limit(50)
    # limit(50).sort([('Submission Time', -1)])
    submission_list = []
    for i in submissions:
        submission_list.append(Submission(i,problems_db))
    submission_list.sort(key=lambda d: datetime.datetime.strptime(d.submissionTime, '%Y-%m-%d %H:%M'), reverse=True)
    # print(submission_list)
    cursor = contests_db.find({"_id": ObjectId(contestID)})[0]
    name = cursor.get('Contest Title') + " Submissions"
    return name, submission_list


def get_clarifications(cntst_id):
    form = IssueForm()
    return "a"

    # problemsdb = mongo.db.problems
    # contestsdb = mongo.db.contests
    # clarificationsdb = mongo.db.clarifications
    #
    # existing_posts = problemsdb.find({}).sort('name')
    # i = 0;
    # list = []
    # problem_id_array = []
    # pair = (i, 'None')
    # list.append(pair)
    # problem_id_array.append('Contest')
    # contest_now = contestsdb.find({"_id": ObjectId(cntst_id)})[0]
    # problems = contest_now.get('Problem ID')
    # for p in problems:
    #     i = i + 1
    #     for x,y in p.items():
    #         prob = problemsdb.find_one({'myid': y})
    #         pair1 = (i, prob['name'])
    #         list.append(pair1)
    #         problem_id_array.append(y)
    #
    # form.problemName.choices = list
    #
    # if form.validate_on_submit():
    #     title = form.title.data
    #     problemName = form.problemName.data
    #     problemID = problem_id_array[problemName]
    #     print(problemID)
    #     text = form.text.data
    #     user_name = session['username']
    #     issueID = uuid.uuid1().__str__()
    #
    #     clarificationsdb.insert({'IssueID': issueID,
    #                              'UserName': user_name,
    #                              'Title': title,
    #                              'ProblemID': problemID,
    #                              'text': text,
    #                              'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    #                   'commentNumber': 0})
    #     # return redirect(url_for('issues'))
    #
    # issue_array = []
    # i = mongo.db.Issues
    # issuelist = i.find({}).sort('date', -1)
    # for issue in issuelist:
    #     if issue['ProblemID'] != 'CodeFlask':
    #         pb = problemsdb.find_one({'myid': issue['ProblemID']})
    #         issue_array.append(
    #             Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], pb['name'],
    #                   issue['text'], issue['date'] , issue['commentNumber']))
    #     else:
    #         issue_array.append(
    #             Issue(issue['IssueID'], issue['UserName'], issue['Title'], issue['ProblemID'], 'CodeFlask',
    #                   issue['text'], issue['date'],issue['commentNumber']))
    #
    # return form,issue_array




def UpcomingContests():
    contest_db = app.mongo.db.contests
    contest_cursor = contest_db.find({}).sort([['Start Date', 1], ['Start Time', 1]])
    pclist = []
    for pc in contest_cursor:
        starting_datetime = pc['Start Date'] + "T" + pc['Start Time'] + ":00+06:00"
        ending_date = pc['Start Date'] + "T" + pc['End Time'] + ":00+06:00"
        id = pc['_id']
        name = pc['Contest Title']
        dt = datetime.datetime.now()
        pcet = pc['End Time']
        rep = ''
        flag = 0
        for i in range(0, len(pcet)):
            if flag == 1:
                rep += pcet[i]
            if pcet[i] == '.':
                flag = 1
        pcet.replace(rep, '')
        ds = datetime.datetime.strptime(pc['Start Date'] + ' ' + pcet, "%Y-%m-%d %H:%M")
        xx = dt.strftime("%Y-%m-%d %H:%M")

        cd = datetime.datetime.strptime(xx, "%Y-%m-%d %H:%M")
        if ds >= dt:
            pclist.append(ClassesList.tripled(starting_datetime, ending_date, id, name))

    return pclist


