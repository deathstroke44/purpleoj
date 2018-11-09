import app
from UtilityFunctionsForEditor import cleanup, getInputFileListForUdebug, extractInputName, getCode, \
    getErrorFileName, getOutputFileName, getExecutibleFileName, getCustomInputsFileName, getProgramFileName, \
    makeSubmissionFolders, getInputsForUdebug
import os


def udebugUtil(problemId, form):
    acceptedOutput = ""
    yourOutputs = ""
    inputs = ""
    mismatchNumber = -1
    results = list()
    problemTitle = app.mongo.db.problems.find_one({'myid': problemId}).get('name')
    inputFiles = getInputFileListForUdebug(problemId)
    selectedinputFile = ""
    usableInputFiles = list()
    for x in inputFiles:
        usableInputFiles.append(extractInputName(x, problemId))
    print(inputFiles)
    if "get_accepted_output_button" in form:
        acceptedOutput = form["accepted_output_textarea"]
        inputs = form["input_textarea"]
        code = getCode("static/uploads/" + problemId + "sol.cpp")
        acceptedOutput = runForUbebug(inputs, code)
        print(code)
        print(acceptedOutput)

    elif "compare_outputs_button" in form:
        print(form)
        acceptedOutput = form["accepted_output_textarea"]
        inputs = form["input_textarea"]
        yourOutputs = form["your_output_textarea"]
        code = getCode("static/uploads/" + problemId + "sol.cpp")
        acceptedOutput = runForUbebug(inputs, code)
        # print(code)
        # print(acceptedOutput)
        yourOutputList = list()
        acceptedOutputList = list()
        for x in acceptedOutput.split("\n"):
            if x == None:
                acceptedOutputList.append("")
            else:
                acceptedOutputList.append(x)
        for x in yourOutputs.split("\n"):
            if x == None:
                yourOutputList.append("")
            else:
                yourOutputList.append(x)
        acceptedOutputLineNumber = len(acceptedOutputList)
        yourOutputLineNumber = len(yourOutputList)
        if (len(acceptedOutputList) > len(yourOutputList)):
            for i in range(len(acceptedOutputList) - len(yourOutputList)):
                yourOutputList.append("")
        elif (len(acceptedOutputList) < len(yourOutputList)):
            for i in range(-len(acceptedOutputList) + len(yourOutputList)):
                acceptedOutputList.append("")
        outputpair = zip(acceptedOutputList, yourOutputList)
        mismatchNumber = 0
        for i, (x, y) in enumerate(outputpair):
            if x != y[:-1]:
                mismatchNumber += 1
                if (i < acceptedOutputLineNumber and i < yourOutputLineNumber):
                    results.append((int(i + 1), x, int(i + 1), y))
                elif (i < acceptedOutputLineNumber):
                    results.append((int(i + 1), x, "", y))
                else:
                    results.append(("", x, int(i + 1), y))
    if "inputstorer" in form and len(form["inputstorer"]) > 0:
        selectedinputFile = "static/inputs_for_udebug/" + problemId + str(form["inputstorer"]).replace("\n",
                                                                                                       "").replace(
            "\r", "").strip(" ") + ".txt"
        inputs = getInputsForUdebug(selectedinputFile)
    return app.render_template('udebug.html', selectedinput=inputs, acceptedOutput=acceptedOutput,
                               yourOutput=yourOutputs,
                               results=results, mismatchNumber=mismatchNumber, inputs=usableInputFiles,
                               problemTitle=problemTitle)


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
