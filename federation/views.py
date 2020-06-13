from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import views
from api.views import objectMedia

from .serializers import *
# Create your views here.
class BlockFederationViewSetAPI(views.APIView):
    def get(self, request):
        serializerFederationElements = FederationBlockSerializer(FederationElement.objects.all(), many=True)
        dataFederationElements = serializerFederationElements.data
        from image_cropping.utils import get_backend
        for elem in dataFederationElements:
            ID = elem.get("id")
            obj = FederationElement.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (320, 300),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            elem['image'] = image
        return Response(dataFederationElements)

class FederationPage(views.APIView):
    def get(self, request):
        serializerFederation = FederationSerializer(Federation.objects.first())
        dataFederation = serializerFederation.data
        # from image_cropping.utils import get_backend
        # for elem in dataFederation["federationelement_set"]:
        #     for staff in elem["federationstaff_set"]:
        #         ID = staff.get("id")
        #         obj = FederationStaff.objects.get(id=ID)
        #         image = get_backend().get_thumbnail_url(
        #             obj.imageOld,
        #             {
        #                 'size': (320, 300),
        #                 'box': obj.image,
        #                 'crop': True,
        #                 'detail': True,
        #             }
        #         )
        #         staff['image'] = image
        return Response(dataFederation)

class FederationElemDetail(views.APIView):
    def get(self, request, pk):
        id = int(pk)
        element = get_object_or_404(FederationElement, id=id)
        serializerFederationElement = FederationBlockSerializer(element)
        dataFederationElement = serializerFederationElement.data
        from image_cropping.utils import get_backend
        image = get_backend().get_thumbnail_url(
            element.imageOld,
            {
                'size': (320, 300),
                'box': element.image,
                'crop': True,
                'detail': True,
            }
        )
        dataFederationElement['image'] = image
        staffs = FederationStaff.objects.filter(id_fk=element)
        serializerFederationStaff = FederationStaffSerializer(staffs, many=True)
        dataFederationStaff = serializerFederationStaff.data
        for staff in dataFederationStaff:
            ID = staff.get("id")
            obj = FederationStaff.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (320, 300),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            staff['image'] = image
        dataFederationElement["staff"] = dataFederationStaff
        return Response(dataFederationElement)
