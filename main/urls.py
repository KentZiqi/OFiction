from django.conf.urls import patterns, url
from main.views import *
from main.account_views import *
from main.profile_views import *

urlpatterns = patterns('',
                       url(r'^login/?$', LoginView.as_view(), name='login'),
                       url(r'^logout/?$', logout, name='logout'),
                       url(r'^sign_up/?$', RegistrationView.as_view(), name='sign_up'),

                       url(r'^$', home, name='home'),

                       url(r'^notifications/?$', notifications, name='notifications'),

                       url(r'^episode/(?P<episode_id>\d+)/?$', episode, name='episode'),
                       url(r'^episode/new/(?P<fiction_id>\d+)/(?P<parent_id>\d+)/?$', episode_create,
                           name='episode_create'),
                       url(r'^episode/(?P<episode_id>\d+)/edit/?$', episode_edit, name='episode_edit'),

                       url(r'^explore/?$', explore, name='explore'),

                       url(r'^fiction/(?P<fiction_id>\d+)/?$', fiction, name='fiction'),
                       url(r'^fiction/new/?$', FictionCreate.as_view(), name='create_fiction'),

                       url(r'^storyline/(?P<episode_id>\d+)/?$', storyline, name='storyline'),

                       url(r'^pdf/(?P<pdf_name>.+)/?$', pdf, name='pdf'),

                       url(r'^comment/(?P<episode_id>\d+)/?', comment_create, name="comment_create"),
                       url(r'^star/(?P<episode_id>\d+)/?', star, name="star"),


                       url(r'^profile/?$', profile_required(profile), name='profile'),
                       url(r'^profile/edit/?$', profile_required(ProfileEditView.as_view()), name='edit_profile'),

                       url(r'^settings/?$', settings, name='settings'),
)
