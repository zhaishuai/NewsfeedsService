# -*- coding:utf-8 -*-
#from newsfeedsDataLayer.models import RelatedReading
from newsfeedsDataLayer.models import Artical
from newsfeedsDataLayer.models import User_id
#import os
#User_id().insertUser(1)
#User_id().updateKeywords(1, "iPhone 苹果 谷歌 鲍尔默 长角 ZDNetXPVistaMaryJoFoley15 小米 电商 互联网 百度 永福 易信")
#User_id().updateKeywords(11, "百度 永福 易信 ")
#RelatedReading().insertRelatedReading("1461be38528df0efea5a0bb48ed57da5")
#result = Artical().recommendation(2)
#Artical().everyClassificationRecommendation(1)
#result = Artical().recommendation(11,"NewsfeedsSoftware/spiders/spiderStartupController_package/Configuration.xml")
#print "********************************"
#for re in result:
#    print re["title"]
#print User_id().getLastUserId()
#User_id().readArtiaclThenAppendKeywords(1, "65958f7f7e5c8256de240c60ec368594")
#print str(os.getcwd())+"1111111111111111111111111"

'''
def getUserKeyWord(user_id):
    keyword = User_id.objects.filter(userID = user_id).values()[0]["keywords"]
    keywordSet = dict()
    for key in keyword.strip().split('$'):
        if key !="":
            word = key.split('-')
            count = word[1].split('?')
            keywordSet[word[0]] = count[0]
            
    for key in keywordSet:
        print key,keywordSet[key]
        
getUserKeyWord(11)
'''