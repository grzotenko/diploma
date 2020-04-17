from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from datetime import date, timedelta
from collections import namedtuple

from directions.models import Direction
# Create your views here.

objectMain = namedtuple('common', ('main', 'menu', 'social', 'partners', 'contacts', 'massMedia'))
objectNews = namedtuple('main_news', ('main', 'important'))

@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        'Main Page': {
            'Footer & Header': reverse('common-fh-list', request=request),
            'Block News': reverse('common-news-list', request=request),
        },
        'News': {
            'List': reverse('news-list', request=request, args=[0]),
            'Filter-Direction': reverse('news-list', request=request, args=[0]) + "?direction=" + str(Direction.objects.first().id),
            'Detail': reverse('news-detail', request=request, args=[1]),
            'Filter-Time': reverse('news-list', request=request, args=[0]) + "?from=10.04.2020&to=03.05.2020",
        },
    })