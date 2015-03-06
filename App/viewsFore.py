__author__ = 'blaczom'

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *
from App.utils import log
from App.models import Article, ArticleType
from math import ceil
from App import gNavCache,gNavPosCache



@require_http_methods(["GET"])
def gool(request, goolArg="", goolSecArg=""):
    navMenuList = getNav()

    lArtId = request.GET.get('reqid', '0')

    lPageNo = int(request.GET.get('reqpg', '1'))
    lPagePer = int(request.GET.get('reqpr', '10'))
    lPageNo = 1 if lPageNo < 1 else lPageNo
    lPageAll = 1

    renderVal = {"title": "山东鼎成卫星导航定位技术有限公司",
                 "boardPic": "/static/img/top1.jpg",
                 "position": [("公司", '/resec/1/'), ("公司简介", '/resec/1/')],
                 "artId": lArtId,
                 "leftList1": [],
                 "contList": [],
                 "contSingle": {}
                }
    try:
        if len(lArtId) > 10: lSingle = True
        else: lSingle=False

        if goolArg in ("resec","rethi","refou","refiv","recon") :
          if goolSecArg:
            renderVal["position"].append(("公司", '/resec/1/'))
            renderVal["position"].append(("公司", '/resec/1/'))
          else:
            pass
          renderVal["position"] = []

        if goolArg == "resec":      # 这里只是一个栏目的名字。具体显示模块是靠html文件定义的。
            if goolSecArg == "1":   # 公司页面：直接显示第一条记录的内容。

                renderVal["contSingle"] = ArticleType.objects.filter(kind__icontains=',corp-1-corpinfo-1,')[0].fk_article.all()[:1].values()[0]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                return render(request, "rendFrame-single.html", locals())
            elif goolSecArg == "2":    # 资质荣誉：直接显示所有记录的图片链接。点击图片，显示详细信息。
                renderVal["position"] = [("公司", '/resec/1/'), ("资质荣誉", '/resec/2/')]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                if lSingle:
                    renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                    return render(request, "rendFrame-single.html", locals())
                else:
                    lPageAll = 1
                    renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-honor-1,')[0].fk_article.all().order_by('exorder').values()
                    return render(request, "rendFrame-endless3.html", locals())
            elif goolSecArg == "3":    # 企业动态
                renderVal["position"] = [("公司", '/resec/1/'), ("企业动态", '/resec/3/')]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                if lSingle:
                    renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                    return render(request, "rendFrame-single.html", locals())
                else:
                    renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-activity-1,')[0].fk_article.all().order_by('-exorder')[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                    lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',corp-1-activity-1,')[0].fk_article.all().count() / lPagePer)
                    return render(request, "rendFrame-table.html", locals())
            elif goolSecArg == "4":    # 行业新闻
                renderVal["position"] = [("公司", '/resec/1/'), ("行业新闻", '/resec/4/')]
                renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
                if lSingle:
                    renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                    return render(request, "rendFrame-single.html", locals())
                else:
                    renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',corp-1-news-1,')[0].fk_article.all().order_by('-exorder')[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                    lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',corp-1-news-1,')[0].fk_article.all().count() / lPagePer)
                    return render(request, "rendFrame-table.html", locals())
            else:
                return HttpResponseRedirect('/' + goolArg + "/1/")
        elif goolArg == "rethi":    # 行业应用：全部都是一个模式。
            renderVal["boardPic"] = "/static/img/top2.jpg"
            lPagePer = 6
            if goolSecArg == "1":
              renderVal["position"] = [("产品应用", '/' + goolArg + '/1/'), ("产品应用", '/' + goolArg + '/1/')]
            elif goolSecArg == "2":
              renderVal["position"] = [("产品应用", '/' + goolArg + '/1/'), ("产品应用", '/' + goolArg + '/2/')]
            elif goolSecArg == "3":
              renderVal["position"] = [("产品应用", '/' + goolArg + '/1/'), ("产品应用", '/' + goolArg + '/3/')]
            elif goolSecArg == "4":
              renderVal["position"] = [("产品应用", '/' + goolArg + '/1/'), ("产品应用", '/' + goolArg + '/4/')]
            else:
              return HttpResponseRedirect('/' + goolArg + "/1/")
            renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',app-1-list1-n,').order_by('exorder').values()

            if lSingle:
                renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                return render(request, "rendFrame-single.html", locals())
            else:
                renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',app-1-app' + goolSecArg + '-1,')[0].fk_article.all().order_by('-exorder')[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',app-1-app' + goolSecArg + '-1,')[0].fk_article.all().count() / lPagePer)
                return render(request, "rendFrame-line.html", locals())

        elif goolArg == "refou":  # 典型客户，左边链接显示公司的左边链接。
            renderVal["boardPic"] = "/static/img/top3.jpg"
            renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
            renderVal["position"] = [("典型客户", '/' + goolArg + '/')]
            if lSingle:
                renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                return render(request, "rendFrame-single.html", locals())
            else:
                renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',case-1,')[0].fk_article.all().order_by('-exorder')[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',case-1,')[0].fk_article.all().count() / lPagePer)
                return render(request, "rendFrame-table.html", locals())

        elif goolArg == "refiv":   # 行业应用。
            renderVal["boardPic"] = "/static/img/top4.jpg"
            lPagePer = 9
            if goolSecArg == "1":
              renderVal["position"] = [("行业应用", '/' + goolArg + '/1/'), ("行业应用", '/' + goolArg + '/1/')]
            elif goolSecArg == "2":
              renderVal["position"] = [("行业应用", '/' + goolArg + '/1/'), ("行业应用", '/' + goolArg + '/2/')]
            elif goolSecArg == "3":
              renderVal["position"] = [("行业应用", '/' + goolArg + '/1/'), ("行业应用", '/' + goolArg + '/3/')]
            elif goolSecArg == "4":
              renderVal["position"] = [("行业应用", '/' + goolArg + '/1/'), ("行业应用", '/' + goolArg + '/4/')]
            else:
              return HttpResponseRedirect('/' + goolArg + "/1/")
            renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',ind-1-list1-n,').order_by('exorder').values()

            if lSingle:
                renderVal["contSingle"] = Article.objects.filter(id=lArtId).values()[0]
                return render(request, "rendFrame-single.html", locals())
            else:
                renderVal["contList"] = ArticleType.objects.filter(kind__icontains=',ind-1-ind' + goolSecArg + '-1,')[0].fk_article.all().order_by('-exorder')[(lPageNo-1)*lPagePer:lPageNo*lPagePer].values()
                lPageAll = ceil(ArticleType.objects.filter(kind__icontains=',ind-1-ind' + goolSecArg + '-1,')[0].fk_article.all().count() / lPagePer)
                return render(request, "rendFrame-grid3.html", locals())
        elif goolArg == "recon": # 联系我们，左边链接显示公司的左边链接。
            renderVal["boardPic"] = "/static/img/top5.jpg"
            renderVal["position"] = [("联系我们", '/' + goolArg + '/')]
            renderVal["contSingle"] = ArticleType.objects.filter(kind__icontains=',cont-1,')[0].fk_article.all()[:1].values()[0]
            renderVal["leftList1"] = ArticleType.objects.filter(kind__icontains=',corp-1-list1-n,').order_by('exorder').values()
            return render(request, "rendFrame-single.html", locals())
        else:
            return HttpResponseRedirect("/")

    except Exception as e:
        log("gool执行错误：%s" % str(e.args))
        raise(e)
        return HttpResponse("gool执行错误：%s" % str(e.args))

def home(request):
    showCaseList = ArticleType.objects.filter(kind__icontains=',top-1-showcase-1-list-n,').values()
    navMenuList = getNav()
    gridShowList = ArticleType.objects.filter(kind__icontains=',top-1-grid-1-list-n,').values('title', 'exlink', 'remark', 'link')
    # rightBarList 很不友好。 1、2、3、4排序来的。4是视频
    rightBarList = ArticleType.objects.filter(kind__icontains=',top-1-right-1-n,').order_by('exorder').values('title', 'exlink', 'remark', 'link')
    # 得到1、2的列表内容前5项
    rightBarGet1List = ArticleType.objects.filter(kind__icontains = rightBarList[0]["exlink"])[0].fk_article.all()[0:5].values('title', 'id', 'rectime', 'link')
    rightBarGet2List = ArticleType.objects.filter(kind__icontains = rightBarList[1]["exlink"])[0].fk_article.all()[0:5].values('title', 'id', 'rectime', 'link')

    return render(request, "home.html", locals())

def getNav():
    # return [ {"title":"", "hasChild":False, "childList":[{title:"", "link":""},{}...], "link":"" },  ... ]
    global gNavCache  # 全局缓冲，防止每次都查询数据库导航菜单。
    global gNavPosCache
    if len(gNavCache) > 0:
        pass
    else:
        navTopList = ArticleType.objects.filter(kind__icontains=',nav0-n,').order_by('exorder').values()
        navSecList = ArticleType.objects.filter(kind__icontains=',nav0-n-nav1-n,').order_by('exorder').values()
        navAllList = []
        for iTop in navTopList:
            childListTmp = []
            hasChildTmp = False
            gNavPosCache.update({iTop['link']: iTop}) # 缓存所有的记录。方便查找拉。
            for iSub in navSecList:
                if iSub["parent_id"] == iTop["id"]:
                    hasChildTmp = True
                    childListTmp.append( { "title": iSub["title"], "link":iSub["link"] } )
                    l_tmp = iSub
                    l_tmp.update( {"upPosition": iTop["title"]} )
                    gNavPosCache.update({iSub['link']: l_tmp}) # 缓存所有的记录。方便查找拉。
            navAllList.append({"title": iTop["title"], "link":iTop["link"], "hasChild":hasChildTmp, "childList":childListTmp })
        log("-- i select database for menu --")
        gNavCache = navAllList
    return gNavCache




