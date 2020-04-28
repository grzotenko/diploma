from django.contrib import admin
from image_cropping import ImageCroppingMixin
from tabbed_admin import TabbedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin

from .models import *
# Register your models here.
class StageInline(SortableInlineAdminMixin,admin.TabularInline):
    model = Stage
    extra = 0
    fields = [("groups", "next"), ("yellowcards", "matches"), "type",]
    
class RulesAdmin(admin.ModelAdmin):
    model = Rules
    fields = ["title",]
    inlines = [StageInline]
admin.site.register(Rules, RulesAdmin)

class GameAdmin(admin.ModelAdmin):
    model = Game
admin.site.register(Game, GameAdmin)