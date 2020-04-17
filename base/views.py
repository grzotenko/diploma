from django.shortcuts import render
from django.shortcuts import redirect
from main.models import Main

# Create your views here.
def main_main(request):
    return redirect("/admin/main/main/"+str(Main.objects.first().id)+"/change/")
def main_partner(request):
    return redirect("/admin/main/main/"+str(Main.objects.first().id)+"/change/#tabs-5")
