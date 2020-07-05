from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from datetime import date, timedelta, datetime
from news.serializers import *
from events.serializers import *
from .serializers import *

class AllTrends(views.APIView):
    def get(self, request):
        serializerTrends = TrendSerializer(Trend.objects.all(), many=True)
        return Response(serializerTrends.data)

class TrendDetail(views.APIView):
    def get(self, request, pk):
        id = int(pk)
        trend = get_object_or_404(Trend, id=id)
        serializerTrend = TrendDetailSerializer(trend).data
        serializerTrend["directions"] = DirectionSerializer(Direction.objects.filter(id_fk=trend), many=True).data
        serializerTrend["documents"] = TrendsDocumentsSerializer(TrendsDocuments.objects.filter(id_fk=trend), many=True).data
        return Response(serializerTrend)

class TrendDetailNews(views.APIView):
    def get(self, request, pk, page):
        id = int(pk)
        offset = int(page)
        trend = get_object_or_404(Trend, id=id)
        news = News.objects.filter(directions__id_fk = trend).distinct()[offset:offset+6]
        serializerDirectionNews = NewsPartBlockSerializer(news, many=True)
        dataDirectionNews = serializerDirectionNews.data
        from image_cropping.utils import get_backend
        for news in dataDirectionNews:
            ID = news.get("id")
            obj = News.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (300, 300),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            news['image'] = image
        return Response(dataDirectionNews)

class TrendDetailEvents(views.APIView):
    def get(self, request, pk, page):
        id = int(pk)
        offset = int(page)
        trend = get_object_or_404(Trend, id=id)
        events = Event.objects.filter(directions__id_fk = trend).distinct()[offset:offset+6]
        serializerDirectionEvents = EventBlockSerializer(events, many=True)
        dataDirectionEvents = serializerDirectionEvents.data
        from image_cropping.utils import get_backend
        for event in dataDirectionEvents:
            ID = event.get("id")
            obj = Event.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (390, 280),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            event['image'] = image
        return Response(dataDirectionEvents)