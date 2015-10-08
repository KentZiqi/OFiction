from django.conf.urls import patterns, url
from main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ColaFiction.views.home', name='home'),
    url(r'^$', home, name='home'),
    url(r'^notifications/$', notifications, name='notifications'),
    url(r'^episode/$', episode, name='episode'),
    url(r'^explore/$', explore, name='explore'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^storyline/$', storyline, name='storyline'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^sign_in/$', sign_in, name='sign_in'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^welcome/$', welcome, name='welcome')
)
