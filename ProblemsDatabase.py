import threading


class ProblemsDatabase():
    _instance = None
    _lock = threading.Lock()
    _insertLock=threading.Lock()
    def __new__(cls):
        if ProblemsDatabase._instance is None:
            with ProblemsDatabase._lock:
                if ProblemsDatabase._instance is None:
                    ProblemsDatabase._instance =super(ProblemsDatabase, cls).__new__(cls)
        return ProblemsDatabase._instance
    def insert(self,mongo,Dictionary):
        with ProblemsDatabase._insertLock:
            mongo.insert(Dictionary)
    def incrementSumissionCount(self,mongo,problemId):
        problem = mongo.find({'myid': problemId})
        problem = problem[0]
        # print(problem)
        sub = problem.get('sub')
        sub = int(sub) + 1
        print(int(sub))
        mongo.update_one(
            {'_id': problem.get('_id')}, {
                '$set': {
                    'sub': sub
                }}, upsert=False)
    def incrementAcSumissionCount(self,mongo,problemId):
        with ProblemsDatabase._insertLock:
            problem=mongo.find({'myid':problemId})
            problem=problem[0]
            # print(problem)
            acsub=problem.get('acsub')
            acsub=int(acsub)+1
            print(int(acsub))
            mongo.update_one(
                {'_id':problem.get('_id')},{
                '$set':{
                    'acsub':acsub
                }},upsert=False)

    def __init__(self):
        self.clients = []