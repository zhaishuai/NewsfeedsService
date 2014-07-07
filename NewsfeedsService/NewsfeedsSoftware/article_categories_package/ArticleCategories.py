# -*- coding:utf-8 -*-
'''
Created on Aug 9, 2013

@author: jimzhai

功能：对文章进行分类

classify(self,content): 开始分类
content是从SpiderStartupController中取得的

'''
from pymining.math.text2matrix import Text2Matrix
from pymining.common.global_info import GlobalInfo
from pymining.common.configuration import Configuration
from pymining.preprocessor.chisquare_filter import ChiSquareFilter
from pymining.classifier.naive_bayes import NaiveBayes
from operator import itemgetter

class ArticleCategories(object):
    def classify(self,content,xml_path):
        config = Configuration.FromFile(xml_path)
        GlobalInfo.Init(config, "__global__", True)
        txt2mat = Text2Matrix(config, "__matrix__", True)
        chiFilter = ChiSquareFilter(config, "__filter__", True)
        nbModel = NaiveBayes(config, "naive_bayes", True)   
        
        [cols, vals] = txt2mat.CreatePredictSample(content.decode("utf-8"))
        [cols, vals] = chiFilter.SampleFilter(cols, vals)      
        return sorted(nbModel.TestSample(cols, vals),reverse = True ,key=itemgetter(1, 0))
        #return nbModel.TestSample(cols, vals)
    # Classify
        
if __name__ == "__main__":
    inputStr = "iPhone中国移动奚国华运营苹果网络2G基站目前万个"
    print ArticleCategories().classify(inputStr,"conf/articleCategoriesConfiguration.xml")[0][0]