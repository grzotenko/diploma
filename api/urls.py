from django.conf.urls import url, include
from django.urls import path

from .views import api_root
from main.views import MainCommonViewSet
from news.views import BlockNewsViewSetAPI, AllNewsViewSet, NewsDetail
urlpatterns = [
    url(r'^$', api_root),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('common/', MainCommonViewSet.as_view(), name='common-fh-list'),
    path('common/news/', BlockNewsViewSetAPI.as_view(), name='common-news-list'),
    path('news/detail/<int:pk>', NewsDetail.as_view(), name='news-detail'),
    path('news/list/<int:page>', AllNewsViewSet.as_view(), name='news-list'),
]
