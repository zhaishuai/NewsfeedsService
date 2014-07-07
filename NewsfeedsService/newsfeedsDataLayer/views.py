# -*- coding:UTF-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import User_id,Artical,RelatedReading
from django.template.loader import get_template 
from django.template import Context
from django.http import HttpResponse
import os

global next_user_id #�扮��风�id
next_user_id = User_id().getLastUserId() + 1

@api_view(['GET', 'PUT', 'DELETE'])
def creatUser(request):
    if request.method == 'GET':
        global next_user_id
        User_id().insertUser(next_user_id)
        next_user_id += 1
        return Response(next_user_id-1)
    
@api_view(['GET', 'PUT', 'DELETE'])
def recommendation(request):
    user_id = None
    print request.GET
    for k in request.GET:
        user_id = k
    artical = None
    #print os.getcwd()
    if user_id != None:
        artical = Artical().recommendation(user_id,"NewsfeedsService/NewsfeedsSoftware/spiders/spiderStartupController_package/Configuration.xml")
    return Response(artical)
@api_view(['GET', 'PUT', 'DELETE'])
def readArtical(request):
    #http://192.168.6.13:8003/readArtical?1=bf4d5937c5b4e93f999ddc5ec2fab863
    user_id = None
    req = request.GET
    for k in req:
        user_id = k
    md5 = req[k]
    User_id().readArtiaclThenAppendKeywords(user_id, md5)
    
    return Response(RelatedReading().getRelatedArtical(md5))

@api_view(['GET', 'PUT', 'DELETE'])
def readRelatedArtical(request):
    user_id = None
    req = request.GET
    for k in req:
        user_id = k
    md5 = req[k]
    artical = Artical.objects.filter(md5Code=md5).values()
    if len(artical)!=0:
        artical = artical[0]
    dic = {"artical":artical,"RelatedReading":RelatedReading().getRelatedArtical(md5)}
    return Response(dic)

@api_view(['GET', 'PUT', 'DELETE'])
def getUserKeyWord(request):
    user_id = None
    print request.GET
    for k in request.GET:
        user_id = k
    keyword = User_id.objects.filter(userID = user_id).values()[0]["keywords"]
    keywordSet = dict()
    for key in keyword.strip().split('$'):
        if key !="":
            word = key.split('-')
            count = word[1].split('?')
            keywordSet[word[0]] = count[0]
    keywordSet= sorted(keywordSet.iteritems(), key=lambda d:d[1], reverse = True)
    keyDic = []
    length = len(keywordSet)
    count = 0
    
    while count<length and count<50:
        keyDic.append("{text:"+'"'+keywordSet[count][0]+'"' + ","+"weight:"+keywordSet[count][1]+"}")
        count += 1
    
    t = get_template('index.html')
    html = t.render(Context({'user_key_word': keyDic}))
                    
    return HttpResponse(html)

@api_view(['GET', 'PUT', 'DELETE'])
def getArticalByKind(request):
    kind = None
    req = request.GET
    for k in req:
        kind = k
    page = req[kind]
    
    artic = Artical.objects.order_by('-date').filter(classification=kind).values()[int(page):int(page)+20]
    return Response(artic)

@api_view(['GET', 'PUT', 'DELETE'])
def getHtml(request):
    t = get_template('index.html')
    html = t.render(Context('user_key_word'))
    return HttpResponse(html)
    