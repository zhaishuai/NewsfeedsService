# -*- coding:utf-8 -*-
'''
Created on Aug 16, 2013

@author: jimzhai
'''
'''

from NewsfeedsSoftware.article_categories_package.ArticleCategories import ArticleCategories
from NewsfeedsSoftware.article_categories_package.ArticleCategoriesTrain import ArticleCategoriesTrain




XML_PATH = "conf/articleCategoriesConfiguration.xml"
TRANING_PATH = "data/keywordtrain.txt"
ArticleCategoriesTrain().training(TRANING_PATH,XML_PATH)#训练
print str(ArticleCategories().classify("iPhone 中国移动 奚国华 运营 苹果 网络 2G 基站 目前 万个",XML_PATH)[0][0])
'''