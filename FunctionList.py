
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

class graph:
    def __init__(self,nodelist,edgelist):
        self.nodelist=nodelist
        self.edgelist=edgelist

class adapter:
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