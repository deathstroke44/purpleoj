import datetime, time, os
from codemirrorform import CodemirrorForm
from app import session


def getProblemSolution():
    return 12


def getProgramFileName(language):
    if language == "Python":
        return "submissions/" + getUserId() + "/" + getProblemId() + "/1.py"
    elif language == "Java":
        return "submissions/" + getUserId() + "/" + getProblemId() + "/Main.java"
    else:
        return "submissions/" + getUserId() + "/" + getProblemId() + "/1.cpp"


def getExecutibleFileName(language):
    if language == "Python":
        return "submissions/" + getUserId() + "/" + getProblemId() + "/a"
    elif language == "Java":
        return "submissions/" + getUserId() + "/" + getProblemId()
    else:
        return "submissions/" + getUserId() + "/" + getProblemId() + "/a"


def getOutputFileName():
    return "submissions/" + getUserId() + "/" + getProblemId() + "/outputs/1.txt"


def getErrorFileName():
    return "submissions/" + getUserId() + "/" + getProblemId() + "/outputs/error.txt"


def getCustomInputsFileName():
    return "submissions/" + getUserId() + "/" + getProblemId() + "/custom_inputs/1.txt"


def getUserId():
    return session['username']


def getProblemId():
    return "TestProblem"


def getExpectedOutputFileName(problemId):
    return "static/uploads/" + problemId + "out1.txt"


def getTestCaseFileName(problemId):
    return "static/uploads/" + problemId + "in1.txt"


def doesOutputMatch(userOutputFile, expectedOutputFile):
    try:
        userOutput = open(userOutputFile)
    except:
        return False
    expectedOutput = open(expectedOutputFile)
    for (x, y) in zip(userOutput.readlines(), expectedOutput.readlines()):
        if x != y:
            userOutput.close()
            expectedOutput.close()
            return False
    userOutput.close()
    expectedOutput.close()
    return True


def makeSubmissionFolders():
    os.system("mkdir submissions/" + getUserId())
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId())
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId() + "/outputs")
    os.system("mkdir submissions/" + getUserId() + "/" + getProblemId() + "/custom_inputs")


def runCode(form):
    selectedLanguage = form.get('languages')
    print(selectedLanguage)
    makeSubmissionFolders()
    from strategypatternforsubmission import RunJava, RunPython, RunC
    if selectedLanguage == "Python":
        runMode = RunPython()
        # return runPython(form)
    elif selectedLanguage == "C":
        runMode = RunC()
        # return runC(form)
    elif selectedLanguage == "Java":
        runMode = RunJava()
        # return runJava(form)
    return runMode.performRun(form)


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
            submissionInfo["Comilation Status"] = "CE"
            return submissionInfo
    # running the program
    if selectedLanguage == "Python":
        now = time.time()
        os.system("python3 " + getProgramFileName("Python") + " < " + getTestCaseFileName(problemId) + " 1>" +
                  getOutputFileName() + " 2>" + getErrorFileName())
        then = time.time()
    elif selectedLanguage == "Java":
        now = time.time()
        os.system("java -cp " + getExecutibleFileName("Java") + " Main <" + getTestCaseFileName(problemId) +
                  " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        then = time.time()
    elif selectedLanguage == "C":
        now = time.time()
        os.system(" ./" + getExecutibleFileName("C") + " < " + getTestCaseFileName(problemId) +
                  " 1> " + getOutputFileName() + " 2> " + getErrorFileName())
        then = time.time()

    # reading runtime errors
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    if len(errors) != 0:
        submissionInfo["Run Status"] = "RTE"
        return submissionInfo
    timeElapsed = then - now
    submissionInfo["Execution Time"] = timeElapsed
    if doesOutputMatch(getExpectedOutputFileName(problemId), getOutputFileName()) == False:
        submissionInfo["Result Verdict"] = "WA"
        return submissionInfo
    else:
        submissionInfo["Result Verdict"] = "Passed"
        return submissionInfo


def cleanup():
    os.system("rm -r submissions/" + getUserId())


from bson.objectid import ObjectId


def runForUbebug(inputs, text):
    makeSubmissionFolders()
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
    if True:
        finputs = open(getCustomInputsFileName(), "w")
        print(inputs, file=finputs)
        finputs.close()
        # checking for compile errors
        if len(errors) == 0:

            os.system(" ./" + getExecutibleFileName("C") + " < " + getCustomInputsFileName() +
                      " 1> " + getOutputFileName() + " 2> " + getErrorFileName())


        else:
            # os.system("rm -r submissions/" + getUserId())
            return errors

    # reading program outputs
    finputs = open(getOutputFileName(), "r")
    outputs = finputs.readlines()
    finputs.close()
    # reading RTE
    finputs = open(getErrorFileName(), "r")
    errors = finputs.readlines()
    finputs.close()
    # os.system("rm -r submissions/" + getUserId())
    # checking for RTE
    output = ""
    cleanup()
    for x in outputs:
        output += x
    if len(errors) == 0:
        print(output)
        return output
    else:
        print(errors)
        return errors


def getCode(filename):
    codelist = open(filename).readlines()
    code = ""
    for x in codelist:
        code += x + "\n"
    return code


def getInputFileListForUdebug(problemId):
    os.system("cd static/inputs_for_udebug &&ls | grep " + problemId + ">" + getUserId() + ".txt")
    return open("static/inputs_for_udebug/" + getUserId() + ".txt").readlines()


def getInputsForUdebug(filename):
    codelist = open(filename).readlines()
    code = ""
    for x in codelist:
        code += x
    return code


def extractInputName(x, problemId):
    return x.replace(problemId, "").replace(".txt", "")
