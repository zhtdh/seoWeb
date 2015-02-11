__author__ = 'blaczom'
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.http import *

from App.viewsFore import getCorpInfo,getContact
from App.utils import log
@require_http_methods(["GET"])
def gool(request, goolArg="", goolSecArg=""):
    try:
        if goolArg == "resec":
            corpInfo = getCorpInfo()
            return render(request, "rendSec.html",locals())
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
