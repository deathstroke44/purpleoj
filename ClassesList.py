class problem:
    def __init__(self, sub_task_count, id, pnt1, pnt2, pnt3, time_limit, memory_limit, stylee, name, acsub, sub,
                 setter):
        self.sub_task_count = sub_task_count
        self.pnt1 = pnt1
        self.pnt2 = pnt2
        self.pnt3 = pnt3
        self.id = id
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.stylee = stylee
        self.name = name
        self.acsub = acsub
        self.sub = sub
        self.setter = setter

class postob:
    def __init__(self, xtitle, xtext, xdt, xuser_, xid_):
        self.title = xtitle
        self.text = xtext
        self.dt = xdt
        self.user_ = xuser_
        self.id_ = xid_

class tripled:
    def __init__(self,st,ed,id,name):
        self.name=name
        self.st=st
        self.ed=ed
        self.id=id

class prob_struct:
    def __init__(self, pn, tl, ml, id):
        self.pn = pn
        self.tl = 'Time Limit : ' + str(tl) + 'ms'
        self.ml = 'Memory Limit: ' + str(ml) + 'mb'
        self.id = id