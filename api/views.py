from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from datetime import date, timedelta
from collections import namedtuple

from federation.models import FederationElement
from events.models import Event
from directions.models import Trend, Direction
# Create your views here.

objectMain = namedtuple('common', ('main', 'menu', 'social', 'partners', 'contacts', 'massMedia'))
objectNews = namedtuple('main_news', ('main', 'important'))
objectMedia = namedtuple('media', ('photos', 'videos', 'urlphotos', 'urlvideos'))

from tournaments.models import *

@api_view(['GET'])
def time_test(request, format=None):
    a = Game.objects.get(id=490000)
    return Response({
        'Main Page': str(a.id)
    })
@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        # 'Main Page': {
        #     'Footer & Header': reverse('common-fh-list', request=request),
        #     'Block News': reverse('common-news-list', request=request),
        #     'Block Media': reverse('common-media-list', request=request),
        #     'Block Events': reverse('common-events-list', request=request),
        #     'Block Trends': reverse('common-trends-list', request=request),
        #
        # },
        # 'Events': {
        #     'Active': {
        #         'List': reverse('events-active-list', request=request, args=[0]),
        #         'Filter-Direction': reverse('events-active-list', request=request, args=[0]) + "?direction=1",
        #         'Filter-Time': reverse('events-active-list', request=request,
        #                                args=[0]) + "?from=10.4.2020&to=3.10.2020",
        #     },
        #     'Completed': {
        #         'List': reverse('events-completed-list', request=request, args=[0]),
        #         'Filter-Direction': reverse('events-completed-list', request=request, args=[0]) + "?direction=1",
        #         'Filter-Time': reverse('events-completed-list', request=request,
        #                                args=[0]) + "?from=10.4.2020&to=3.10.2020",
        #     },
        #     'All': {
        #         'List': reverse('events-all-list', request=request, args=[0]),
        #         'Filter-Direction': reverse('events-all-list', request=request, args=[0]) + "?direction=1",
        #         'Filter-Time': reverse('events-all-list', request=request,
        #                                args=[0]) + "?from=10.4.2020&to=3.10.2020",
        #     },
        #     'Detail': reverse('events-detail', request=request, args=[Event.objects.first().id]),
        # },
        # 'News': {
        #     'List': reverse('news-list', request=request, args=[0]),
        #     'Filter-Direction': reverse('news-list', request=request, args=[0]) + "?direction=" + str(Direction.objects.first().id),
        #     'Detail': reverse('news-detail', request=request, args=[1]),
        #     'Filter-Time': reverse('news-list', request=request, args=[0]) + "?from=10.4.2020&to=03.05.2020",
        # },
        # 'Federation': {
        #     'Page': reverse('federation-page', request=request),
        # },
        'Search': reverse('search', request=request, args=[0]),
        # 'Trends': {
        #     'List': reverse('common-trends-list', request=request),
        #     'Detail': reverse('trend-detail', request=request, args=[Trend.objects.first().id]),
        #     'News': reverse('trend-detail-news', request=request, args=[Direction.objects.first().id, 0]),
        #     'Opportunities': reverse('trend-detail-events', request=request, args=[Direction.objects.first().id, 0]),
        # },
    })