# -*- coding:utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from NewsfeedsSoftware.items import NewsfeedssoftwareItem
from NewsfeedsSoftware.spiders.urlxpath_package.URL_Xpath import URL_Xpath
from V8Engine.runtime import JSR
from scrapy.http import HtmlResponse
import socket
'''
Created on Aug 6, 2013

@author: jimzhai

功能：爬取网页的信息

url_xpath中存放爬虫spider爬取网页时的网址，xpath等信息

'''
class Spider(BaseSpider):
    url_xpath = URL_Xpath()
    name = "spider"
    allowed_domains = []
    start_urls = []
    
    '''
    def __init__(self):
    '''
        #初始化函数
    '''
    #__init__
    '''

    def set_url_xpath(self,url_xpath):
        self.url_xpath.allow_domains = url_xpath.allow_domains
        self.url_xpath.content = url_xpath.content
        self.url_xpath.start_urls = url_xpath.start_urls
        self.url_xpath.title = url_xpath.title
        self.url_xpath.url_list = url_xpath.url_list
        self.url_xpath.js_url_list = url_xpath.js_url_list
        self.url_xpath.js_xpath = url_xpath.js_xpath
        self.url_xpath.js_artical_xpath = url_xpath.js_artical_xpath
        self.url_xpath.classification = url_xpath.classification
        self.url_xpath.imageURL = url_xpath.imageURL
        self.allowed_domains.append(self.url_xpath.allow_domains)
        self.start_urls.append(self.url_xpath.start_urls)
        print self.url_xpath.start_urls
    '''
        手动调用该函数为url_xpath赋值
    '''
    #set_url_xpath
    
    def getResponse4js(self,response,url,newencoding,xpath):
        hxs = HtmlXPathSelector(response)
        title = hxs.select(self.url_xpath.title).extract()
        response4js = HtmlResponse(url,encoding = newencoding)
        response4js.status = response.status
        response4js.headers = response.headers
        try:
            response4js.body = ("<html><title>"+title[0]+"</title>").encode("utf-8")+str(JSR(url).execute(xpath))+("</html>").encode('utf-8')
        except socket.error as socketerror:
            response4js.body = ("<html><title>"+title[0]+"</title>").encode("utf-8")+str(JSR(url).execute(xpath))+("</html>").encode('utf-8')
            print "time out!"
        return response4js

    def parse(self,response):
        if self.url_xpath.js_xpath!=None:
            response = self.getResponse4js(response, self.url_xpath.start_urls, "utf-8", self.url_xpath.js_xpath)
        hxs = HtmlXPathSelector(response)
        for site in hxs.select(str(self.url_xpath.url_list)) :    
            href = site.select("@href").extract()
            if href !=[] and href[0].strip()!="":
                print href[0]
                if self.url_xpath.js_url_list!=None:
                    yield Request(self.__switchHref(self.url_xpath.js_url_list,href[0]), callback=self.parseContent)
                else:
                    yield Request(self.__switchHref(self.url_xpath.start_urls,href[0]), callback=self.parseContent)
                '''
                if href[0].split("/")[0] == "http:" :  
                    #判断是这种网址：http://news.21cn.com/webfocus/a/2013/0807/08/23280223.shtml还是这种网址webfocus/a/2013/0807/08/23280223.shtml
                    yield Request(href[0], callback=self.parseContent)
                else :
                    yield Request(self.url_xpath.start_urls+"/"+href[0], callback=self.parseContent)
                    #yield Request("http://www.huxiu.com"+"/"+href[0], callback=self.parseContent)
                '''
    '''
        爬取文章中的链接
    '''              
    #parse
    
    def parseContent(self,response):
        URL = response.url
        if self.url_xpath.js_artical_xpath!=None:
            response = self.getResponse4js(response, response.url, "utf-8", self.url_xpath.js_artical_xpath.strip())
        print response.url
        print "----------------------------------------"
        hxs = HtmlXPathSelector(response)
        items = []
        for site in hxs.select('//html') :
            title = site.select(self.url_xpath.title).extract()
            if title != []:
                item = NewsfeedssoftwareItem()
                item['title'] = title[0]
                print title[0]
                items.append(item)
        #count = 0
        for site in hxs.select(self.url_xpath.content+"|"+self.url_xpath.imageURL):
            '''提取文章内容'''
            content = site.select("text()").extract()
            
            website = site.select("@src").extract()
            if website!= [] and website[0].strip()!="":
                itemcontent = NewsfeedssoftwareItem()
                itemcontent['content'] = "<$$>"         #<$$>代表图片
                items.append(itemcontent)
                
            
            if content != []:
                itemcontent = NewsfeedssoftwareItem()
                itemcontent['content'] = content[0].strip()
                items.append(itemcontent)

                
            
                
        for site in hxs.select(self.url_xpath.imageURL):  
            '''提取文章中的图片'''      
            image_url = site.select("attribute::src").extract()
            
            if image_url != []:
                itemhref = NewsfeedssoftwareItem()
                if self.url_xpath.js_url_list!=None:
                    itemhref['image_url'] = self.__switchHref(self.url_xpath.js_url_list,image_url[0])
                else:
                    itemhref['image_url'] = self.__switchHref(self.url_xpath.start_urls,image_url[0])
                items.append(itemhref)
                
        '''提取文章地址'''
        address_item = NewsfeedssoftwareItem()
        address_item["address"] = URL
        items.append(address_item)
        return items
    
    def __switchHref(self,head_href,href):
        if href !="" and head_href!=None:
            if href.strip().split("/")[0] == "http:" :  
            #判断是这种网址：http://news.21cn.com/webfocus/a/2013/0807/08/23280223.shtml还是这种网址webfocus/a/2013/0807/08/23280223.shtml
                return href
            else :
                if href[0]=='/':    
                    return head_href+"/".encode("utf-8")+href
                else:
                    return head_href+href
        
        
  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    