from rest_framework import serializers
from main.models import Fiction, Profile, Episode

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'display_name')

class FictionSerializer(serializers.ModelSerializer):
    starter = ProfileSerializer()

    class Meta:
        model = Fiction
        fields = ('id', 'title', 'starter', 'created_date')

class EpisodeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'author', 'summary', 'popularity', 'created_date', 'sentiment', 'previous_ids_without_parent', 'next_ids_without_parent')

class EpisodeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'author', 'summary', 'popularity', 'created_date', 'content')