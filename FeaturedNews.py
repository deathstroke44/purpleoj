class FeaturedNews():
    def __init__(self,imageSource,title,url):
        self.imageSource=imageSource
        self.title=title
        self.url=url
    def toString(self):
        return self.imageSource +" "+self.title+" "+self.url
