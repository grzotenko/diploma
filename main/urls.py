from django.conf.urls import url, include
from django.urls import path

from .controller import MainPage, MainPageReact
from base.settings import REACT_USE

if REACT_USE:
    urlpatterns = [
        path('', MainPageReact.as_view(), name="main_main"),
    ]
else:
    urlpatterns = [
        path('', MainPage.as_view(), name="main_main"),
    ]