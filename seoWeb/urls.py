from django.conf.urls import patterns, include, url
#from django.contrib import admin
from App import views
from App import viewsFore
#from App.ueditor.views import get_ueditor_controller
from App.views import ueditorController
urlpatterns = patterns('',

  url(r'^$', 'App.viewsFore.home', name='home'),
  url(r'^App/1/', views.test1,name='test1'),
  url(r'^notstatic/js/ueditor/controller', ueditorController,name='ueditor'),
  url(r'^rest/$',views.dealREST,name='rest'),

  url(r'^(?P<goolArg>\w+)/$', viewsFore.gool, name='gool'),
  url(r'^(?P<goolArg>\w+)/(?P<goolSecArg>\w+)/$', viewsFore.gool, name='goolsub'),


)
