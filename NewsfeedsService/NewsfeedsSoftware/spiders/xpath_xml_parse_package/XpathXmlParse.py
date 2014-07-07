# -*- coding:utf-8 -*-
import xml.etree.ElementTree as et
from Queue import Queue
from NewsfeedsSoftware.spiders.urlxpath_package.URL_Xpath import URL_Xpath

'''
Created on Aug 6, 2013

@author: jimzhai

功能：解析Configuration.xml，来获取scrapy爬取网页时所必须的xpath语句

URL_Xpath_queue 为存储URL_Xpath对象的队列

getNumOfClassification(self,path) 获得Classification的种类数目

'''

class XpathXmlParse(object):
    def parseXML(self,path,start_position):
        count = 0;
        URL_Xpath_queue = Queue()
        
        """"获取所有list节点"""
        for website in et.parse(path).getroot().findall('list'):
            if count>=start_position:
                URL_Xpath_queue.put(URL_Xpath(website.find("allow_domains").text,
                                      website.find("start_urls").text, 
                                      website.find("url_list").text,
                                      website.find("js_url_list").text,
                                      website.find("js_xpath").text,
                                      website.find("js_artical_xpath").text,
                                      website.find("title").text,
                                      website.find("content").text,
                                      website.find("classification").text,
                                      website.find("imageURL").text
                                      ))
            count += 1
        return URL_Xpath_queue
    # parseXML

    
    def getNumOfClassification(self,path):
        return et.parse(path).getroot().find('intro').text
    
if __name__ == "__main__":

        URL_Xpath_queue = XpathXmlParse().parseXML("Configuration.xml")
        
        while not URL_Xpath_queue.empty():
            xx = URL_Xpath_queue.get()
            print xx.allow_domains,xx.content,xx.start_urls,xx.title,xx.url_list,xx.classification,xx.imageURL
        URL_Xpath()
        print XpathXmlParse().getNumOfClassification("Configuration.xml")

    
