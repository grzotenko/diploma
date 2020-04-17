from django.contrib import admin
from django.urls import path
from api.views import api_root
from django.conf.urls import include, url, re_path

from django.conf.urls.static import static  #media+static
from django.conf import settings            #media+static
from .views import *
urlpatterns = [
    path('admin/main/main/', main_main),
    path('admin/main/partner/', main_partner),
    path('admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # url(r'^', include('main.urls')),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)