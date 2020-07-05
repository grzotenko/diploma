from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from .models import *
from .views import MainCommonViewSet
from templates.controller import getHeaderViews

class MainPage(View):
    initial = {'key': 'value'}
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        context = MainCommonViewSet.get(MainCommonViewSet, request, False)

        return render(request, self.template_name, context)

class MainPageReact(View):
    template_name = 'index.html'
    def get(self, *args, **kwargs):#, *args, **kwargs):
        context = dict()
        return render(args[0], self.template_name, context)
