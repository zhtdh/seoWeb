__author__ = 'blaczom'

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *
from App.utils import log
from App.models import Article, ArticleType
from math import ceil

@require_http_methods(["GET"])
def gool(request, goolArg="", goolSecArg=""):
    lArtId = request.GET.get('reqid', '0')
    lPageNo = int(request.GET.get('reqpg', '1'))
    lPagePer = int(request.GET.get('reqpr', '10'))
    lPageNo = 1 if lPageNo < 1 else lPageNo
    lPageAll = 1
    renderVal = {"title":"山东鼎成卫星导航定位技术有限公司",
                 "position" : [("公司", '/resec/1/'), ("公司简介", '/resec/1/')],
                 "artId" : lArtId,
                 "leftList1": [],
                 "contList" :[],
                 "contSingle" : {}    }
    try:
        if len(lArtId) > 10: lSingle = True
        else: lSingle=False

        if goolArg == "resec":      # 这里只是一个栏目的名字。具体显示模块是靠html文件定义的。
            if goolSecArg == "1":   # 公司页面：直接显示第一条记录的内容。
                renderVal["position"] = [("公司", '/resec/1/'), ("公司简介", '/resec/1/')]
                renderVal["contSingle"] = ArticleType.objects.filter(kind__icontains=',corp-1-corpinfo-1,')[0].fk_article.all()[:1].values()[0]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                return render(request, "rendSec-cont.html", {"renderVal": renderVal})
            elif goolSecArg == "2":    # 资质荣誉：直接显示所有记录的图片链接。点击图片，显示详细信息。
                renderVal["position"] = [("公司", '/resec/1/'), ("资质荣誉", '/resec/2/')]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                if lSingle:
                    renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                    return render(request, "rendSec-cont.html", locals())
                else:
                    lPageAll = 1
                    renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-honor-1,')[0].fk_article.all().values()
                    return render(request, "rendSec-list.html", locals())
            elif goolSecArg == "3":
                renderVal["position"] = [("公司", '/resec/1/'), ("企业动态", '/resec/3/')]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                if lSingle:
                    renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                    return render(request, "rendSec-cont.html", locals())
                else:
                    renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-activity-1,')[0].fk_article.all()[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                    lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',corp-1-activity-1,')[0].fk_article.all().count() / lPagePer)
                    return render(request, "rendFou-list.html", locals())
            elif goolSecArg == "4":
                renderVal["position"] = [("公司", '/resec/1/'), ("行业新闻", '/resec/4/')]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                if lSingle:
                    renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                    return render(request, "rendSec-cont.html", locals())
                else:
                    renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-news-1,')[0].fk_article.all()[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                    lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',corp-1-news-1,')[0].fk_article.all().count() / lPagePer)
                    return render(request, "rendFou-list.html", locals())
            else:
                return HttpResponseRedirect('/' + goolArg + "/1/")
        elif goolArg == "rethi":    # 行业应用：全部都是一个模式。
            lPagePer = 6
            if goolSecArg == "1":
              renderVal["position"] = [("应用", '/' + goolArg + '/1/'), ("应用1", '/' + goolArg + '/1/')]
            elif goolSecArg == "2":
              renderVal["position"] = [("应用", '/' + goolArg + '/1/'), ("应用1", '/' + goolArg + '/2/')]
            elif goolSecArg == "3":
              renderVal["position"] = [("应用", '/' + goolArg + '/1/'), ("应用1", '/' + goolArg + '/3/')]
            elif goolSecArg == "4":
              renderVal["position"] = [("应用", '/' + goolArg + '/1/'), ("应用1", '/' + goolArg + '/4/')]
            else:
              return HttpResponseRedirect('/' + goolArg + "/1/")
            renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',app-1-list1-n,').order_by('exorder').values()

            if lSingle:
                renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                return render(request, "rendSec-cont.html", locals())
            else:
                renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',app-1-app' + goolSecArg + '-1,')[0].fk_article.all()[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',app-1-app' + goolSecArg + '-1,')[0].fk_article.all().count() / lPagePer)
                return render(request, "rendThi-list.html", locals())

        elif goolArg == "refou":  # 典型客户，左边链接显示公司的左边链接。
            renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
            renderVal["position"] = [("典型客户", '/' + goolArg + '/')]
            if lSingle:
                renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                return render(request, "rendSec-cont.html", locals())
            else:
                renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',case-1,')[0].fk_article.all()[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',case-1,')[0].fk_article.all().count() / lPagePer)
                return render(request, "rendFou-list.html", locals())

        elif goolArg == "refiv":
            return render(request, "rendFiv.html", locals())
        elif goolArg == "recon":
            contact = ArticleType.objects.filter(kind__icontains=',topContact,')[0].fk_article.all()[:1].values()[0]
            return render(request, "rendCon.html",locals())
        else:
            return HttpResponseRedirect("/")

    except Exception as e:
        log("gool执行错误：%s" % str(e.args))
        raise(e)
        return HttpResponse("gool执行错误：%s" % str(e.args))

def home(request):
    showCaseList = ArticleType.objects.filter(kind__icontains=',top-1-showcase-1-list-n,').values()
    return render(request, "home.html",locals())
