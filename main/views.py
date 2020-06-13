from django.shortcuts import render
from django.views import View
from rest_framework import views
from rest_framework.response import Response
from datetime import date, timedelta
from directions.models import Trend
from api.views import objectMain
from .serializers import *

# from base.settings import REACT_USE
# Create your views here.
class MainCommonViewSet(views.APIView):
    def get(self, request, REACT_USE=True):
        ObjectMain = objectMain(
            main=Main.objects.first(),
            menu=Menu.objects.all(),
            partners=Partner.objects.all(),
            social=SocialNet.objects.first(),
            contacts=Contact.objects.first(),
            massMedia=Contact.objects.last(),
        )
        serializerCommon = CommonSerializer(ObjectMain)
        serializerCommon.data.get("menu")[4].update({"path": "/direction/" + str(Trend.objects.first().id) +"/about"})
        commonData = serializerCommon.data
        from image_cropping.utils import get_backend
        for partner in commonData.get("partners"):
            ID = partner.get("id")
            obj = Partner.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (50, 50),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            partner['image'] = image
        if not REACT_USE:
            return serializerCommon.data
        return Response(serializerCommon.data)

