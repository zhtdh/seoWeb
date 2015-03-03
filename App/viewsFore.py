__author__ = 'blaczom'

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *
from App.utils import log
from App.models import Article, ArticleType

@require_http_methods(["GET"])
def gool(request, goolArg="", goolSecArg=""):

    renderVal = {"title":"山东鼎成卫星导航定位技术有限公司",
                 "position" : [("公司", '/top/'), ("公司简介", '/resec/1/')],
                 "isList": False,
                 "leftList1": [],
                 "contList" :[],
                 "contSingle" : {}
                }
    try:
        if goolArg == "resec":      # 这里只是一个模版的名字。
            if goolSecArg == "1":
                renderVal["position"] = [("公司", '/resec/'), ("公司简介", '/resec/1/')]
                renderVal["contSingle"] = ArticleType.objects.filter(kind__icontains=',corp-1-corpinfo-1,')[0].fk_article.all()[:1].values()[0]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                return render(request, "rendSec-cont.html", {"renderVal": renderVal})
            elif goolSecArg == "2":    # 资质荣誉
                renderVal["position"] = [("公司", '/resec/'), ("资质荣誉", '/resec/2/')]
                renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-honor-1,')[0].fk_article.all().values()
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                return render(request, "rendSec-list.html", {"renderVal": renderVal})
            elif goolSecArg == "3":

                return render(request, "rendSec.html", locals())
            elif goolSecArg == "4":

                return render(request, "rendSec.html", locals())
            else:
                return HttpResponseRedirect(goolArg + "/1/")
        elif goolArg == "rethi":

            return render(request, "rendThi.html")
        elif goolArg == "refou":
            return render(request, "rendFou.html")
        elif goolArg == "refiv":
            return render(request, "rendFiv.html", locals())
        elif goolArg == "recon":
            contact = ArticleType.objects.filter(kind__icontains=',topContact,')[0].fk_article.all()[:1].values()[0]
            return render(request, "rendCon.html",locals())
        else:
            return HttpResponseRedirect("/")

    except Exception as e:
        log("gool执行错误：%s" % str(e.args))
        return HttpResponse("gool执行错误：%s" % str(e.args))

def home(request):
    showCaseList = ArticleType.objects.filter(kind__icontains=',top-1-showcase-1-list-n,').values()
    return render(request, "home.html",locals())
