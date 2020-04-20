from django.contrib import admin
from tabbed_admin import TabbedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.urls import reverse
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin, ImageCropWidget

from .models import FederationElement, Federation, FederationDocuments, FederationStaff

# Register your models here.
class FederationStaffInline(SortableInlineAdminMixin,admin.StackedInline):
    model = FederationStaff
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("name","position","imageOld","image","text","customOrder")
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        crop_fields = getattr(self.model, 'crop_fields', {})
        if db_field.name in crop_fields:
            kwargs['widget'] = ImageCropWidget

        return super(FederationStaffInline, self).formfield_for_dbfield(db_field, **kwargs)

    def get_model_perms(self, request):
        return {}

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.model_name, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path)
            obj.delete()
@admin.register(FederationElement)
class FederationElementAdmin(ImageCroppingMixin, admin.ModelAdmin):
    readonly_fields = ["return_back",]
    fields = ["imageOld", "image", "return_back"]
    inlines = [FederationStaffInline]

    def return_back(self, obj):
        if obj.pk:
            url = '/admin/federation/federation/1/change/#tabs-3'
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Вернуться к редактированию Федерации')
            ))
        return ""
    return_back.short_description = ""
    def get_model_perms(self, request):
        return {}

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}/{2}'.format(obj._meta.app_label, obj._meta.model_name, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path)
            obj.delete()

class FederationElementInline(SortableInlineAdminMixin,admin.StackedInline):
    model = FederationElement
    extra = 1
    readonly_fields = ["get_edit_link",]
    fields = ["title","get_edit_link","customOrder"]
    def get_edit_link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Кликните по Этой ссылке для редактирования картинки')
            ))
        return mark_safe('<b style="color: #900;"> Создайте элемент и отредактируйте его после!!</b>')
    get_edit_link.short_description = "Редактировать структуру"

class FederationDocumentsInline(SortableInlineAdminMixin,admin.StackedInline):
    model = FederationDocuments
    readonly_fields = []
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "file", "customOrder")
        }),
    )
class FederationAdmin(TabbedModelAdmin):
    model = Federation
    list_display = ['title',]
    tab_overview = (
        (None, {
            'fields': ('title',),
        }),
    )
    tab_documents = (
        FederationDocumentsInline,
    )
    tab_elements = (
        FederationElementInline,
    )
    tabs = [
        ('Основная информация о федерации', tab_overview),
        ('Документы', tab_documents),
        ('Структура', tab_elements),
    ]
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
admin.site.register(Federation, FederationAdmin)