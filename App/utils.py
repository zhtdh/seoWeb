__author__ = 'donghai'

import os
from datetime import datetime,date
from seoWeb.settings import BASE_DIR, DEBUG
import sys
import json
from decimal import Decimal

class ServerToClientJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj,Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self,obj)

class AppException(Exception):
    pass

def log(aMsg, alogFile = BASE_DIR + 'djgw.log'):
    '''
        记录日志： from zdCommon.utils import log, logErr
    @param aMsg: 记录的信息
    @param alogFile:  记录的文件名，默认djgw.log
    '''
    if DEBUG:
        lMsg = datetime.now().strftime('%m-%d %H:%M:%S -> ') + sys._getframe(1).f_code.co_name + ' -> ' + str(aMsg)
        print(lMsg + str(type(aMsg)))
        #a = open(alogFile, 'a+')
        #a.write(lMsg+os.linesep)
        #a.close()
    # if os.path.exists(alogFile): raise Exception("our system log file does not exist") 直接写。

def logErr(aMsg, alogFile = BASE_DIR + 'err.log'):
    lMsg = datetime.now().strftime('Err: %y-%m-%d %H:%M:%S from: ') + sys._getframe(1).f_code.co_name + " " + str(aMsg)
    print(lMsg)  #控制台打印error
    #a = open(alogFile, 'a+')
    #a.write(lMsg + os.linesep)
    #a.close()
    # if os.path.exists(alogFile): raise Exception("our system log file does not exist") 直接写。

# push a Err msg into sessions . and return to client. usage: logErrReq(request, 'err msg') :  l_rtn = genRtnFail(request, "消息处理过程错误")
def logErrReq(aReq, aMsg):
  aReq.session["lastErr"].append(aMsg)
  logErr(aMsg)


def genRtn(aCode=1, aInfo="", aAlert=0, aErr=[], aObj={}):
  return {"rtnCode":aCode, "rtnInfo":aInfo, "alertType":aAlert, "error":aErr, "exObj":aObj}

def genRtnOk(aInfo):
  return {"rtnCode":1, "rtnInfo":aInfo, "alertType":0, "error":[], "exObj":{}}

def genRtnFail(aReq, aInfo, aAlert=0):
  if aReq:
    return {"rtnCode":-1, "rtnInfo":aInfo, "alertType":0, "error":aReq.session["lastErr"]}
  else:
    return {"rtnCode":-1, "rtnInfo":aInfo, "alertType":0, "error":["未知错误"]}



from App.models import ArticleType,Article

g_type_fields = ArticleType._meta.get_all_field_names()
g_type_fields.remove('fk_article')
g_type_fields.remove('parent')
g_type_fields.remove('subarticletype')

g_article_fields = Article._meta.get_all_field_names()
g_article_fields.remove('parent')

g_auto_fields = ('recname, rectime, updtime')

'''
目的：dump任何对象到文件中保存起来。可以load出来。
使用方法：
>>> import zdCommon.utils
>>> dump2file('sdfs', 'aa.txt')
>>> b = load4file('aa.txt')
'''

from pickle import dump, load, dumps
def dump2file(aobj, afilename):
    ls_file = BASE_DIR + afilename
    a = open(ls_file, 'wb')
    dump(aobj, a)
    a.close()

def load4file(afilename):
    ls_file = BASE_DIR + afilename
    a = open(ls_file, 'rb')
    l_obj = load(a)
    a.close()
    return(l_obj)
