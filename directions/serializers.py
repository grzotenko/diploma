from rest_framework import serializers
from .models import *
class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['id', 'title',]

class TrendsDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendsDocuments
        fields = ['id', 'title','file']


class TrendDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['id', 'title', 'text','imageActive','imageInactive',]

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'title',]
