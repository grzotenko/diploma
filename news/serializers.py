from rest_framework import serializers

from directions.serializers import DirectionSerializer

from .models import *

class NewsPartBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'date']

class NewsBlocksSerializer(serializers.Serializer):
    main = NewsPartBlockSerializer(many=True)
    important = NewsPartBlockSerializer(many=True)

class AllNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'preview', 'date']

class NewsNextPrevSimilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title']

class NewsSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True)
    class Meta:
        model = News
        fields = ['id', 'title', 'date', 'directions', ]