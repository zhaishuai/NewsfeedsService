# -*- coding:utf-8 -*-
from django.db import models
import jieba.analyse
import jieba.posseg
from NewsfeedsSoftware.spiders.xpath_xml_parse_package.XpathXmlParse import XpathXmlParse
import time

class Artical(models.Model):





    title=models.TextField()
    content=models.TextField()
    md5Code=models.CharField(max_length=32)
    keyword=models.CharField(max_length=100)
    address=models.URLField()
    classification=models.CharField(max_length=50)
    imageURL = models.TextField()
    date=models.DateField(auto_now_add=True)
    
    Title=" "
    Content=" "
    Address=" "
    Md5Code=" "
    Classification=" "
    ImageURL = " "
        
    def insertNewArtical(self):
        Artical.objects.create(title=self.Title,content=self.Content,md5Code=self.Md5Code,keyword=self.getKeyWord(),address=self.Address,classification=self.Classification,imageURL=self.ImageURL)
        #Artical.objects.create(title="hello",content="self.Content",md5Code="self.__getMd5Code()",keyword="self.__getKeyWord()",address="self.Address")
        #print "********************以下是持久层的信息******************"
        #print "title:"+self.Title+"  Content:"+self.Content+"  md5Code:"+self.Md5Code+"  keyword:"+self.__getKeyWord()+"  address:"+self.Address
        #print "****************************************************"
    '''
        向数据库插入数据
    
    '''
    #insertNewArtical
    
    
    def getKeyWord(self):
        tags = jieba.analyse.extract_tags(self.Content)
        content = ""
        for tag in tags:
            content +=tag
        words = jieba.posseg.cut(content)
        count = 0
        content = ''
        for w in words:
            if w.flag in ["nrt","n","nt","nz","nr","ns","nz","eng"]:#只提取名词
                #print w
                content += str(w).split('/')[0]#去掉词性
                count += 1
                if count == 3 :
                    break
                content +=" "
        return content
    #__getKeyWord

#-------------------------------------------------推荐函数集合-------------------------------------------------#

    def recommendation(self,user_id,PATH,N = 1,DAY = 2):
        result = []
        result += self.__recommendFromKeyword(user_id, N, DAY)
        result += self.__everyClassificationRecommendation(user_id,PATH, N, DAY)
        return result

    '''
        推荐函数实体
    
    '''
    #recommendation
    
    def __everyClassificationRecommendation(self,user_id,PATH,N = 1,DAY = 2):
         #推荐的条数
        
        result = []
        #num = XpathXmlParse().getNumOfClassification("NewsfeedsSoftware/spiders/spiderStartupController_package/Configuration.xml")
        num = XpathXmlParse().getNumOfClassification(PATH)
        num = int(num)      #文章种类数
        articalth = []      #每种类型的指针，用于记录上次推荐的位置
        for n in range(num):
            articalth.append(0)
        
        user = User_id.objects.get(userID = user_id)
        
        readArtical = dict()#用来防止文章重复
        self.__articleRecheck(readArtical, user, DAY)#用来防止文章重复         
        points = user.pointToArtical.split("$")
        #-----------------------------------------------------
        i = 0
        for p in points:
            if p.strip() != "" and i < len(articalth):
                articalth[i]=int(p)
            i += 1
        
        for n in range(num):
            artic = Artical.objects.filter(classification=str(n)).values()[articalth[n]:articalth[n]+N]
            if len(artic) != 0:
                if len(artic) < N:
                    articalth[n] += len(artic)
                else:
                    articalth[n] += N
                for art in artic:
                    if art["md5Code"] not in readArtical:
                        result.append(art)
                        readArtical[art["md5Code"]] = art["date"]
        for r in result:
                print r["title"],r["classification"]
        #-----------------------------------------------------
        
        art = ""
        for n in articalth:
            art += str(n)+"$"
        
        self.__writeRecheckMd5Code(user,readArtical,DAY)
        user.pointToArtical = art
        user.save()
        return result
        
        
    '''
        从每一种类型（classification）中选取一篇文章向用户推荐
    
    '''
    #__everyClassificationRecommendation
    
    
    
    
    
    def __recommendFromKeyword(self,user_id,N = 1,DAY = 2):
        #keystr = "$小品-7?0$新闻-7?2$王雪-7?0$刘德华-4?2$相声-3?1$小米-3?1"#从数据库读取
        #read_artical_md5Code:"$c600639e6e476782dfb8e97c3ba200db?121234343(时间)"
        user = User_id.objects.get(userID=user_id)
        keystr = user.keywords
        pointToKey = 6
        readArtical = dict()#用来防止文章重复
        self.__articleRecheck(readArtical, user, DAY)#用来防止文章重复                
        
        keySet = keystr.split("$")
        keyWordresult = []#结果:[['小品',7,0],['新闻',7,2]]
        recommendResult = []
        for k in keySet:
            if k =="":
                continue
            ks = k.split("-")
            kss = ks[1].split("?")
            keyWordresult.append([ks[0],int(kss[0]),int(kss[1])])
            
        num = 0
        if len(keyWordresult) <= 5:
            num = len(keyWordresult)
        else:
            num = 5
        for i in range(num):
            print keyWordresult[i][0],keyWordresult[i][2]
            artic = Artical.objects.filter(keyword__icontains=keyWordresult[i][0]).values()[keyWordresult[i][2]:keyWordresult[i][2]+N]
            if len(artic) < N:
                keyWordresult[i][2] += len(artic)
            else:
                keyWordresult[i][2] += N
            #-----------------------以下部分是查重-------------------------------
            for art in artic:
                if art["md5Code"] not in readArtical:
                    recommendResult.append(art)
                    readArtical[art["md5Code"]] = art["date"]
            #-----------------------------------------------------------------
        if len(keyWordresult) > 5:
            print "else 部分"
            pointToKey = user.pointToKeyword
            for i in range(5):
                if pointToKey >= len(keyWordresult):
                    pointToKey = 6
                print keyWordresult[pointToKey][0],keyWordresult[pointToKey][2]
                artic = Artical.objects.filter(keyword__icontains=keyWordresult[pointToKey][0]).values()[keyWordresult[pointToKey][2]:keyWordresult[pointToKey][2]+N]
                if len(artic) < N:
                    keyWordresult[pointToKey][2] += len(artic)
                else:
                    keyWordresult[pointToKey][2] += N
                pointToKey += 1
                #-----------------------以下部分是查重-------------------------------
                for art in artic:
                    if art["md5Code"] not in readArtical:
                        recommendResult.append(art)
                        readArtical[art["md5Code"]] = art["date"]
                #-----------------------------------------------------------------
                
#        print NumOfKeyWord
         
        self.__writeRecheckMd5Code(user, readArtical, DAY)
        
            
        user.keywords=""
        for k in keyWordresult:
            user.keywords += "$"+str(k[0])+"-"+str(k[1])+"?"+str(k[2])
        
        if pointToKey >= len(keyWordresult):
            pointToKey = 6                  #防止越界
        user.pointToKeyword = pointToKey
        
        user.save()
        
        for r in recommendResult:
            print r["title"],r["keyword"],r["md5Code"]
        return recommendResult
            
    #recommendFromKeyword
    
    def __articleRecheck(self,readArtical,user,DAY):
        art = user.read_artical_md5Code.split('$')
        for md5 in art:
            if str(md5).strip() != "":
                Md5 = str(md5).split("?")
                if Md5[0]!="" :
                    #print time.time()-time.mktime(time.strptime(Md5[1],'%Y-%m-%d'))
                    if (DAY==0 or time.time()-time.mktime(time.strptime(Md5[1],'%Y-%m-%d')))<=(DAY*24*60*60):
                        readArtical[Md5[0]] = Md5[1]
    #__articleRecheck
    
    def __writeRecheckMd5Code(self,user,readArtical,DAY):
        user.read_artical_md5Code=""
        for k in readArtical:
            if DAY==0 or time.time()-time.mktime(time.strptime(str(readArtical[k]),'%Y-%m-%d'))<=DAY*24*60*60:
                user.read_artical_md5Code += '$'+str(k)+"?"+str(readArtical[k])
    #__writeRecheckMd5Code
#------------------------------------------------------------------------------------------------------------#

    def __unicode__(self):
        return "title:"+self.title+" content:"+self.content+" keyword:"+self.keyword+" date:"+self.date+" md5Code:"+self.md5Code
    #__unicode__
    
    
    
    
    #set get del
    
    def get_image_url(self):
        return self.__ImageURL


    def set_image_url(self, value):
        self.__ImageURL = value


    def del_image_url(self):
        del self.__ImageURL

    
    def get_classification(self):
        return self.__Classification


    def set_classification(self, value):
        self.__Classification = value


    def del_classification(self):
        del self.__Classification
    
    
    def get_md_5_code(self):
        return self.__Md5Code


    def set_md_5_code(self, value):
        self.__Md5Code = value


    def del_md_5_code(self):
        del self.__Md5Code
    
    def get_title(self):
        return self.__Title


    def get_content(self):
        return self.__Content


    def set_title(self, value):
        self.__Title = value


    def set_content(self, value):
        self.__Content = value


    def del_title(self):
        del self.__Title


    def del_content(self):
        del self.__Content
    
    def get_address(self):
        return self.__Address


    def set_address(self, value):
        self.__Address = value

    def del_address(self):
        del self.__Address
    
    Title = property(get_title, set_title, del_title, "Title's docstring")
    Content = property(get_content, set_content, del_content, "Content's docstring")
    Address = property(get_address, set_address, del_address, "Address's docstring")
    Md5Code = property(get_md_5_code, set_md_5_code, del_md_5_code, "Md5Code's docstring")
    Classification = property(get_classification, set_classification, del_classification, "Classification's docstring")
    ImageURL = property(get_image_url, set_image_url, del_image_url, "ImageURL's docstring")

#class Artical


class User_id(models.Model):
    userID = models.IntegerField()
    read_artical_md5Code = models.TextField()
    keywords = models.TextField()
    pointToArtical = models.TextField()
    pointToKeyword = models.IntegerField()
    date = models.DateField(auto_now_add = True)
    
    
    def insertUser(self,userid):
        User_id.objects.create(userID=userid,read_artical_md5Code="",keywords="",pointToArtical = "",pointToKeyword = 6)
    def getLastUserId(self):
        u = User_id.objects.all().order_by('-userID')[0]
        return u.userID
    def readArtiaclThenAppendKeywords(self,userid,md5):
        cont = Artical.objects.filter(md5Code=md5).values()
        if len(cont)!=0:
            self.__updateKeywords(userid, str(cont[0]['keyword']))
            
    
    def __updateKeywords(self,userid,keywords):
        #u.keywords的格式为 $关键词-2(关键词出现次数)?23(上次在指针在数据库中的位置)
        #key = "$小品-7?0$新闻-7?2$王雪-7?0$刘德华-4?2$相声-3?1"
        u = User_id.objects.get(userID=userid)
        keyword = ""
        keywords = keywords.strip()
        keywordsSet = keywords.split(" ")
        key=str(u.keywords.strip())
        keyDic = dict()
        keySet = key.split("$")
        for k in keySet:
            ks = k.split('-')
            if ks[0]!='':
                kss = ks[1].split('?')
                if kss[1].strip()=="":
                    kss[1]="0"
                keyDic[ks[0]]=[int(kss[0]),int(kss[1])]
                
        for k in keywordsSet:
            if k in keyDic:
                keyDic[k][0] += 1
            elif k!="":
                keyDic[k]=[1,0]
                
        keyDic= sorted(keyDic.iteritems(), key=lambda d:d[1], reverse = True)
        for k in keyDic:
            keyword += "$"+k[0]+"-"+str(k[1][0])+"?"+str(k[1][1])
        u.keywords = keyword
        u.save()
        #print keyword
    #__updateKeywords
    
    def updatePointToArtical(self):
        return None
    #updatePointToArtical
    
#class User_id
class RelatedReading(models.Model):
    mymd5 = models.CharField(max_length = 32)
    first = models.CharField(max_length=32)
    second = models.CharField(max_length=32)
    third = models.CharField(max_length=32)
    fouth = models.CharField(max_length=32)
    fifth = models.CharField(max_length=32)
    sixth = models.CharField(max_length=32)
    
    def insertRelatedReading(self,md5,keywords,myclassification):
        keywords = keywords.strip().split(' ')
        relateQueue = []
        for key in keywords:

            articals = Artical.objects.order_by("-date").filter(keyword__contains=key).values()
            for artical in articals:
                print artical["title"],artical["md5Code"]
                if artical["md5Code"]!=md5:
                    relateQueue.append(artical["md5Code"])

        
        if len(relateQueue) < 6 :
            #print "*******************小于六*******************"
            articals = Artical.objects.order_by("-date").filter(classification=myclassification).values()
            for artical in articals:
                if len(relateQueue) >=6 :
                    break;
                #print artical["title"],artical["md5Code"]
                if artical["md5Code"]!=md5:
                    relateQueue.append(artical["md5Code"])
            while len(relateQueue) < 6:
                relateQueue.append("")
        RelatedReading.objects.create(mymd5 = md5,first=relateQueue[0],second=relateQueue[1],third=relateQueue[2],fouth=relateQueue[3],fifth=relateQueue[4],sixth=relateQueue[5])
        
    def getRelatedArtical(self,md5):
        ar = RelatedReading.objects.filter(mymd5=md5).values()
        if len(ar)!=0:
            art = ar[0]
            print art
            result = dict()
            if len(art['first'])!=0:
                artical = Artical.objects.filter(md5Code = art['first']).values()
                if len(artical)!=0:
                    result[art['first']] = artical[0]['title']
            if len(art['second'])!=0:
                artical = Artical.objects.filter(md5Code = art['second']).values()
                if len(artical)!=0:
                    result[art['second']] = artical[0]['title']
            if len(art['third'])!=0:
                artical = Artical.objects.filter(md5Code = art['third']).values()
                if len(artical)!=0:
                    result[art['third']] = artical[0]['title']
            if len(art['fouth'])!=0:
                artical = Artical.objects.filter(md5Code = art['fouth']).values()
                if len(artical)!=0:
                    result[art['fouth']] = artical[0]['title']
            if len(art['fifth'])!=0:
                artical = Artical.objects.filter(md5Code = art['fifth']).values()
                if len(artical)!=0:
                    result[art['fifth']] = artical.values()[0]['title']
            if len(art['sixth'])!=0:
                artical = Artical.objects.filter(md5Code = art['sixth']).values()
                if len(artical)!=0:
                    result[art['sixth']] = artical[0]['title']
            return result
    

