from django.db import models
from django.utils import timezone
from image_cropping import ImageRatioField
from .validators import validate_file_extension, validate_image
from django.utils.safestring import mark_safe       #for imagePreView
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import architect
from directions.models import Direction
# Create your models here.
class Event(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    title = models.TextField(max_length=500, verbose_name="Заголовок События", blank=False, default='')
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='', verbose_name="Картинка к событию",
                              upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '390x280', help_text="Выберите область для отображения картинки", verbose_name="Выберите область")
    imageBig = ImageRatioField('imageOld', '900x315', help_text="Выберите область для отображения картинки в большом варианте", verbose_name="Большая картинка")
    address = models.CharField(default='', verbose_name="Место проведения", blank=True, max_length=300)
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на яндекс-карту")
    dateStart = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="Дата начала")
    dateEnd = models.DateField(blank=True,verbose_name="Дата окончания/проведения(ОСТАВЬТЕ ПУСТЫМ, ЕСЛИ У СОБЫТИЯ НЕТ ПЕРИОДА ПРОВЕДЕНИЯ)",null=True)
    date = models.CharField(max_length=100, verbose_name="Строковое представление даты", default="", blank=False)
    directions = models.ManyToManyField(Direction, verbose_name="Тэги",blank=True)
    main = models.BooleanField(default=False, verbose_name="Отображение на главной странице")
    text = RichTextUploadingField(blank=True, default="", verbose_name="Текст")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ['dateStart', 'dateEnd']
        indexes = (
            models.Index(fields=['title']),
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
            super(Event, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(Event, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.model_name,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(Event, self).delete(*args, **kwargs)