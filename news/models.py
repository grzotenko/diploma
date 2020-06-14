from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe       #for imagePreView
from image_cropping import ImageRatioField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from .validators import validate_file_extension, validate_image
import architect
from directions.models import Direction
# Create your models here.
@architect.install('partition', type='range', subtype='date',
                   constraint='month', column='date')
class News(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.app_label,instance.id, filename)
    title = models.TextField(max_length=400, verbose_name="Заголовок Новости", blank=False, default='')
    preview = models.TextField(max_length=500, verbose_name="Превью Новости", blank=True, default='')
    date = models.DateTimeField(default=timezone.now, blank=False, verbose_name="Дата и Время")
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='', verbose_name="Картинка к новости", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '300x300', help_text="Выберите область для отображения картинки в маленьком варианте", verbose_name="Маленькая картинка")
    imageBig = ImageRatioField('imageOld', '900x315', help_text="Выберите область для отображения картинки в большом варианте", verbose_name="Большая картинка")
    main = models.BooleanField(default=False, verbose_name="Главная новость")
    important = models.BooleanField(default=False, verbose_name="Важная новость")
    text = RichTextUploadingField(blank=True, default="", verbose_name="Текст")
    directions = models.ManyToManyField(Direction, verbose_name="Выберите Направления", blank=True)
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
            super(News, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(News, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.app_label,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(News, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-date"]
        indexes = (
            models.Index(fields=['preview']),
            models.Index(fields=['title']),
            models.Index(fields=['text']),
        )
