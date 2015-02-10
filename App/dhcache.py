__author__ = 'blaczom'
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect

def gool(request, goolArg="", goolSecArg=""):
  if goolArg == "resec" :
    return render(request, "rendSec.html")
  elif goolArg == "rethi" :
    return render(request, "rendThi.html")
  elif goolArg == "refou" :
    return render(request, "rendFou.html")
  elif goolArg == "refiv" :
    return render(request, "rendFiv.html", locals())
  elif goolArg == "recon" :
    return render(request, "rendCon.html")
  else:
    return HttpResponseRedirect("/")

