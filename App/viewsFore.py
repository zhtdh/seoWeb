__author__ = 'blaczom'
from django.shortcuts import render,HttpResponse
from App.models import Article

def home(request):
    return render(request, "home.html")
def getCorpInfo():
    try:
        return Article.objects.filter(parent_id='0')\
            .filter(kind__icontains='corpinfo').values('content')[0]['content']
    except IndexError:
        return "无简介"
def getContact():
    try:
        return Article.objects.filter(parent_id='0')\
            .filter(kind__icontains='topContact').values('content')[0]['content']
    except IndexError:
        return "无联系方式"