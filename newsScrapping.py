
import requests
from bs4 import BeautifulSoup
from newsStrategy import LoadCodeForceStrategy, article_array, LoadHackerRankStrategy, LoadCrazyProgrammerStrategy,LoadTopCoderStrategy,LoadAtCoderStrategy


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
    # ********
    # from newsScrapping import LoadRawHtmlFiles
    # LoadRawHtmlFiles()  #Has to call this at a certain time of the day
    # ******

    soup0, soup1, soup2, soup3, soup4, soup5, soup6 = LoadSoup()

    atcoderMain = soup0.find_all('div', class_='panel panel-default')
    atcoderPage2 = soup1.find_all('div', class_='panel panel-default')
    CodeForceMain = soup2.find_all('div', class_='topic')
    CodeForcePage2 = soup3.find_all('div', class_='topic')
    HackerRankMain = soup4.find_all('div', class_='blog-content')
    TopCoderMain = soup5.find_all('div', class_='story-content')
    thecrazyprogrammerMain = soup6.find_all('article')

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


def LoadSoup():
    f = open('static/WebsiteData/atcoder.html', 'r', encoding='utf-8')
    soup0 = BeautifulSoup(f.read(), 'lxml')

    f = open('static/WebsiteData/atcoder_page2.html', 'r', encoding='utf-8')
    soup1 = BeautifulSoup(f.read(), 'lxml')

    f = open('static/WebsiteData/codeforces.html', 'r', encoding='utf-8')
    soup2 = BeautifulSoup(f.read(), 'lxml')

    f = open('static/WebsiteData/codeforces_page2.html', 'r', encoding='utf-8')
    soup3 = BeautifulSoup(f.read(), 'lxml')

    f = open('static/WebsiteData/hackerrank_mainpage.html', 'r', encoding='utf-8')
    soup4 = BeautifulSoup(f.read(), 'lxml')

    f = open('static/WebsiteData/topcoder.html', 'r', encoding='utf-8')
    soup5 = BeautifulSoup(f.read(), 'lxml')

    f = open('static/WebsiteData/thecrazyprogrammer.html', 'r', encoding='utf-8')
    soup6 = BeautifulSoup(f.read(), 'lxml')

    return soup0, soup1, soup2, soup3, soup4, soup5, soup6


def LoadRawHtmlFiles():
    source0 = requests.get('https://atcoder.jp/').text
    source1 = requests.get('https://atcoder.jp/?p=2').text
    source2 = requests.get('http://codeforces.com/').text
    source3 = requests.get('http://codeforces.com/page/2').text
    source4 = requests.get('https://blog.hackerrank.com/?h_r=home&h_l=header').text
    source5 = requests.get('https://www.topcoder.com/blog/allnew/').text
    source6 = requests.get('https://www.thecrazyprogrammer.com/category/programming').text

    f = open('static/WebsiteData/atcoder.html', 'w', encoding='utf-8')
    f.write(str(source0))
    f.close()

    f = open('static/WebsiteData/atcoder_page2.html', 'w', encoding='utf-8')
    f.write(str(source1))
    f.close()

    f = open('static/WebsiteData/codeforces.html', 'w', encoding='utf-8')
    f.write(str(source2))
    f.close()

    f = open('static/WebsiteData/codeforces_page2.html', 'w', encoding='utf-8')
    f.write(str(source3))
    f.close()

    f = open('static/WebsiteData/hackerrank_mainpage.html', 'w', encoding='utf-8')
    f.write(str(source4))
    f.close()

    f = open('static/WebsiteData/topcoder.html', 'w', encoding='utf-8')
    f.write(str(source5))
    f.close()

    f = open('static/WebsiteData/thecrazyprogrammer.html', 'w', encoding='utf-8')
    f.write(str(source6))
    f.close()
