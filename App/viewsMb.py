__author__ = 'blaczom4gmail'

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *
from App.utils import log
from App.models import Article, ArticleType
from math import ceil
import json

def getRest(request, aGetType=""):
    print('i get here', request.GET.get('jpargs', '0'))

    lArtId = request.GET.get('reqid', '0')

    lPageNo = int(request.GET.get('reqpg', '1'))
    lPagePer = int(request.GET.get('reqpr', '10'))
    lPageNo = 1 if lPageNo < 1 else lPageNo
    lPageAll = 1

    renderVal = {"title": "",
                 "artId": lArtId,
                 "contList": [],
                 "contSingle": {}
                }

    try:
        if len(lArtId) > 10: lSingle = True
        else: lSingle=False

        if aGetType == "resec":      # 这里只是一个栏目的名字。具体显示模块是靠html文件定义的。
          pass
    finally:
      pass


    data = {
    'name':"test jsonp",
    'gendar': "sexual",
    }

    callback = request.GET['callback']

    return HttpResponse('%s(%s)' % (callback, json.dumps(data)))