import abc
import uuid

article_array=[]


class NewsStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def Load(self, soup):
        pass


class Article:
    def __init__(self, title_filename, content_filename):
        self.title_filename = title_filename
        self.content_filename = content_filename


class LoadCodeForceStrategy(NewsStrategyAbstract):
    def Load(self, soup):
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

        article_array.append(Article(file_name_title, file_name_content))


class LoadHackerRankStrategy(NewsStrategyAbstract):
    def Load(self, soup):
        title = soup.find('h3')
        link = title.find("a")['href']
        x = str(title)
        x1 = str(title).find("</h3>")



        title2 = x[:x1] + '<sub>  HackerRank</sub>' + x[x1:]
        uid1 = uuid.uuid1()
        file_name_title = 'static/news/' + str(uid1) + '.html'
        f = open(file_name_title, 'w', encoding='utf8')
        f.write(str(title2).replace('h3', 'h4'))
        f.close()

        content = soup.find('p')
        content = str(content)+"<span class=\"read-more\"><a href=\""+link+"\">Read More »</a></span>"
        uid2 = uuid.uuid1()
        file_name_content = 'static/news/' + str(uid2) + '.html'
        f = open(file_name_content, 'w', encoding='utf8')
        f.write(str(content))
        f.close()

        article_array.append(Article(file_name_title, file_name_content))


class LoadCrazyProgrammerStrategy(NewsStrategyAbstract):
    def Load(self, soup):
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

        article_array.append(Article(file_name_title, file_name_content))


class LoadTopCoderStrategy(NewsStrategyAbstract):
    def Load(self, soup):
        title = soup.find('h3')
        link = title.find("a")['href']
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

        content = str(content) + "<span class=\"read-more\"><a href=\"" + link + "\">Read More »</a></span>"
        uid2 = uuid.uuid1()
        file_name_content = 'static/news/' + str(uid2) + '.html'
        f = open(file_name_content, 'a', encoding='utf8')
        f.write(str(content))
        f.close()

        article_array.append(Article(file_name_title, file_name_content))


class LoadAtCoderStrategy(NewsStrategyAbstract):
    def Load(self, soup):
        FullArticle = soup.find_all('div')
        title = FullArticle[0].h3
        string = str(title)
        title = string.replace(title.a['href'], 'https://atcoder.jp' + title.a['href']).replace('class="panel-title"',
                                                                                                '')
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

        article_array.append(Article(file_name_title, file_name_content))
