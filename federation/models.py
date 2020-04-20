from django.db import models
from .validators import validate_file_extension, validate_image, validate_documents
from ckeditor_uploader.fields import RichTextUploadingField
from image_cropping import ImageRatioField
# Create your models here.

class Federation(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="Название", blank=False, default='')
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
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='',
                                 verbose_name="Картинка к элементу структуры", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '320x300',
                            help_text="Выберите область для отображения картинки", verbose_name="")

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
    def save(self, *args, **kwargs):
        if self.id:
            import os, glob
            path = './media/{0}/{1}/*.*'.format(self._meta.app_label,self.id)
            pathOld = '.{0}*.*'.format(self.imageOld.url)
            filesOld = glob.glob(pathOld)
            filesOld.append("." + self.imageOld.url)
            for file in glob.glob(path):
                if file not in filesOld:
                    os.remove(file)
        else:
            saved_image = self.imageOld
            self.imageOld = None
            super(FederationElement, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(FederationElement, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.app_label,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(FederationElement, self).delete(*args, **kwargs)

class FederationStaff(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    id_fk = models.ForeignKey(FederationElement, on_delete=models.CASCADE, verbose_name="Структура")
    name = models.CharField(blank=False, default="", max_length=150, verbose_name="Имя")
    position = models.CharField(blank=True, default="", max_length=201, verbose_name="Должность")
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='',
                                 verbose_name="Фото", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '320x300',
                            help_text="Выберите область для отображения картинки", verbose_name="")
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
    def save(self, *args, **kwargs):
        if self.id:
            import os, glob
            path = './media/{0}/{1}/*.*'.format(self._meta.model_name,self.id)
            pathOld = '.{0}*.*'.format(self.imageOld.url)
            filesOld = glob.glob(pathOld)
            filesOld.append("." + self.imageOld.url)
            for file in glob.glob(path):
                if file not in filesOld:
                    os.remove(file)
        else:
            saved_image = self.imageOld
            self.imageOld = None
            super(FederationStaff, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(FederationStaff, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.model_name,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(FederationStaff, self).delete(*args, **kwargs)

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