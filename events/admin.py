from django.contrib import admin
from django.utils.safestring import mark_safe
from datetime import timedelta
from base.settings import DATE_FORMAT, MONTH_FORMAT
from .dateformation import month_from_ru_to_eng
from image_cropping import ImageCroppingMixin
from django.utils import dateformat
from .models import *
# Register your models here.

def reverse_date(modeladmin, request, queryset):
    for flagman in queryset:
        if flagman.dateStart is None:
            flagman.dateStart = flagman.dateEnd
            flagman.save()
reverse_date.short_description = "Реверсировать одиночные даты"
class EventAdmin(ImageCroppingMixin,admin.ModelAdmin):
    model = Event
    list_display = ['title', 'date', 'main']
    readonly_fields = ('date',)
    filter_horizontal = ('directions',)
    actions = [reverse_date]
    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'main'),
        }),
        ("Изображения", {
            'fields': ('imageOld', ('image', 'imageBig'),),
        }),
        ("Дополнительная информация", {
            'fields': (('address', 'map'), ('dateStart','dateEnd') ,'date','directions',),
        }),
        ("Текст", {
            'fields': ('text',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.dateEnd is None:
            if obj.dateStart is None:
                obj.date = ""
            else:
                obj.dateEnd = obj.dateStart
                obj.date = dateformat.format(obj.dateEnd, DATE_FORMAT)
        else:
            if obj.dateStart is None:
                obj.date = ""
            else:
                if obj.dateEnd < obj.dateStart:
                    obj.dateStart = obj.dateEnd
                if obj.dateEnd > obj.dateStart:
                    prev = obj.dateStart - timedelta(days=1)
                    next = obj.dateEnd + timedelta(days=1)
                    if prev.month is not obj.dateStart.month and next.month is not obj.dateEnd.month:
                        if obj.dateStart.month == obj.dateEnd.month and obj.dateStart.year == obj.dateEnd.year:
                            obj.date = month_from_ru_to_eng(dateformat.format(obj.dateEnd, MONTH_FORMAT)) + " " + obj.dateEnd.strftime("%Y")
                        else:
                            obj.date = obj.dateStart.strftime("%d.%m.%Y") + " - " + obj.dateEnd.strftime("%d.%m.%Y")
                    else:
                        obj.date = obj.dateStart.strftime("%d.%m.%Y") + " - " + obj.dateEnd.strftime("%d.%m.%Y")

        if obj.address is not None and obj.address != "":
            if obj.map is not None and obj.map != "":
                obj.save()
        else:
            obj.save()
    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.model_name, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors = True)
            obj.delete()
admin.site.register(Event, EventAdmin)