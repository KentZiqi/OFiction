from rest_framework import serializers
from main.models import Fiction, Profile, Episode

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'display_name')

class FictionSerializer(serializers.ModelSerializer):
    starters = ProfileSerializer(many=True)

    class Meta:
        model = Fiction
        fields = ('id', 'title', 'starters', 'created_date')

class EpisodeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'author', 'summary', 'popularity', 'created_date')

class EpisodeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'author', 'summary', 'popularity', 'created_date', 'content')