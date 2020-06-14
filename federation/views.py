from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import views
from api.views import objectMedia

from .serializers import *
# Create your views here.
class FederationPage(views.APIView):
    def get(self, request):
        serializerFederation = FederationSerializer(Federation.objects.first())
        dataFederation = serializerFederation.data
        return Response(dataFederation)

