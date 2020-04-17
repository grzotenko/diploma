from django.contrib import admin
from tabbed_admin import TabbedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin

from .models import Direction, Trend
# Register your models here.
class DirectionInline(SortableInlineAdminMixin,admin.StackedInline):
    model = Direction
    readonly_fields = []
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "customOrder")
        }),
    )
class TrendAdmin(SortableAdminMixin, TabbedModelAdmin):
    model = Trend
    list_display = ['title',]
    readonly_fields = ('imagePreView',)
    tab_overview = (
        (None, {
            'fields': ('title', 'text', 'imageActive','imageInactive', 'imagePreView',),
        }),
    )
    tab_direction = (
        DirectionInline,
    )
    tabs = [
        ('Основная информация о направлении', tab_overview),
        ('Тэги', tab_direction),
    ]
admin.site.register(Trend, TrendAdmin)