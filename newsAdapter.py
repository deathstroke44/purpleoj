import requests
from bs4 import BeautifulSoup


class SocketInterFace:
    def getData(self):
        pass


# Adaptee
class Socket(SocketInterFace):
    def getData(self):
        return LoadRawHtmlFiles()


# Target interface
class TargetSocketInterface:
    def getData(self): pass


# The Adapter
class Adapter(TargetSocketInterface):
    __socket = None

    def __init__(self, socket):
        self.__socket = socket

    def getData(self):
        soup0, soup1, soup2, soup3, soup4, soup5, soup6 = LoadSoup()
        atcoderMain = soup0.find_all('div', class_='panel panel-default')
        atcoderPage2 = soup1.find_all('div', class_='panel panel-default')
        CodeForceMain = soup2.find_all('div', class_='topic')
        CodeForcePage2 = soup3.find_all('div', class_='topic')
        HackerRankMain = soup4.find_all('div', class_='blog-content')
        TopCoderMain = soup5.find_all('div', class_='story-content')
        thecrazyprogrammerMain = soup6.find_all('article')

        return atcoderMain, atcoderPage2, CodeForceMain, CodeForcePage2, \
               HackerRankMain, TopCoderMain, thecrazyprogrammerMain


# Client
class Client:
    __power = None

    def __init__(self, power):
        self.__power = power

    def getSoup(self):
        return self.__power.getData()


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
