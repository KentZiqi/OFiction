from django.conf.urls import patterns, url
from main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ColaFiction.views.home', name='home'),
    url(r'^$', home, name='home'),
    url(r'^notifications/$', notifications, name='notifications'),

    url(r'^episode/(?P<episode_id>\d+)/$', episode, name='episode'),
    url(r'^episode/new/(?P<fiction_id>\d+)/(?P<parent_id>\d+)/$',episode_create, name='episode_create'),
    url(r'^episode/(?P<episode_id>\d+)/edit/$',episode_edit, name='episode_edit'),

    url(r'^explore/$', explore, name='explore'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^storyline/$', storyline, name='storyline'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^sign_in/$', sign_in, name='sign_in'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^welcome/$', welcome, name='welcome'),

    url(r'^fiction/new/$', FictionCreate.as_view(), name='create_fiction'),

    url(r'^comment/(?P<episode_id>\d+)/', comment_create, name="comment_create"),
    url(r'^star/(?P<episode_id>\d+)/', star, name="star")
)
