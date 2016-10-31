# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

class QSBK:
    def __int__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent':self.user_agent}
        self.stories=[]
        self.enable = False
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"Connecting failure,reason:",e.reason
                return None
    def getPageItems(self,pageIndex):
        pageCode=self.getPage(pageIndex)
        if not pageCode:
            print "Page loading failed..."
            return None
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?"content">(.*?)</div>.*?number">(.*?)</.*?number">(.*?)</.*?<div class="cmtMain">.*?"main-text">(.*?)</div>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            haveImg =re.search("img",item[3])
            if not haveImg:
                pageStories.append([item[0].strip(),item[1].strip(),item[2].strip(),item[4].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True and len(self.stories) < 2:
            pageStories = self.getPageItems(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input=raw_input()
            self.loadpage()
            if input == "Q":
                self.enable = False
                return
            print u"Page%d\tAuthor:%s\tPublish time:%s\n%s\nUps:%s\n"%(page,story[0],story[1],story[2],story[3])

    def start(self):
        print u"Reading Wikipedia embarrassments, press enter to find new scripts, Q exit"
        self.enable = True
        self.loadPage()
        nowpage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowpage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowpage)

spider= QSBK()
spider.start()









