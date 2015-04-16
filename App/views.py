# coding:utf-8
from django.db import connection, transaction
from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError, DatabaseError
from App.utils import *
from App.models import *
from App.ueditor.views import get_ueditor_controller

def test1(request):
  return render(request, "App/test.html")

def getPageRowNo(p_dict):
  """usage:  getPageRowNo( {pageCurrent:当前页, pageRows:一页的行数, pageTotal: 0} )
    :return: (firstRowNo,lastRowNo, rowTotal)
    """
  if 'pageCurrent' not in p_dict or 'pageRows' not in p_dict or 'pageTotal' not in p_dict:
    raise AppException('上传分页参数错误')
  if not (isinstance(p_dict['pageCurrent'], int) and
            isinstance(p_dict['pageRows'], int) and
            isinstance(p_dict['pageTotal'], int)):
    raise AppException('上传分页参数错误')
  first_row = (p_dict['pageCurrent'] - 1) * p_dict['pageRows']
  last_row = first_row + p_dict['pageRows']
  if p_dict['pageTotal'] == 0:
    row_total = 0
  else:
    row_total = -1
  return first_row, last_row, row_total

def logon(session, p_user, p_rtn):
  """usage: logon(request.session, { md5: "xx",username: "aaa" }, rtn) """
  ls_name = p_user['username']
  ls_pw = p_user['md5']
  try:
    user = User.objects.get(username=ls_name)
    if user.pw == ls_pw:
      session['username'] = ls_name
      session['usertype'] = user.usertype
      p_rtn.update({"rtnInfo": "登录成功", "rtnCode": 1 })
    else:
      session["username"] = None
      p_rtn.update({"rtnInfo": "密码错误", "rtnCode": -1  })
  except ObjectDoesNotExist:
    p_rtn.update({"rtnInfo": "用户不存在", "rtnCode": -1  })

def saveArticleType(p_AType):
  if '_exState' not in p_AType:
    pass
  elif p_AType['_exState'] == 'new':  # 添加新的栏目数据
    newType = ArticleType()
    for i in g_type_fields:
      # 如果有这个栏目。
      if i in p_AType.keys():
        newType[i] = p_AType[i]
    newType.save()
  elif p_AType['_exState'] == 'dirty':  # 更新数据
    oldType = ArticleType.objects.get(id=p_AType['id'])
    changed_field = []
    for i in g_type_fields:
      if oldType[i] != str(p_AType[i]) and i not in g_auto_fields:
        oldType[i] = p_AType[i]
        changed_field.append(i)
    oldType.save(update_fields=changed_field)
  elif p_AType['_exState'] == 'clean':
    pass
  else:
    raise AppException('state参数非法!')
  if 'items' in p_AType:
    for i in p_AType['items']:
      saveArticleType(i)

def dealArticleType(p_dict, p_rtn):
  """ usage: dealArticleType(  { "id": 0, "title": "根","items": [{..
              "_exState": "clean",  # new：生成insert，dirty：生成update，clean：忽略。
              "items": []  } ... ], "deleteId": [xxx, xxx]  }, rtn)
  """
  if 'deleteId' in p_dict:
    if len(p_dict['deleteId']) > 0:
      ArticleType.objects.filter(id__in=p_dict['deleteId']).delete()
  saveArticleType(p_dict)
  p_rtn.update(genRtnOk("保存栏目成功。"))

def getArticleType(p_rtn, aExparm):    # {type: user/admin}
  """   返回全部ArticleType """
  l_rtn = {'id': '0','parent_id':None,'title': '根','items': []}
  try:
    getSubArticleType('0', l_rtn['items'], aExparm['type'])
    p_rtn.update( genRtnOk("查询栏目成功。") )
    p_rtn.update({"exObj": { "columnTree": l_rtn }})
  except ObjectDoesNotExist:
    p_rtn.update(genRtnFail(None, "根不存在"))

def getSubArticleType(p_parent_id, p_items, aExType):
  if aExType=="user":
    a_type = ArticleType.objects.filter(parent_id=p_parent_id).exclude(
      exkind__contains=",userinvisible,").values()       # 转化为 [dict{}
  else:
    a_type = ArticleType.objects.filter(parent_id=p_parent_id).values()  # 转化为 [dict{}
  for t in a_type:
    items = []
    getSubArticleType(t['id'], items, aExType)
    l_tmp = {'items': items}
    t.update(l_tmp)
    p_items.append(t)

def getArticleList(p_dict, p_rtn):
  """ usage: getArticleList( {
        location: { pageCurrent:当前页, pageRows:一页的行数,pageTotal:共有多少页 },
        columnId:'xxx'  }, rtn)
  """
  if 'columnId' not in p_dict or 'location' not in p_dict:
    raise AppException('上传参数错误')
  firstRow, lastRow, rowTotal = getPageRowNo(p_dict['location'])
  articles = list(Article.objects.filter(parent_id=p_dict['columnId']) \
                    .order_by('-rectime').values('id', 'title', 'recname', 'rectime')[firstRow:lastRow])
  if rowTotal == 0:
    total = Article.objects.filter(parent_id=p_dict['columnId']).count()
  else:
    total = -1
  p_rtn.update(genRtnOk("查询文章列表成功。") )
  p_rtn.update({ "exObj": {  "rowCount": total,  "contentList": articles } })

def getArticle(p_dict, p_rtn):
  """ usage: getArticle( { articleId: xxx } , p_rtn ) """
  if 'articleId' not in p_dict:
    raise AppException('上传参数错误')
  try:
    article = Article.objects.filter(id=p_dict['articleId']).values()[0]
    p_rtn.update(genRtnOk("查询文章成功。"))
    p_rtn.update({"exObj": {"article": article }} )
  except ObjectDoesNotExist:
    p_rtn.update(genRtnFail(None, "查询文章失败"))

def setArticle(p_dict, p_rtn, request):
  if "article" not in p_dict and '_exState' not in p_dict['article']:
    raise AppException('上传参数错误，缺少article的关键字段')
  l_art = p_dict['article']

  if l_art['_exState'] == 'new':
    recArt = Article()
  elif l_art['_exState'] == 'dirty':
    recArt = Article.objects.get(id=l_art['id'])
  for i in g_article_fields:
    if i not in g_auto_fields and i in l_art: # 传递过来的参数。
      recArt[i] = l_art[i]
  recArt["rectime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  if l_art['_exState'] == 'new':
    recArt["recname"] = request.session["username"]
    recArt.save()
    p_rtn.update(genRtnOk("新纪录保存成功"))
  elif l_art['_exState'] == 'dirty':
    if request.session['username'] == recArt['recname'] or request.session['username'] == 'Admin':
      recArt.save()
      p_rtn.update(genRtnOk("纪录保存成功"))
    elif recArt['recname'] == 'Admin':
      p_rtn.update(genRtnFail(request, "Admin所有的记录只能本人修改。"))
      p_rtn["alertType"] = 1
    elif request.session['usertype'] == "pow":
      recArt.save()
      p_rtn.update(genRtnOk("纪录保存成功"))
    else:
      p_rtn.update(genRtnFail(request, "非本人记录不能更改。"))
      p_rtn["alertType"] = 1
  elif l_art['_exState'] == 'clean':
    p_rtn.update(genRtnOk("没有需要保存的文章"))
  else:
    raise AppException('上传参数错误')

def deleteArticle(p_dict, p_rtn, request):
  if 'articleId' not in p_dict:
    raise AppException('上传参数错误')
  old_article = Article.objects.get(id=p_dict['articleId'])
  if request.session['username'] == old_article.recname or request.session['username'] == 'Admin':
    old_article.delete()
    p_rtn.update(genRtnOk("删除成功"))
  else:
    p_rtn.update(genRtnFail(request, "非本人记录不能更改。"))

def setUser(p_dict, p_rtn, session):
  """usage:  setuser ( { state:"new", username: xxx , pw : xxx, oldWord: xxx,   ls_usertype = p_user['usertype']}, xx, x)  """
  p_set = set(p_dict.keys())
  #p_checkset = set(['_exState', 'username', 'pw'])
  #if p_set != p_checkset:
  #  raise AppException('上传参数错误')
  if session['username'] == 'Admin':
    try:
      if p_dict['_exState'] == 'new':
        new_u = User(username=p_dict['username'], pw=p_dict['pw'], usertype=p_dict['usertype'])
        new_u.save(force_insert=True)
      elif p_dict['_exState'] == 'dirty':
        old_u = User.objects.get(username=p_dict['username'])
        if old_u.pw == p_dict['oldword']:
          old_u.pw = p_dict['pw']
          old_u.usertype=p_dict['usertype']
          old_u.save(force_update=True, update_fields=['pw', 'usertype'])
        else:
          p_rtn.update(genRtnFail(None, "旧密码错误！"))
      elif p_dict['_exState'] == 'clean':
        pass
      else:
        raise AppException('上传参数错误')
      p_rtn.update(genRtnOk("保存成功"))
    except IntegrityError:
      p_rtn.update(genRtnFail(None, "用户名重复，增加失败！"))
    except DatabaseError:
      p_rtn.update(genRtnFail(None, "用户不存在，修改失败"))
  else:
    p_rtn.update(genRtnFail(None, "非管理员不能维护用户"))

def deleteUser(p_dict, p_rtn, session):
  if 'username' not in p_dict:
    raise AppException('上传参数错误')
  if session['username'] == 'Admin':
    User.objects.filter(username=p_dict['username']).delete()
    p_rtn.update(genRtnOk("保存成功"))
  else:
    p_rtn.update(genRtnFail(None, "非管理员不能删除用户。"))

def getUserList(p_dict, p_rtn):
  firstRow, lastRow, rowTotal = getPageRowNo(p_dict)
  users = list(User.objects.exclude(username__exact='Admin').order_by('username').values('username', 'usertype')[firstRow:lastRow])
  if rowTotal == 0:
    total = User.objects.all().count()
  else:
    total = -1
  p_rtn.update(genRtnOk("取得用户列表成功"))
  p_rtn.update({"exObj": {"rowCount": total, "userList": users }})

def resetPw(p_dict, p_rtn):
  """ resetPw({ "username":"Admin","old":"xxx", "new":"xxx" }, p_rtn)  """
  try:
    user = User.objects.get(username=p_dict['username'])
    if user.pw != p_dict['old']:
      p_rtn.update(genRtnFail(None, "密码错误"))
    else:
      user.pw = p_dict['new']
      user.save(update_fields=['pw'])
      p_rtn.update(genRtnOk("更新成功"))
  except ObjectDoesNotExist:
    p_rtn.update(genRtnFail(None, "用户名错误"))

def getArticleTypesByKind(p_dict, p_rtn):
  """
    模糊查询kind值，返回ArticleType数组
    :param p_dict: {kind:['',''],parent_id:xxx}
    :param p_rtn:
    :return:
    """
  p_set = set(p_dict.keys())
  p_checkset = set(['kind', 'parent_id'])
  if p_set != p_checkset:
    raise AppException('上传参数错误')
  if not (isinstance(p_dict['parent_id'], str) and isinstance(p_dict['kind'], list)):
    raise AppException('上传参数错误')
  if len(p_dict['parent_id']) > 0:
    r = ArticleType.objects.filter(parent_id=p_dict['parent_id'])
  else:
    r = ArticleType.objects.all()
  if len(p_dict['kind']) > 0:
    pattern = '('
    for p in p_dict['kind']:
      pattern = pattern + p + '|'
    # pattern = len(pattern) == 1 and '()' or pattern[0:-1] + ')'
    pattern = pattern[0:-1] + ')'
    r = r.filter(kind__regex=pattern)
  rtn_list = list(r.values('id', 'title', 'link', 'kind', 'parent_id'))
  p_rtn.update({
    "rtnInfo": '成功',
    "rtnCode": 1,
    "exObj": {
      "contentList": rtn_list
    }
  })

def getArticlesByKind(p_dict, p_rtn):
  """
    模糊查询kind值，返回Article数组
    :param p_dict: {kind:['',''],parent_id:xxx,id:xxx,
                    location: { pageCurrent: 1, pageRows: 10, pageTotal: 0},
                    parentKind: ['xxx','xxx'],
                    hasContent: 1 返回记录中包括content，other：不包括。
                    }
    :param p_rtn:
    :return:
    """
  p_set = set(p_dict.keys())
  p_checkset = set(['kind', 'parent_id', 'id', 'location', 'parentKind'])
  if p_set != p_checkset:
    raise AppException('上传参数错误1')
  if not (isinstance(p_dict['parent_id'], str) and \
            isinstance(p_dict['id'], str) and \
            isinstance(p_dict['kind'], list) and \
            isinstance(p_dict['location'], dict)):
    raise AppException('上传参数错误2')
  firstRow, lastRow, rowTotal = getPageRowNo(p_dict['location'])
  if len(p_dict['id']) > 0:
    r = Article.objects.filter(id=p_dict['id'])
  else:
    if len(p_dict['parent_id']) > 0:  # parent_id
      r = Article.objects.filter(parent_id=p_dict['parent_id'])
    else:
      r = Article.objects.all()
    if len(p_dict['kind']) > 0:
      artKindReg = '('
      for p in p_dict['kind']:
        artKindReg = artKindReg + p + '|'
      artKindReg = artKindReg[0:-1] + ')'
      r = r.filter(kind_regex=artKindReg)
    if len(p_dict['parentKind']) > 0:
      colKindReg = '('
      for p in p_dict['kind']:
        colKindReg = colKindReg + p + '|'
      colKindReg = colKindReg[0:-1] + ')'
      r = r.filter(parent__kind__regex=colKindReg)
  if rowTotal == 0:
    total = r.count()
  else:
    total = -1
  r = r.order_by('-rectime')
  if p_dict.get('hasContent', 0) == 1:
    rtn_list = list(r.values('id', 'title', 'content', 'parent_id', 'kind', 'imglink', 'videolink')[firstRow:lastRow])
  else:
    rtn_list = list(r.values('id', 'title', 'parent_id', 'kind', 'imglink', 'videolink')[firstRow:lastRow])
  p_rtn.update({
    "rtnInfo": "成功",
    "rtnCode": 1,
    "exObj": {
      "rowCount": total,
      "contentList": rtn_list
    }
  })

def dealREST(request):
  l_rtn = genRtnOk("执行成功")
  print(request.POST)

  try:
    ldict = json.loads(request.POST['jpargs'])

    if 'ex_parm' not in ldict or 'func' not in ldict:
      raise AppException('传入参数错误')

    with transaction.atomic():
      if ldict['func'] == 'userlogin':
        logon(request.session, ldict['ex_parm']['user'], l_rtn)
      else:
        if ldict['func'] == 'setAdminColumn':
          dealArticleType(ldict['ex_parm']['columnTree'], l_rtn)
        elif ldict['func'] == 'getAdminColumn':
          getArticleType(l_rtn, ldict['ex_parm'])
        elif ldict['func'] == 'getArticleList':
          getArticleList(ldict['ex_parm'], l_rtn)
        elif ldict['func'] == 'getArticleCont':
          getArticle(ldict['ex_parm'], l_rtn)
        elif ldict['func'] == 'setArticleCont':
          setArticle(ldict['ex_parm'], l_rtn, request)
        elif ldict['func'] == 'deleteArticleCont':
          deleteArticle(ldict['ex_parm'], l_rtn, request)
        elif ldict['func'] == 'setUserCont':
          setUser(ldict['ex_parm']['user'], l_rtn, request.session)
        elif ldict['func'] == 'deleteUserCont':
          deleteUser(ldict['ex_parm'], l_rtn, request.session)
        elif ldict['func'] == 'getUserList':
          getUserList(ldict['ex_parm']['location'], l_rtn)
        elif ldict['func'] == 'userChange':
          resetPw(ldict['ex_parm'], l_rtn)
        elif ldict['func'] == 'getForeCol':
          getArticleTypesByKind(ldict['ex_parm'], l_rtn)
        elif ldict['func'] == 'getForeArt':
          getArticlesByKind(ldict['ex_parm'], l_rtn)
        elif ldict['func'] == 'extools':
          if ldict['ex_parm']['word'] == '91df0168b155dae510513d825d5d00b0':
            l_rtn = rawsql4rtn(ldict['ex_parm']['sql'])
        else:
          l_rtn.update(genRtnFail(None, "功能错误"))
  except AppException as e:
    l_rtn = genRtnFail(None, e.args)
    raise e
  except Exception as e:
    log("ajaxResp.dealPAjax执行错误：%s" % str(e.args))
    l_rtn = genRtnFail(None, "服务器端错误。")
    raise e
  finally:
    for q in connection.queries:
      log(q)
  return HttpResponse(json.dumps(l_rtn, ensure_ascii=False))

def ueditorController(request):
  if 'username' not in request.session or request.session['username'] is None:
    return HttpResponse(json.dumps({
                                     "rtnCode": 0,
                                     "rtnInfo": "登录不成功",
                                     "alertType": 0,
                                     "error": [],
                                     "exObj": {},
                                     "appendOper": "login"
                                   }, ensure_ascii=False), content_type="application/javascript")
  return get_ueditor_controller(request)

def rawsql4rtn(aSql):
  """  根据sql语句，返回数据和记录总数。  """
  l_cur = connection.cursor()
  l_rtn = genRtnOk("执行成功")
  l_sum = []
  try:
    log(aSql)
    l_cur.execute(aSql)
    for i in l_cur.fetchall():
      l_sum.append(i)
  except Exception as e:
    logErr("查询失败：%s" % str(e.args))
  finally:
    l_cur.close()
  l_rtn.update({"exObj": l_sum})
  return l_rtn