# -*- coding:utf-8 -*-
from multiprocessing.queues import Queue
from NewsfeedsSoftware.spiders.spiderStartupController_package.CrawlerWorker import CrawlerWorker
from NewsfeedsSoftware.spiders.Spider import Spider
from NewsfeedsSoftware.spiders.xpath_xml_parse_package.XpathXmlParse import XpathXmlParse
from NewsfeedsSoftware.spiders.urlxpath_package.URL_Xpath import URL_Xpath
from NewsfeedsSoftware.article_categories_package.ArticleCategories import ArticleCategories
from NewsfeedsSoftware.article_categories_package.ArticleCategoriesTrain import ArticleCategoriesTrain
from newsfeedsDataLayer.models import Artical,RelatedReading

import jieba.analyse
import md5


'''
Created on Aug 7, 2013

@author: jimzhai

功能：启动Spider爬虫，并为其加载相关xpath语句

startSpider：启动爬虫开始爬取网页

__processing: 用于事务处理,与进行文章分类训练相关的代码写在该函数中

0 社会，1 娱乐，2 财经，3 科技，4 体育，5 汽车，6 国际

'''


class SpiderStartupController(object):
    
    XML_PATH = "conf/articleCategoriesConfiguration.xml"
    TRANING_PATH = "data/keywordtrain.txt"
    md5_hashMap={}
    def startSpider(self,start_position=0):
        print "start scrap!"
        spider = Spider()
        result_queue = Queue()
        md5_queue = [] #用来存储已经爬下来的文章的md5Code
        URL_Xpath_queue = XpathXmlParse().parseXML("Configuration.xml",start_position)
        keywordtrainFile = open(self.TRANING_PATH,'a')
        print "loading md5 code!"
        self.__getMd5HashMap()
        print "finish loading md5 code!"
        while not URL_Xpath_queue.empty():
            url_xpath = URL_Xpath_queue.get()
            #print url_xpath.allow_domains,url_xpath.content,url_xpath.start_urls,url_xpath.title,url_xpath.url_list,URL_Xpath_queue.qsize()
            spider.set_url_xpath(url_xpath)
            crawler = CrawlerWorker(spider, result_queue)
            crawler.start()
            title = ""
            content = "    "
            judger = False          #判断是否为第一次运行
            needToTrain = False
            md5Code = " "           #文章特征码，用于文章查重
            classification=""       #文章类型
            image_url = ""
            address = ""
            
            for item in result_queue.get():
                if 'title' in item:
                    if judger and content.strip()!="":
                        md5Code = self.__getMd5Code(content)
                        if md5Code in self.md5_hashMap:
                            print "Article repeat over！"
                            content = "    "
                            title=""
                            classification=""
                            image_url = ""
                            judger=False
                            continue;
                        #print title
                        #print "---------------以上是标题------------------"
                        #print content
                        
                        tags = jieba.analyse.extract_tags(content,10)#提取关键词
                        classification = url_xpath.classification
                        if url_xpath.classification != None :#进行文章分类训练
                            print "writing training document!"
                            self.__writeTrainingDocument(title,tags, keywordtrainFile, url_xpath)
                            
                            needToTrain = True
                            #print "+++++++++++++++进行训练 文章类型："+classification+"+++++++++++++++++"
                        else:
                            print "doing classification!"
                            classification = self.__getClassification(tags)
                            
                            #print "+++++++++++++++进行分类 文章类型："+classification+"+++++++++++++++++"
                        artical = Artical()
                        artical.set_title(title)
                        artical.set_content(content)
                        artical.set_address(address)
                        artical.set_md_5_code(md5Code)
                        if image_url.strip() == "":
                            image_url = "None"
                        artical.set_image_url(image_url)
                        #-----------Bug-Patch----------#
                        mykeywords = artical.getKeyWord()
                        if mykeywords.strip() == "":
                            continue;
                        '''
                            排除只有标点的文章
                            
                        '''
                        #------------------------------#
                        md5_queue.append([md5Code,mykeywords.strip(),classification])
                        artical.set_classification(classification)
                        print "++++++++++++++++++++++++++++++ writing"+artical.Title +"to database!++++++++++++++++++++++++++++++++++"
                        #在此处决定是插入还是更新
                        artical.insertNewArtical()
                        
                    content = "    "
                    image_url = ""              
                    judger = True
                    
                    title = item['title']
                elif 'content' in item :
                    content += "    "+item['content']+'\n'
                elif 'image_url' in item:
                    #content += "<$$img/>"
                    image_url += '$'+str(item['image_url'])
                    #print "ooooooooooooooooooo" + str(image_url)
                elif 'address' in item:
                    address = item['address']
                
        keywordtrainFile.close()
        if needToTrain :
            print "start training!"
            ArticleCategoriesTrain().training(self.TRANING_PATH,self.XML_PATH)#训练
            print "finish training!"
        print "进行相关文章匹配"
        for md5 in md5_queue:
            RelatedReading().insertRelatedReading(md5[0],md5[1],md5[2])
            
    #startSpider
    
    def __writeTrainingDocument(self,title,tags,keywordtrainFile,url_xpath):
        #print "---------------------------关键词----------------------------"
        word = ""
        for tag in tags:
            #print tag
            if tag != "":
                word +=tag       
        keywordtrainFile.write(word+"\t"+url_xpath.classification+"\n")

        #print "------------------------------------------------------------"  
    #__processing
    
    def __getClassification(self,tags):
        keyword = ""
        for tag in tags:
            if tag != "":
                keyword += tag+" "
        return str(ArticleCategories().classify(keyword,self.XML_PATH)[0][0])
    '''
        对文章不进行训练时调用该函数
        
    '''
    #__pricessing
    
    def __getMd5Code(self,content):
        m = md5.new()
        m.update(content) 
        #print m.digest()
        return m.hexdigest()
    #__getMd5Code
    
    def __getMd5HashMap(self):
        for mdfive in Artical.objects.all().values("md5Code"):
            self.md5_hashMap[mdfive["md5Code"]]=1
    '''
        从数据库中读取所有文章的md5特征值，并将其存放至md5_hashMap中以便查重
    
    '''
    #__getMd5HashMap
    
    
if __name__ == "__main__":
    SpiderStartupController().startSpider(0)
