from django.conf.urls import patterns, include, url
from django.contrib import admin
from App import views
from App import viewsFore
from App import dhcache
from App.ueditor.views import get_ueditor_controller
urlpatterns = patterns('',

  url(r'^$', 'App.viewsFore.home', name='home'),
  url(r'^(?P<goolArg>\w+)/$', dhcache.gool, name='gool'),
  url(r'^(?P<goolArg>\w+)/(?P<goolSecArg>\w+)/$', dhcache.gool, name='goolsub'),


  url(r'^admin/', include(admin.site.urls)),
  url(r'^App/1/', views.test1,name='test1'),
  url(r'^notstatic/js/ueditor/controller', get_ueditor_controller,name='ueditor'),
  #url(r'^ajax/',views.dealPAjax,name='ajax'),
  url(r'^rest/$',views.dealREST,name='rest'),
)
