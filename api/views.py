from django.http import Http404
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
    def get_object(self, fiction_id):
        try:
            return Fiction.objects.get(id=fiction_id)
        except Fiction.DoesNotExist:
            raise Http404

    def get(self, request, fiction_id, format=None):
        fiction = self.get_object(fiction_id)
        episodes = Episode.objects.filter(fiction=fiction).all()
        serializer = EpisodeSummarySerializer(episodes, many=True)
        return Response(serializer.data)

class EpisodeSummary(APIView):
    """
    List summary view of a Episode
    """
    def get_object(self, episode_id):
        try:
            return Episode.objects.get(id=episode_id)
        except Episode.DoesNotExist:
            raise Http404

    def get(self, request, episode_id, format=None):
        episode = self.get_object(episode_id)
        serializer = EpisodeSummarySerializer(episode)
        return Response(serializer.data)

class EpisodeFull(APIView):
    """
    List ful view of a Episode
    """
    def get_object(self, episode_id):
        try:
            return Episode.objects.get(id=episode_id)
        except Episode.DoesNotExist:
            raise Http404

    def get(self, request, episode_id, format=None):
        episode = self.get_object(episode_id)
        serializer = EpisodeFullSerializer(episode)
        return Response(serializer.data)