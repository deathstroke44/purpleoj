import uuid
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template

app = Flask(__name__)


def reformatContent(content):
    # string = '</p>'
    # foundIndex = str(content).find(string)
    # print(foundIndex)
    # output = str(content)[:foundIndex+4] + '<br>' + str(content)[4+foundIndex:]
    return content

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/')
def news():
    class Article:
        def __init__(self, title_filename, content_filename):
            self.title_filename = title_filename
            self.content_filename = content_filename

    article_array = []
    source0 = requests.get('https://atcoder.jp/').text
    source1 = requests.get('https://atcoder.jp/?p=2').text
    source2 = requests.get('http://codeforces.com/').text
    source3 = requests.get('http://codeforces.com/page/2').text
    source4 = requests.get('https://csacademy.com/blog/ceoi-2018/').text

    soup0 = BeautifulSoup(source0, 'lxml')
    soup1 = BeautifulSoup(source1, 'lxml')
    soup2 = BeautifulSoup(source2, 'lxml')
    soup3 = BeautifulSoup(source3, 'lxml')
    soup4 = BeautifulSoup(source4, 'lxml')

    div0 = soup0.find_all('div', class_='panel panel-default')
    div1 = soup1.find_all('div', class_='panel panel-default')
    div2 = soup2.find_all('div', class_='topic')
    div3 = soup3.find_all('div', class_='topic')

    # for i in div0:
    #     title = i.find('h3', class_='panel-title')
    #     content = i.find('div', class_='panel-body blog-post')
    #
    #     print(content.find('p'))
    #
    #     uid1 = uuid.uuid1()
    #     file_name_title = 'static/news/' + str(uid1) + '.html'
    #     f = open(file_name_title, 'a', encoding='utf8')
    #     f.write(str(title))
    #     f.close()
    #
    #     uid2 = uuid.uuid1()
    #     file_name_content = 'static/news/' + str(uid2) + '.html'
    #     f = open(file_name_content, 'a')
    #     f.write(str(content.text))
    #     f.close()
    #
    #     print(str(content.text))
    #     article_array.append(Article(file_name_title, file_name_content))
    #     break

    # for i in div1:
    #     details = i.find_all('div')
    #     detail1 = details[1].text.replace("[", "").replace("]", " ")
    #     uid = uuid.uuid1()
    #     file_name = 'static/news/' + str(uid) + '.html'
    #     f = open(file_name, 'a', errors='ignore')
    #     f.write(htmlfreshner(str(details[1].text)))
    #     f.close()
    #     article_array.append(Article(details[0].h3.text, file_name))

    for i in div2:
        title = i.find('div', class_='title')
        content = i.find('div', class_='ttypography')
        content2 = content

        uid1 = uuid.uuid1()
        file_name_title = 'static/news/' + str(uid1) + '.html'
        f = open(file_name_title, 'a', encoding='utf8')
        f.write(str(title).replace('<p>', '').replace('</p>', '').replace('div','h4').replace(title.a['href'], 'http://codeforces.com/'+title.a['href']))
        f.close()

        print(title.a['href'])

        for a in content.find_all('img'):
            if a:
                imageSource = a['src']
                st = 'http'
                if imageSource.find(st) == -1:
                    content = str(content).replace(imageSource,'http://codeforces.com/'+imageSource)

        for link in content2.find_all('a'):
            if link:
                linkSource = link['href']
                st = 'http'
                if linkSource.find(st) == -1:
                    content = str(content).replace(linkSource,'http://codeforces.com/'+linkSource)

        uid2 = uuid.uuid1()
        file_name_content = 'static/news/' + str(uid2) + '.html'
        f = open(file_name_content, 'a', encoding='utf8')
        f.write(str(content))
        f.close()

        article_array.append(Article(file_name_title, file_name_content))
        # print(content)

    for i in div3:
        title = i.find('div', class_='title')
        content = i.find('div', class_='ttypography')
        # content = reformatContent(content)

        uid1 = uuid.uuid1()
        file_name_title = 'static/news/' + str(uid1) + '.html'
        f = open(file_name_title, 'a', encoding='utf8')
        f.write(str(title).replace('<p>', '').replace('</p>', ''))
        f.close()

        for a in content.find_all('img'):
            if a:
                imageSource = a['src']
                st = 'http'
                if imageSource.find(st) == -1:
                    content = str(content).replace(imageSource,'http://codeforces.com/'+imageSource)
                    print(a['src'])

        uid2 = uuid.uuid1()
        file_name_content = 'static/news/' + str(uid2) + '.html'
        f = open(file_name_content, 'a', encoding='utf8')
        f.write(str(content))
        f.close()

        article_array.append(Article(file_name_title, file_name_content))
        # print(content)

    return render_template('news.html', article_array=article_array)


def htmlfreshner(bad):
    good = ''
    l = len(bad)
    cnt = 0
    for i in range(1, l - 1):
        if bad[i] == '\n':
            cnt += 1
        else:
            cnt = min(3, cnt)
            if cnt > 1:
                cnt -= 1
            for k in range(0, cnt):
                good += '\n'
            good += bad[i]
            cnt = 0
    return good


if __name__ == '__main__':
    app.run(debug=True)
