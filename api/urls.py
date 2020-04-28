from django.conf.urls import url, include
from django.urls import path

from .views import api_root, time_test
from main.views import MainCommonViewSet
from news.views import BlockNewsViewSetAPI, AllNewsViewSet, NewsDetail
from federation.views import BlockFederationViewSetAPI, FederationElemDetail
from events.views import BlockEventsViewSetAPI, EventDetail,EventsAllViewSet, EventsActiveViewSet, EventsCompletedViewSet
from mediafiles.views import BlockMediaViewSetAPI
urlpatterns = [
    url(r'^$', api_root),
    path('timetest', time_test, name='time-test'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('common/', MainCommonViewSet.as_view(), name='common-fh-list'),
    path('common/news/', BlockNewsViewSetAPI.as_view(), name='common-news-list'),
    path('common/federation/', BlockFederationViewSetAPI.as_view(), name='common-federation-list'),
    path('common/media/', BlockMediaViewSetAPI.as_view(), name='common-media-list'),
    path('common/events/', BlockEventsViewSetAPI.as_view(), name='common-events-list'),
    path('news/detail/<int:pk>', NewsDetail.as_view(), name='news-detail'),
    path('news/list/<int:page>', AllNewsViewSet.as_view(), name='news-list'),
    path('federation/detail/<int:pk>', FederationElemDetail.as_view(), name='federation-detail'),
    path('events/all/list/<int:page>', EventsAllViewSet.as_view(), name='events-all-list'),
    path('events/active/list/<int:page>', EventsActiveViewSet.as_view(), name='events-active-list'),
    path('events/completed/list/<int:page>', EventsCompletedViewSet.as_view(), name='events-completed-list'),
    path('events/detail/<int:pk>', EventDetail.as_view(), name='events-detail'),
]
