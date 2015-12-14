from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import FictionSerializer, EpisodeSummarySerializer, EpisodeFullSerializer
from main.models import Fiction, Episode

class FictionList(APIView):
    """
    List all fictions
    """
    def get(self, request, format=None):
        fictions = Fiction.objects.all()
        serializer = FictionSerializer(fictions, many=True)
        return Response(serializer.data)

class EpisodeList(APIView):
    """
    List all episodes of a Fiction
    """
    def get(self, request, fiction_id, format=None):
        fiction = Fiction.objects.get(id=fiction_id)
        episodes = Episode.objects.filter(fiction=fiction).all();
        serializer = EpisodeSummarySerializer(episodes, many=True)
        return Response(serializer.data)

class EpisodeSummary(APIView):
    """
    List summary view of a Episode
    """
    def get(self, request, episode_id, format=None):
        episode = Episode.objects.get(id=episode_id)
        serializer = EpisodeSummarySerializer(episode)
        return Response(serializer.data)

class EpisodeFull(APIView):
    """
    List ful view of a Episode
    """
    def get(self, request, episode_id, format=None):
        episode = Episode.objects.get(id=episode_id)
        serializer = EpisodeFullSerializer(episode)
        return Response(serializer.data)