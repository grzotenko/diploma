from django.shortcuts import render
from django.shortcuts import redirect
from main.models import Main
from federation.models import Federation
from mediafiles.models import MediaFiles
# Create your views here.
def main_main(request):
    return redirect("/admin/main/main/"+str(Main.objects.first().id)+"/change/")
def main_partner(request):
    return redirect("/admin/main/main/"+str(Main.objects.first().id)+"/change/#tabs-5")
def mediafiles_mediafiles(request):
    return redirect("/admin/mediafiles/mediafiles/"+str(MediaFiles.objects.first().id)+"/change/")
def mediafiles_mediaphotos(request):
    return redirect("/admin/mediafiles/mediafiles/"+str(MediaFiles.objects.first().id)+"/change/#tabs-2")
def federation_federation(request):
    return redirect("/admin/federation/federation/"+str(Federation.objects.first().id)+"/change/")
def federation_federationelement(request):
    return redirect("/admin/federation/federation/"+str(Federation.objects.first().id)+"/change/#tabs-3")