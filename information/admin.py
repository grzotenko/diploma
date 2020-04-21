from django.contrib import admin
from image_cropping import ImageCroppingMixin
from tabbed_admin import TabbedModelAdmin

from .models import *
# Register your models here.
class TeamAdmin(ImageCroppingMixin,admin.ModelAdmin):
    model = Team
    list_display = ['title', 'date',]
    fields = ['title', 'date','imageOld', 'image',]

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.model_name, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors = True)
            obj.delete()
admin.site.register(Team, TeamAdmin)

class PlayersHistoryInline(admin.StackedInline):
    model = PlayersHistory
    readonly_fields = []
    extra = 0
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': (("team", "number"), ("start", "end"), ("goals", "assists", "yellowcards", "redcards"))
        }),
    )
class PlayerAdmin(TabbedModelAdmin):
    model = Player
    list_display = ['fullname', 'position']
    readonly_fields = ['imagePreView', ]
    tab_overview = (
        (None, {
            'fields': ('surname', 'name', 'patronymic', "birthday", "position",("image","imagePreView",),),
        }),
    )
    tab_history = (
        PlayersHistoryInline,
    )

    tabs = [
        ('Основная информация об игроке', tab_overview),
        ('Статистика', tab_history),
    ]
    def save_model(self, request, obj, form, change):
        obj.fullname = obj.surname + " " + obj.name
        obj.save()
admin.site.register(Player, PlayerAdmin)