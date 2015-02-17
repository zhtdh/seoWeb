__author__ = 'blaczom'

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *
from App.utils import log
from App.models import Article, ArticleType

@require_http_methods(["GET"])
def gool(request, goolArg="", goolSecArg=""):
    try:
        if goolArg == "resec":
            corpInfo = getCorpInfo()
            return render(request, "rendSec.html", locals())
        elif goolArg == "rethi":
            return render(request, "rendThi.html")
        elif goolArg == "refou":
            return render(request, "rendFou.html")
        elif goolArg == "refiv":
            return render(request, "rendFiv.html", locals())
        elif goolArg == "recon":
            contact = getContact
            return render(request, "rendCon.html",locals())
        else:
            return HttpResponseRedirect("/")
    except Exception as e:
        log("gool执行错误：%s" % str(e.args))
        return HttpResponse("gool执行错误：%s" % str(e.args))

def home(request):
    return render(request, "home.html")

def getCorpInfo():
    try:
        return ArticleType.objects.filter(kind__icontains=',corpinfo,')[0].fk_article.all()[:1].values()[0]
    except IndexError:
        return None

def getContact():
    try:
        return Article.objects.filter(parent_id='0')\
            .filter(kind__icontains='topContact').values('content')[0]['content']
    except IndexError:
        return "无联系方式"