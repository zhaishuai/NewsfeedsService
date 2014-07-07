# -*- coding:utf-8 -*-
'''
Created on Aug 9, 2013

@author: jimzhai

功能：分类学习模块

training(self,fileName): 对分析器进行训练

reportPrecision(self,fileName):报告分析器对测试文本分析的精度

'''
from pymining.math.text2matrix import Text2Matrix
from pymining.common.global_info import GlobalInfo
from pymining.common.configuration import Configuration
from pymining.preprocessor.chisquare_filter import ChiSquareFilter
from pymining.classifier.naive_bayes import NaiveBayes
class ArticleCategoriesTrain(object):
    def training(self,fileName,xml_path):
        config = Configuration.FromFile(xml_path)
        GlobalInfo.Init(config, "__global__")
        txt2mat = Text2Matrix(config, "__matrix__")
        [trainx, trainy] = txt2mat.CreateTrainMatrix(fileName)
        chiFilter = ChiSquareFilter(config, "__filter__")
        chiFilter.TrainFilter(trainx, trainy)
        [trainx, trainy] = chiFilter.MatrixFilter(trainx, trainy)
        nbModel = NaiveBayes(config, "naive_bayes")
        nbModel.Train(trainx, trainy)
    # training
    
    def reportPrecision(self,fileName,xml_path):
        config = Configuration.FromFile(xml_path)
        GlobalInfo.Init(config, "__global__", True)
        txt2mat = Text2Matrix(config, "__matrix__", True)
        chiFilter = ChiSquareFilter(config, "__filter__", True)
        nbModel = NaiveBayes(config, "naive_bayes", True)   
        [testx, testy] = txt2mat.CreatePredictMatrix("data/"+fileName)
        [testx, testy] = chiFilter.MatrixFilter(testx, testy)
        [resultY, precision] = nbModel.Test(testx, testy)
        print precision
    # reportPrecision
    
if __name__ == "__main__":
    ArticleCategoriesTrain().training("data/keywordtrain.txt","conf/articleCategoriesConfiguration.xml")
    #ArticleCategoriesTrain().reportPrecision("test copy.txt")

