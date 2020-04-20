from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from adminsortable2.admin import SortableInlineAdminMixin

from .models import News
# Register your models here.

class NewsAdmin(ImageCroppingMixin,admin.ModelAdmin):
    model = News
    list_display = ['title', 'date', 'main', 'important']
    readonly_fields = ()
    filter_horizontal = ('directions',)
    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'preview', 'date',),
        }),
        ("Изображения", {
            'fields': ('imageOld', ('image', 'imageBig')),
        }),
        ("Текст", {
            'fields': ( 'text',),
        }),
        ("Дополнительная информация", {
            'fields': (('main', 'important'),'directions', ),
        }),
    )
    def save_model(self, request, obj, form, change):
        if obj.main:
            obj.important = False
        obj.save()

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.app_label, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors = True)
            obj.delete()
admin.site.register(News, NewsAdmin)