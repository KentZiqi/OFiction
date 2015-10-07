from django.conf.urls import patterns, url
from main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ColaFiction.views.home', name='home'),
    url(r'^$', home, name='home'),
    url(r'^notifications/$', notifications, name='notifications'),
    url(r'^work/$', work, name='work'),
    url(r'^explore/$', explore, name='explore'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^storyline/$', storyline, name='storyline'),
    url(r'^settings/$', settings, name='settings')
)
