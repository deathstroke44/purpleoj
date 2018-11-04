
from newsStrategy import LoadCodeForceStrategy, article_array, LoadHackerRankStrategy, LoadCrazyProgrammerStrategy,LoadTopCoderStrategy,LoadAtCoderStrategy
from newsAdapter import Socket,Client,Adapter

codeforce = LoadCodeForceStrategy()
hackerrank = LoadHackerRankStrategy()
crazyprogrammer = LoadCrazyProgrammerStrategy()
topcoder = LoadTopCoderStrategy()
atcoder = LoadAtCoderStrategy()


class NewsMain(object):
    def __init__(self, load_strategy):
        self._load_strategy = load_strategy

    def Load(self, soup):
        self._load_strategy.Load(soup)


class CodeFroce(NewsMain):
    def __init__(self):
        super(CodeFroce, self).__init__(codeforce)


class HackerRank(NewsMain):
    def __init__(self):
        super(HackerRank, self).__init__(hackerrank)


class CrazyProgrammer(NewsMain):
    def __init__(self):
        super(CrazyProgrammer, self).__init__(crazyprogrammer)


class TopCoder(NewsMain):
    def __init__(self):
        super(TopCoder, self).__init__(topcoder)


class AtCoder(NewsMain):
    def __init__(self):
        super(AtCoder, self).__init__(atcoder)


def newsCall():
    socket = Socket()
    # socket.getData()
    adapter = Adapter(socket)
    client = Client(adapter)

    atcoderMain, atcoderPage2, CodeForceMain, CodeForcePage2, \
    HackerRankMain, TopCoderMain, thecrazyprogrammerMain = client.getSoup()

    index = 0
    for i in CodeForceMain:
        instance = CodeFroce()
        instance.Load(i)

    for i in HackerRankMain:
        instance = HackerRank()
        instance.Load(i)
        index = index + 1

    for i in TopCoderMain:
        instance = TopCoder()
        instance.Load(i)

    for i in CodeForcePage2:
        instance = CodeFroce()
        instance.Load(i)

    for i in thecrazyprogrammerMain:
        instance = CrazyProgrammer()
        instance.Load(i)

    # for i in atcoderMain:
    #     instance = AtCoder()
    #     instance.Load(i)

    # import random
    # random.shuffle(article_array)
    # print(article_array.__len__())
    return article_array


