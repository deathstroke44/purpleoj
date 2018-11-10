import abc
import multiprocessing

from UtilityFunctionsForEditor import *
import app
import uuid
from ProblemsDatabase import ProblemsDatabase


def getProblemNumber(problemId, contestId):
    print(ObjectId(contestId))
    contest = app.mongo.db.contests.find({"_id": ObjectId(contestId)})[0]
    problemList = contest.get('Problem ID')
    for x in problemList:
        for y, z in x.items():
            if z == problemId:
                return y
        # return x


def submitCode(auxform, problemId):
    selectedLanguage = auxform.get('languages')
    print(selectedLanguage)
    makeSubmissionFolders()
    submissionInfo = dict()
    submissionInfo["Language"] = selectedLanguage
    submissionInfo["Submission Time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    form = CodemirrorForm(auxform)
    text = form.source_code.data.replace("\t", "    ")
    submissionInfo["Code"] = text
    now = time.time()
    then = time.time()
    fout = open(getProgramFileName(selectedLanguage), "w")
    print(text, file=fout)
    fout.close()
    # compiling
    if selectedLanguage == "Java":
        os.system("javac " + getProgramFileName("Java") + " 2>" + getErrorFileName())
    elif selectedLanguage == "C":
        os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
    # reading compile errors
    if selectedLanguage != "Python":
        finputs = open(getErrorFileName(), "r")
        errors = finputs.readlines()
        finputs.close()

        if (len(errors) != 0):
            print(errors)
            submissionInfo["Compilation Status"] = "CE"
            return submissionInfo
    # running the program
    args = dict()
    args["type"] = "submit"
    args["problem id"] = problemId
    if selectedLanguage == "Python":
        args["language"] = "Python"
        # now = time.time()
        # os.system("python3 " + getProgramFileName("Python") + " < " + getTestCaseFileName(problemId) + " 1>" +
        #           getOutputFileName() + " 2>" + getErrorFileName())
        # then = time.time()
    elif selectedLanguage == "Java":
        args["language"] = "Java"
        # now = time.time()
        # os.system("java -cp " + getExecutibleFileName("Java") + " Main <" + getTestCaseFileName(problemId) +
        #           " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        # then = time.time()
    elif selectedLanguage == "C":
        args["language"] = "C"
        # now = time.time()
        # os.system(" ./" + getExecutibleFileName("C") + " < " + getTestCaseFileName(problemId) +
        #           " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        # then = time.time()
    # reading runtime errors
    (type, status) = runWithCoverage(args)
    if type == "status":
        submissionInfo["Run Status"] = "TLE"
        submissionInfo["Execution Time"] = "Inf"
        return submissionInfo
    else:
        (now, then) = (type, status)
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    if len(errors) != 0:
        submissionInfo["Run Status"] = "RTE"
        return submissionInfo
    timeElapsed = then - now
    submissionInfo["Execution Time"] = timeElapsed
    # if timeElapsed>2:
    #     return "TLE"
    if doesOutputMatch(getExpectedOutputFileName(problemId), getOutputFileName()) == False:
        submissionInfo["Result Verdict"] = "WA"
        return submissionInfo
    else:
        submissionInfo["Result Verdict"] = "Passed"
        return submissionInfo


class Editor():

    def performSubmit(self, id, auxFrom):
        return self.submitStrategy.submit(self, id, auxFrom)

    def performRun(self, auxForm):
        return self.runStrategy.run(self, auxForm)

    def __init__(self, submitStrategy, runStrategy):
        self.submitStrategy = submitStrategy
        self.runStrategy = runStrategy


class SubmitNormal(Editor):
    def __init__(self):
        super(SubmitNormal, self).__init__(SubmitNormalStrategy, None)


class SubmitContest(Editor):
    def __init__(self):
        super(SubmitContest, self).__init__(SubmitForContestStrategy, None)


class RunC(Editor):
    def __init__(self):
        super(RunC, self).__init__(None, RunCStrategy)


class RunPython(Editor):
    def __init__(self):
        super(RunPython, self).__init__(None, RunPythonStrategy)


class RunJava(Editor):
    def __init__(self):
        super(RunJava, self).__init__(None, RunJavaStrategy)


class SubmitStrategy(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def submit(self, id, auxFrom):
        pass


class SubmitForContestStrategy(SubmitStrategy):
    def submit(self, id, auxFrom):
        problemId = id[0]
        contestId = id[1]
        problemsDatabase = app.mongo.db.problems
        submissionDatabase = app.mongo.db.submissions
        problemsdb = ProblemsDatabase()
        submissionInfo = submitCode(auxFrom, problemId)
        problemsdb.incrementSumissionCount(problemsDatabase, problemId)
        print(submissionInfo)
        problemTimeLimit = problemsDatabase.find_one({"myid": problemId}).get("time_limit")
        verdict = dict()
        verdict["Submission Time"] = submissionInfo.get("Submission Time")
        verdict["Language"] = submissionInfo.get("Language")
        if submissionInfo.get("Compilation Status") != None:
            verdict["Status"] = submissionInfo.get("Compilation Status")
        elif submissionInfo.get("Run Status") != None:
            verdict["Status"] = submissionInfo.get("Run Status")
            print("problemTimeLimit" + problemTimeLimit, submissionInfo.get("Execution Time"))

        else:
            print(problemTimeLimit, submissionInfo.get("Execution Time"))
            if float(problemTimeLimit) < float(submissionInfo.get("Execution Time")) * 1000:
                verdict["Status"] = "TLE"
            else:
                if submissionInfo.get("Result Verdict") == "Passed":
                    verdict["Status"] = "AC"
                    problemsdb.incrementAcSumissionCount(problemsDatabase, problemId)
                else:
                    verdict["Status"] = "WA"
        verdict["Execution Time"] = submissionInfo.get("Execution Time")
        verdict["Problem Id"] = problemId
        verdict["Problem Number"] = getProblemNumber(problemId, contestId)
        verdict["User Id"] = session["username"]
        verdict["Code"] = submissionInfo.get("Code")
        verdict["Contest Id"] = contestId
        verdict["Submission Id"] = uuid.uuid4().__str__()
        submissionDatabase.insert(verdict)
        return app.render_template('editor.html', form=CodemirrorForm(auxFrom), status=verdict.get("Status"),
                                   languages=app.languages, check_submissions="Check Submissions",
                                   submissionId=verdict["Submission Id"])


class SubmitNormalStrategy(SubmitStrategy):
    def submit(self, problemId, auxFrom):
        print(problemId)
        print("not for contest")
        problemsDatabase = app.mongo.db.problems
        submissionDatabase = app.mongo.db.submissions
        problemsdb = ProblemsDatabase()
        submissionInfo = submitCode(auxFrom, problemId)
        problemsdb.incrementSumissionCount(problemsDatabase, problemId)
        print(submissionInfo)
        problemTimeLimit = problemsDatabase.find_one({"myid": problemId}).get("time_limit")
        verdict = dict()
        verdict["Submission Time"] = submissionInfo.get("Submission Time")
        verdict["Language"] = submissionInfo.get("Language")
        if submissionInfo.get("Compilation Status") != None:
            verdict["Status"] = submissionInfo.get("Compilation Status")
        elif submissionInfo.get("Run Status") != None:
            verdict["Status"] = submissionInfo.get("Run Status")
        else:
            if float(problemTimeLimit) < float(submissionInfo.get("Execution Time")) * 1000:
                verdict["Status"] = "TLE"
            else:
                if submissionInfo.get("Result Verdict") == "Passed":
                    verdict["Status"] = "AC"
                    problemsdb.incrementAcSumissionCount(problemsDatabase, problemId)
                else:
                    verdict["Status"] = "WA"
        verdict["Execution Time"] = submissionInfo.get("Execution Time")
        verdict["Problem Id"] = problemId
        verdict["User Id"] = session["username"]
        verdict["Code"] = submissionInfo.get("Code")
        verdict["Contest Id"] = ""
        verdict["Submission Id"] = uuid.uuid4().__str__()
        print(submissionDatabase.insert(verdict))
        print(verdict)
        cleanup()
        print(verdict.get("Status"))
        return app.render_template('editor.html', form=CodemirrorForm(auxFrom), status=verdict.get("Status"),
                                   languages=app.languages, check_submissions="Check Submissions",
                                   submissionId=verdict["Submission Id"])


class RunStrategy(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self, auxFrom):
        pass


class RunCStrategy(RunStrategy):
    def run(self, auxForm):
        form = CodemirrorForm(auxForm)
        text = form.source_code.data
        now = time.time()
        then = time.time()
        fout = open(getProgramFileName("C"), "w")
        print(text, file=fout)
        fout.close()
        # compiling the program
        os.system(" g++ -o " + getExecutibleFileName("C") + " " + getProgramFileName("C") + " 2>" + getErrorFileName())
        # reading errors
        finputs = open(getErrorFileName(), "r")
        errors = finputs.readlines()
        finputs.close()
        print(errors)
        # running with user defined inputs
        if auxForm.get("custom_input") != None:
            inputs = form.inputs.data
            finputs = open(getCustomInputsFileName(), "w")
            print(inputs, file=finputs)
            finputs.close()
            # checking for compile errors
            if len(errors) == 0:

                # now = time.time()
                # os.system(" ./" + getExecutibleFileName("C") + " < " + getCustomInputsFileName() +
                #           " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
                # then = time.time()
                args = dict()
                args["language"] = "C"
                args["type"] = "with custom inputs"
                (type, status) = runWithCoverage(args)
                if (type == "status"):
                    status = "Program has been terminated after running for 5 seconds.\nThis maybe due to an infinity loop or waiting for an input. "
                    return app.render_template('editor.html', form=form, status=status,
                                               languages=app.languages)
                else:
                    (now, then) = (type, status)
            else:
                # os.system("rm -r submissions/" + getUserId())
                return app.render_template('editor.html', form=form, status="Program Compiled with errors",
                                           outputs=errors,
                                           languages=app.languages)
        # running without inputs
        else:
            if len(errors) == 0:
                # now = time.time()
                # os.system(
                #     " ./" + getExecutibleFileName("C") + " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
                # then = time.time()
                args = dict()
                args["language"] = "C"
                args["type"] = "without custom inputs"
                (type, status) = runWithCoverage(args)
                if (type == "status"):
                    status = "Program has been terminated after running for 5 seconds.\nThis maybe due to an infinity loop or waiting for an input. "
                    return app.render_template('editor.html', form=form, status=status,
                                               languages=app.languages)
                else:
                    (now, then) = (type, status)


            else:
                # os.system("rm -r submissions/" + getUserId())
                return app.render_template('editor.html', form=form, status="Program Compiled with errors",
                                           outputs=errors,
                                           languages=app.languages)
        # reading program outputs
        finputs = open(getOutputFileName(), "r")
        outputs = finputs.readlines()
        finputs.close()
        timeElapsed = then - now
        outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
        # reading RTE
        finputs = open(getErrorFileName(), "r")
        errors = finputs.readlines()
        finputs.close()
        # os.system("rm -r submissions/" + getUserId())
        # checking for RTE
        if len(errors) == 0:
            print(outputs)
            return app.render_template('editor.html', form=form, status="Program Output", outputs=outputs,
                                       languages=app.languages)
        else:
            print(errors)
            return app.render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                       languages=app.languages)


class RunPythonStrategy(RunStrategy):
    def run(self, auxForm):
        form = CodemirrorForm(auxForm)
        text = form.source_code.data
        now = time.time()
        then = time.time()
        timeout = False
        fout = open(getProgramFileName("Python"), "w")
        print(text, file=fout)
        fout.close()

        if auxForm.get("custom_input") != None:
            inputs = form.inputs.data
            finputs = open(getCustomInputsFileName(), "w")
            print(inputs, file=finputs)
            finputs.close()
            now = time.time()
            args = dict()
            args["language"] = "Python"
            args["type"] = "with custom inputs"
            (type, status) = runWithCoverage(args)
            if (type == "status"):
                status = "Program has been terminated after running for 5 seconds.\nThis maybe due to an infinity loop or waiting for an input. "
                return app.render_template('editor.html', form=form, status=status,
                                           languages=app.languages)
            else:
                (now, then) = (type, status)

        else:
            args = dict()
            args["language"] = "Python"
            args["type"] = "without custom inputs"
            (type, status) = runWithCoverage(args)
            if (type == "status"):
                status = "Program has been terminated after running for 5 seconds.\nThis maybe due to an infinity loop or waiting for an input. "
                return app.render_template('editor.html', form=form, status=status,
                                           languages=app.languages)
            else:
                (now, then) = (type, status)

        finputs = open(getOutputFileName(), "r")
        timeElapsed = then - now
        outputs = finputs.readlines()
        outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
        finputs.close()
        finputs = open(getErrorFileName(), "r")
        errors = finputs.readlines()
        finputs.close()
        # os.system("rm -r submissions/" + getUserId())
        if len(errors) == 0:
            # print(outputs)
            return app.render_template('editor.html', form=form, status="Program Output", outputs=outputs,
                                       languages=app.languages)
        else:
            print(errors)
            return app.render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                       languages=app.languages)


class RunJavaStrategy(RunStrategy):
    def run(self, auxForm):
        form = CodemirrorForm(auxForm)
        text = form.source_code.data
        now = time.time()
        then = time.time()
        fout = open(getProgramFileName("Java"), "w")
        print(text, file=fout)
        fout.close()
        # compiling the program
        os.system("javac " + getProgramFileName("Java") + " 2>" + getErrorFileName())
        # reading errors
        finputs = open(getErrorFileName(), "r")
        errors = finputs.readlines()
        finputs.close()
        print(errors)
        # running with user defined inputs
        if auxForm.get("custom_input") != None:
            inputs = form.inputs.data
            finputs = open(getCustomInputsFileName(), "w")
            print(inputs, file=finputs)
            finputs.close()
            if len(errors) == 0:
                now = time.time()
                args = dict()
                args["language"] = "Java"
                args["type"] = "with custom inputs"
                (type, status) = runWithCoverage(args)
                if (type == "status"):
                    status = "Program has been terminated after running for 5 seconds.\nThis maybe due to an infinity loop or waiting for an input. "
                    return app.render_template('editor.html', form=form, status=status,
                                               languages=app.languages)
                else:
                    (now, then) = (type, status)
                # os.system("java -cp " + getExecutibleFileName("Java") + " Main <" + getCustomInputsFileName() +
                #           " 1> " + getOutputFileName() + " 2> " + getErrorFileName())

            else:
                print(errors)
                # os.system("rm -r submissions/" + getUserId())
                return app.render_template('editor.html', form=form, status="Program Compiled with errors",
                                           outputs=errors,
                                           languages=app.languages)
        # running without inputs
        else:
            if len(errors) == 0:

                # os.system("java -cp " + getExecutibleFileName("Java") + " Main " + " 1> " +
                #           getOutputFileName() + " 2> " + getErrorFileName())
                args = dict()
                args["language"] = "Java"
                args["type"] = "without custom inputs"
                print("asdf")
                (type, status) = runWithCoverage(args)
                print(type, status)
                if (type == "status"):
                    print("terminated")
                    status = "Program has been terminated after running for 5 seconds.\nThis maybe due to an infinity loop or waiting for an input. "
                    return app.render_template('editor.html', form=form, status=status,
                                               languages=app.languages)
                else:
                    (now, then) = (type, status)


            else:
                print(errors)
                # os.system("rm -r submissions/" + getUserId())
                return app.render_template('editor.html', form=form, status="Program Compiled with errors",
                                           outputs=errors,
                                           languages=app.languages)
        finputs = open(getOutputFileName(), "r")
        outputs = finputs.readlines()
        finputs.close()
        timeElapsed = then - now
        # outputs=list("")
        outputs.append("Time elapsed during execution: " + str(round(timeElapsed, 3)) + " s")
        finputs = open(getErrorFileName(), "r")
        # print(finputs)
        errors = finputs.readlines()
        finputs.close()
        # os.system("rm -r submissions/" + getUserId())
        if len(errors) == 0:
            print(outputs)
            return app.render_template('editor.html', form=form, status="Program Output", outputs=outputs,
                                       languages=app.languages)
        else:
            print(errors)
            return app.render_template('editor.html', form=form, status="Program Compiled with errors", outputs=errors,
                                       languages=app.languages)
