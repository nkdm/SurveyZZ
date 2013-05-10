from django.conf.urls import patterns, url
from django.contrib.auth.views import login,logout
from surveys import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>\d+)/results$', views.results),
    url(r'^login/?$', login),
    url(r'^admin/?$', views.admin),
    url(r'^logout/?$', logout,{ 'template_name':'registration/logout.html'} ),
    url(r'^questionnaires/?$', views.questionnaires),
    url(r'^questionnaires/(?P<id>\d+)/?$', views.questionnaire)
)
