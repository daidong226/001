# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    # 匹配<div class="author clearfix">的节点下的html ,里面标签为<h2>里面的内容，匹配到"content">里面的 内容到</div>截止，下一个div里面的class==number的数值,和下一个div节点的评论的div class =main-text的评论的内容
    pattern = re.compile(
        '<div class="author clearfix">.*?<h2>(.*?)</h2>.*?"content">(.*?)</div>.*?number">(.*?)</.*?number">(.*?)</.*?<div class="cmtMain">.*?"main-text">(.*?)</div>',
        re.S)
    items = re.findall(pattern, content)
    # 分别对应的是 昵称，标题，好笑数，评论数,评论的内容
    for item in items:
        haveImg = re.search("img", item[3])
        if not haveImg:
            print item[0], item[1], item[2], item[4]
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
