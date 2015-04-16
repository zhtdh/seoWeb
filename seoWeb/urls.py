from django.conf.urls import patterns, include, url
from App import views, viewsFore, viewsMb

urlpatterns = patterns('',
  url(r'^$', 'App.viewsFore.home', name='home'),
  url(r'^App/1/', views.test1,name='test1'),
  url(r'^notstatic/js/ueditor/controller', views.ueditorController,name='ueditor'),
  url(r'^rest/$',views.dealREST,name='rest'),

  url(r'^mbjp/$',viewsMb.getJsonp,name='mbjp'),

  url(r'^(?P<goolArg>\w+)/$', viewsFore.gool, name='gool'),  # 顺序很重要，放到最后。
  url(r'^(?P<goolArg>\w+)/(?P<goolSecArg>\w+)/$', viewsFore.gool, name='goolsub'),


)

