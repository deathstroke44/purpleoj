import uuid

import requests
from bs4 import BeautifulSoup


def HackerRankSingleArticle(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    FullArticle = soup.find('div', class_='blog-dtl-content')
    title = FullArticle.find('h1')

    x = str(FullArticle)
    x1 = str(FullArticle).find("<h1>")
    x2 = str(FullArticle).find("</h1>")

    content = x[:x1] + x[x2 + 5:]

    uid1 = uuid.uuid1()
    file_name_title = 'static/news/' + str(uid1) + '.html'
    f = open(file_name_title, 'w', encoding='utf8')
    f.write(str(title).replace('h1', 'h4'))
    f.close()

    uid2 = uuid.uuid1()
    file_name_content = 'static/news/' + str(uid2) + '.html'
    f = open(file_name_content, 'w', encoding='utf8')
    f.write(str(content))
    f.close()

    return file_name_title, file_name_content


def HackerRankMainPage(soup):
    title = soup.find('h3')
    x = str(title)
    x1 = str(title).find("</h3>")

    title2 = x[:x1] + '<sub>  HackerRank</sub>' + x[x1:]
    uid1 = uuid.uuid1()
    file_name_title = 'static/news/' + str(uid1) + '.html'
    f = open(file_name_title, 'w', encoding='utf8')
    f.write(str(title2).replace('h3', 'h4'))
    f.close()

    content = soup.find('p')
    uid2 = uuid.uuid1()
    file_name_content = 'static/news/' + str(uid2) + '.html'
    f = open(file_name_content, 'w', encoding='utf8')
    f.write(str(content))
    f.close()

    return file_name_title, file_name_content


def CodeForces(soup):
    title = soup.find('div', class_='title')
    string = str(title)
    title = string.replace(title.a['href'], 'http://codeforces.com/' + title.a['href'])
    content = soup.find('div', class_='ttypography')
    content2 = content

    x = str(title)
    x1 = str(title).find("</div>")

    title2 = x[:x1] + '<sub>  Codeforces</sub>' + x[x1:]

    uid1 = uuid.uuid1()
    file_name_title = 'static/news/' + str(uid1) + '.html'
    f = open(file_name_title, 'a', encoding='utf8')
    f.write(str(title2)
            .replace('<p>', '')
            .replace('</p>', '')
            .replace('div', 'h4'))
    f.close()

    for a in content.find_all('img'):
        if a:
            imageSource = a['src']
            st = 'http'
            if imageSource.find(st) == -1:
                content = str(content).replace(imageSource, 'http://codeforces.com/' + imageSource)

    for link in content2.find_all('a'):
        if link:
            linkSource = link['href']
            st = 'http'
            if linkSource.find(st) == -1:
                content = str(content).replace(linkSource, 'http://codeforces.com/' + linkSource)

    uid2 = uuid.uuid1()
    file_name_content = 'static/news/' + str(uid2) + '.html'
    f = open(file_name_content, 'a', encoding='utf8')
    f.write(str(content))
    f.close()

    return file_name_title, file_name_content


def atcoder(soup):
    FullArticle = soup.find_all('div')
    title = FullArticle[0].h3
    string = str(title)
    title = string.replace(title.a['href'], 'https://atcoder.jp' + title.a['href']).replace('class="panel-title"', '')
    content = FullArticle[1]
    # .replace("[", "").replace("]", " ")

    uid1 = uuid.uuid1()
    file_name_title = 'static/news/' + str(uid1) + '.html'
    f = open(file_name_title, 'a', encoding='utf8')
    f.write(str(title).replace('h3', 'h4'))
    f.close()

    uid2 = uuid.uuid1()
    file_name_content = 'static/news/' + str(uid2) + '.html'
    f = open(file_name_content, 'a', encoding='utf8')
    f.write(str(content).replace('class="panel-body blog-post"', ''))
    f.close()

    return file_name_title, file_name_content


def topcoder(soup):
    title = soup.find('h3')
    content = soup.find('div')

    x = str(title)
    x1 = str(title).find("</h3>")
    title2 = x[:x1] + '<sub>  topCoder</sub>' + x[x1:]

    uid1 = uuid.uuid1()
    file_name_title = 'static/news/' + str(uid1) + '.html'
    f = open(file_name_title, 'a', encoding='utf8')
    f.write(str(title2)
            .replace('h3', 'h4'))
    f.close()

    uid2 = uuid.uuid1()
    file_name_content = 'static/news/' + str(uid2) + '.html'
    f = open(file_name_content, 'a', encoding='utf8')
    f.write(str(content))
    f.close()

    return file_name_title, file_name_content


def thecrazyprogrammer(soup):
    title = soup.find('h2')
    content = soup.find('div')

    x = str(title)
    x1 = str(title).find("</h2>")
    title2 = x[:x1] + '<sub>  TheCrazyProgrammer</sub>' + x[x1:]

    uid1 = uuid.uuid1()
    file_name_title = 'static/news/' + str(uid1) + '.html'
    f = open(file_name_title, 'a', encoding='utf8')
    f.write(str(title2)
            .replace('h2', 'h4'))
    f.close()

    uid2 = uuid.uuid1()
    file_name_content = 'static/news/' + str(uid2) + '.html'
    f = open(file_name_content, 'a', encoding='utf8')
    f.write(str(content))
    f.close()

    return file_name_title, file_name_content


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

    return  soup0,soup1,soup2,soup3,soup4,soup5,soup6


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
