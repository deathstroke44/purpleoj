class Submission():
    def __init__(self,Dictionary,databaseCollection):
        self.problemId = Dictionary.get('Problem Id')
        self.submissionId = Dictionary.get("Submission Id")
        self.userName = Dictionary.get("User Id")
        self.language = Dictionary.get("Language")
        try:
            self.problemName=databaseCollection.find({'myid':self.problemId})[0].get('name')
        except:
            print("")
        self.verdict = Dictionary.get("Status")
        self.executionTime = Dictionary.get("Execution Time")
        self.submissionTime = Dictionary.get("Submission Time")
        self.Code=Dictionary.get("Code")


class ContestSubmission():
    def __init__(self,DictionaryCursor):
        self.submissionId = DictionaryCursor.get("Submission Id")
        self.language = DictionaryCursor.get("Language")
        self.verdict = DictionaryCursor.get("Status")
        self.executionTime = DictionaryCursor.get("Execution Time")
        self.submissionTime = DictionaryCursor.get("Submission Time")