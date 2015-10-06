from django.conf.urls import patterns, url
from main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ColaFiction.views.home', name='home'),
    url(r'^$', home),
)
