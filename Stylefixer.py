import os
lines=os.listdir("/home/muntakim/PycharmProjects/purpleoj/static/css/styles")
lines=[x for x in lines if ".css" in x]
filelines=list()
for x in lines:
    x=x[:-4]
    filelines.append(x)
filelines.sort()
file =open("/home/muntakim/PycharmProjects/purpleoj/static/css/styles/styles.txt","w")
for x in filelines:
    print(x)
    print(x, file=file)
file.close()