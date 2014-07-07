# -*- coding:utf-8 -*-
from scrapy import project, signals
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
import multiprocessing

'''
Created on Aug 7, 2013

@author: jimzhai

功能：为SpiderStartupController的一个工具类

'''

class CrawlerWorker(multiprocessing.Process):
 
    def __init__(self, spider, result_queue):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
 
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
 
        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)
    #__init__
    
    def _item_passed(self, item):
        self.items.append(item)
    # _item_passed
    
    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)
    #run