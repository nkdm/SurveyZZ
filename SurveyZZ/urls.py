from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()
admin.site.login = login_required(admin.site.login)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SurveyZZ.views.home', name='home'),
    # url(r'^SurveyZZ/', include('SurveyZZ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin-django/?', include(admin.site.urls)),
    url(r'^(surveys/)?', include('surveys.urls')),
)
