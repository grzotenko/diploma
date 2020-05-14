from main.models import Menu

def getHeaderViews(context):
    context["menu"] = Menu.objects.all()