# -*- coding:utf-8 -*-
'''
Created on Aug 6, 2013

@author: jimzhai

用途：用来临时存储scrapy解析网页时所必须的Xpath语句

allow_domains对应scraoy中的allow_domains
start_urls要爬取的网页网址
url_list xpath语句，用于解析start_urls里的链接
title xpath语句，用于解析文章标题
content xpath语句，用于解析文章内容
classification 文章的类型，当需要进行分类训练时该项必须填写，不需要分类训练则不用填写
imageURL 文章的图片链接
js_url_list要爬取的网页网址(爬取javascript与AJAX技术的网站)
'''
class URL_Xpath(object):
    def __init__(self,allow_domains=None,start_urls=None,url_list=None,js_url_list=None,js_xpath=None,js_artical_xpath=None,title=None,content=None,classification=None,imageURL=None):
        self.allow_domains = allow_domains
        self.start_urls = start_urls
        self.url_list = url_list
        self.js_url_list = js_url_list
        self.js_xpath = js_xpath
        self.js_artical_xpath = js_artical_xpath
        self.title = title
        self.content = content
        self.classification = classification
        self.imageURL = imageURL
        
    #__init__
    
if __name__ == "__main__":
    xx = URL_Xpath("huxiu.com","www.huxiu.com","xxxx","yyy","ccc","0","//div")    
    print xx.allow_domains,xx.content,xx.start_urls,xx.title,xx.url_list,xx.classification,xx.imageURL