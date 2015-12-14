from django.conf.urls import url
from api.views import FictionList, EpisodeList, EpisodeSummary, EpisodeFull

urlpatterns = [
    url(r'^$', FictionList.as_view(), name="fictions"),
    url(r'fiction/(?P<fiction_id>[^/]+)/?$', EpisodeList.as_view(), name="episodes"),
    url(r'episode/(?P<episode_id>[^/]+)/summary/?$', EpisodeSummary.as_view(), name="episode_summary"),
    url(r'episode/(?P<episode_id>[^/]+)/full/?$', EpisodeFull.as_view(), name="episodes_full"),
]