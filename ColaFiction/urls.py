from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ColaFiction.views.home', name='home'),
    url(r'^main/', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
