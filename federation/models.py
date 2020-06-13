from django.db import models
from .validators import validate_file_extension, validate_image, validate_documents
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from image_cropping import ImageRatioField
# Create your models here.

class Federation(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="Название", blank=False, default='')
    work_time = RichTextField(default='', blank=False, verbose_name="Режим работы")
    text = RichTextField(default='', blank=False, verbose_name="Информация")
    email = models.CharField(default='', blank=False, verbose_name="Электронная почта", max_length=100)
    phone = models.CharField(default='', blank=False, verbose_name="Телефон", max_length=20)
    address = models.CharField(blank=True, default="", max_length=301, verbose_name="Адрес")
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на Яндекс-карту")

    def __str__(self):
        return "ИЗМЕНИТЬ СТРАНИЦУ ФЕДЕРАЦИИ"

    class Meta(object):
        verbose_name="Федерация"
        verbose_name_plural="Федерация"

class FederationElement(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.app_label,instance.id, filename)
    id_fk = models.ForeignKey(Federation, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique=True, verbose_name="Название структуры", blank=False, default='')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name="Структуру Федерация"
        verbose_name_plural="Структуры Федерации"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['title']),
        )

class FederationStaff(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    id_fk = models.ForeignKey(FederationElement, on_delete=models.CASCADE, verbose_name="Структура")
    name = models.CharField(blank=False, default="", max_length=150, verbose_name="Имя")
    position = models.CharField(blank=True, default="", max_length=201, verbose_name="Должность")
    image = models.ImageField(validators=[validate_image], blank=False, default='',
                                 verbose_name="Фото", upload_to=user_directory_path)
    text = RichTextUploadingField(blank=True, default="", verbose_name="Текст")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['name']),
            models.Index(fields=['position']),
            models.Index(fields=['text']),
        )

class FederationDocuments(models.Model):
    id_fk = models.ForeignKey(Federation, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=300, verbose_name="Заголовок")
    file = models.FileField(validators=[validate_documents], blank=True, default='', verbose_name="Файл",
                              upload_to='documents/')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return str(self.title)

    class Meta(object):
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['customOrder']