__author__ = 'blaczom4gmail'

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *
from App.utils import log
from App.models import Article, ArticleType
from math import ceil
import json


def getPageRow(adict):  # {"pn":1,"pr":10,"pa":0}
  first_row = (adict['pn'] - 1) * adict['pr']
  last_row = first_row + adict['pr']
  return first_row, last_row, adict['pa']

def getJsonp(request):
  # 处理手机端发来的请求。 var ls_json = {"fun":"type", "pid":"", "id": "xxxx", "loc":{"pn":1,"pr":10,"pall":0} };
  ldict = json.loads(request.GET.get('jpargs', ''))
  print('getJsonp here : ', ldict)

  try:
    if 'fun' not in ldict:
      raise('上传参数错误')

    l_getType =  ldict['fun']  #  ldict['exp']   ldict['exp']= {pid: xxx, loc :{"pn":1,"pr":10,"pall":0} }
    p_rtn = {}
    t = None;

    if l_getType == "typelist":
      if ldict['exp'] == 'corp':
        t = ArticleType.objects.filter(kind__icontains=',corp-1,')
      elif ldict['exp'] == 'product':
        t = ArticleType.objects.filter(kind__icontains=',app-1,')
      elif ldict['exp'] == 'industry':
        t = ArticleType.objects.filter(kind__icontains=',ind-1,')
      elif ldict['exp'] == 'custom':
        t = ArticleType.objects.filter(kind__icontains=',case-1,')
      else:
        pass
      rtn_list = list(ArticleType.objects.filter(parent_id = t).values('id', 'title', 'parent_id'))
      p_rtn.update({
        "rtnInfo": '成功',
        "rtnCode": 1,
        "exObj": { "data": rtn_list }
      })
    elif l_getType == "artlist":
      #  ldict['exp']   ldict['exp']= {pid: xxx, loc :{"pn":1,"pr":10,"pa":0} }

      l_first , l_end, l_all = getPageRow( ldict['exp']['loc'] )

      if (l_all < 0):
        l_all = Article.objects.filter(parent_id = ldict['exp']['pid']).count()
      print('custom artlist', l_first, l_end, l_all)
      rtn_list = list(Article.objects.filter(parent_id = ldict['exp']['pid'])[l_first:l_end].values('id', 'title'))

      p_rtn.update({
        "rtnInfo": '成功',
        "rtnCode": 1,
        "exObj": { "data": rtn_list, "loc":{"pa": l_all} }
      })
    elif l_getType == "getart":
      rtn_list = list(Article.objects.filter(id = ldict['exp']['pid']).values('id', 'title', 'content', 'rectime', 'recname'))
      p_rtn.update({
        "rtnInfo": '成功',
        "rtnCode": 1,
        "exObj": { "data": rtn_list }
      })
    else:
      pass

    callback = request.GET['callback']
  except Exception as e:
    print("ajaxResp.dealPAjax执行错误：%s" % str(e.args))
    raise e
  finally:
    pass

    print('response now', p_rtn)
    return HttpResponse('%s(%s)' % (callback, json.dumps(p_rtn)))


def getArticleList(p_dict, p_rtn):
  firstRow, lastRow, rowTotal = getPageRowNo(p_dict['location'])
  articles = list(Article.objects.filter(parent_id=p_dict['columnId']) \
                    .order_by('-rectime').values('id', 'title', 'recname', 'rectime')[firstRow:lastRow])
  if rowTotal == 0:
    total = Article.objects.filter(parent_id=p_dict['columnId']).count()
  else:
    total = -1
  p_rtn.update(genRtnOk("查询文章列表成功。") )
  p_rtn.update({ "exObj": {  "rowCount": total,  "contentList": articles } })

