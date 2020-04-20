from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views
from api.views import objectMedia

from .serializers import *
# Create your views here.
class BlockMediaViewSetAPI(views.APIView):
    def get(self, request):
        ObjectMedia = objectMedia(
            photos=MediaPhotos.objects.all(),
            videos=MediaVideos.objects.all(),
            urlphotos=MediaFiles.objects.first().urlPhotos,
            urlvideos=MediaFiles.objects.first().urlVideos,
        )
        serializerMedia = MediaFullSerializer(ObjectMedia)
        mediaData = serializerMedia.data
        from image_cropping.utils import get_backend
        for media in mediaData.get("photos"):
            ID = media.get("id")
            obj = MediaPhotos.objects.get(id = ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (280, 140),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            media['image'] = image
        return Response(mediaData)
