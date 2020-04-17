from django.db import models
from .validators import *
from django.utils.safestring import mark_safe       #for imagePreView
from ckeditor.fields import RichTextField
# Create your models here.
class Trend(models.Model):
    title = models.CharField(max_length=300, unique=True, verbose_name="Название направления", blank=False, default='')
    text = RichTextField(verbose_name="Текст", blank=False, default='')
    imageInactive = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка неактивная",
                              upload_to='trends/')
    imageActive = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка при наведении",
                              upload_to='trends/')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.title

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.imageInactive))
    imagePreView.short_description = 'Предпросмотр картинки'

    class Meta(object):
        verbose_name="Направление"
        verbose_name_plural="Направления"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['text']),
        )

class Direction(models.Model):
    id_fk = models.ForeignKey(Trend, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300, unique=True, verbose_name="Название тэга", blank=False, default='')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name="Тэг"
        verbose_name_plural="Тэги"
        ordering = ['customOrder']
