from django.conf.urls import patterns, url

from surveys import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>\d+)$', views.presentSurvey),                     
    url(r'^(?P<id>\d+)/results$', views.results),
    url(r'^(?P<id>\d+)$', views.presentSurvey)
)
