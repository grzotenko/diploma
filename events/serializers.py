from rest_framework import serializers
from .models import *
from directions.serializers import DirectionSerializer

class EventBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'address', 'map']

class EventSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'directions', 'text', 'address', 'map']

class EventNextPrevSimilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title']


