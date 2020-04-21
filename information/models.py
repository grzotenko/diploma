from django.db import models
from .validators import *
from django.utils import timezone
from image_cropping import ImageRatioField
from django.utils.safestring import mark_safe       #for imagePreView
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Player(models.Model):
    positionGoalkeeper = "G"
    positionDefender = "D"
    positionMidfielder = "M"
    positionForward = "F"
    positionDefault = "U"
    PlayerPositions = (
        (positionGoalkeeper, "Вратарь"),
        (positionDefender, "Защитник"),
        (positionMidfielder, "Полузащитник"),
        (positionForward, "Нападающий"),
        (positionDefault, "Универсал")
    )
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    name = models.CharField(blank=False, default="", max_length=100, verbose_name="Имя")
    surname = models.CharField(blank=False, default="", max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(blank=False, default="", max_length=100, verbose_name="Отчество")
    fullname = models.CharField(blank=False, default="", max_length=200, verbose_name="Полное имя")
    image = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Фото", upload_to=user_directory_path)
    position = models.CharField(max_length=25, verbose_name="Амплуа", blank=False, choices=PlayerPositions,default="Универсал")
    birthday = models.DateField(default=timezone.now, blank=False, verbose_name="День рождения")

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="100" />' % (self.image))
    imagePreView.short_description = 'Предпросмотр картинки'

    def __str__(self):
        return str(self.fullname)

    class Meta(object):
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        indexes = (
            models.Index(fields=['fullname']),
        )

class Team(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    title = models.CharField(max_length=300, verbose_name="Название", blank=False, default='')
    date = models.DateField(default=timezone.now, blank=False, verbose_name="Дата основания")
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='',
                                 verbose_name="Лого", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '300x300',
                            help_text="Выберите область для отображения лого", verbose_name="")

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name="Команда"
        verbose_name_plural="Команды"
        indexes = (
            models.Index(fields=['title']),
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
            super(Team, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(Team, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.model_name,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(Team, self).delete(*args, **kwargs)

class PlayersHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Игрок")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")
    start = models.DateField(default=timezone.now, blank=False, verbose_name="Пришел в команду")
    end = models.DateField(default=None, blank=True, null=True,verbose_name="Покинул команду")
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],default=1, blank=False, null=False,verbose_name="Игровой номер")
    goals = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Голы")
    assists = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Голевые передачи")
    yellowcards = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Желтые карточки")
    redcards = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Красные карточки")
    def __str__(self):
        return str(self.player.fullname) + " - " + str(self.team.title)

    class Meta(object):
        verbose_name = "История Игрока"
        verbose_name_plural = "Истории Игроков"
        ordering = ["-start",]