from django.db import models
from django.utils import timezone
from .validators import *
from image_cropping import ImageRatioField
from django.core.validators import MinValueValidator

from information.models import Team, Player
# Create your models here.
class Rules(models.Model):
    title = models.CharField(blank=False,  default="", max_length=201, verbose_name="Название")

    def __str__(self):
        return str(self.title)

    class Meta(object):
        verbose_name = "Правила"
        verbose_name_plural = "Правила"




class Tournament(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    title = models.CharField(max_length=300, verbose_name="Название", blank=False, default='')
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='',
                                 verbose_name="Лого", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '300x300',
                            help_text="Выберите область для отображения лого", verbose_name="")
    start = models.DateField(default=timezone.now, blank=False, verbose_name="Начало турнира")
    end = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="Окончание турнира")
    address = models.CharField(default='', verbose_name="Место проведения", blank=True, max_length=300)
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на яндекс-карту")
    champion = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Чемпион")
    rules = models.ForeignKey(Rules, on_delete=models.CASCADE, verbose_name="Правила")
    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name="Турнир"
        verbose_name_plural="Турниры"
        ordering = ["title", "-start"]
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
            super(Tournament, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(Tournament, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.model_name,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(Tournament, self).delete(*args, **kwargs)

class AwardsType(models.Model):
    title = models.CharField(blank=False,  default="", max_length=301, verbose_name="Название награды")

    def __str__(self):
        return str(self.title)

    class Meta(object):
        verbose_name = "Тип Индивидуальной награды"
        verbose_name_plural = "Типы Индивидуальных наград"



class Organizer(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.model_name,instance.id, filename)
    id_fk = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='organizers')
    url = models.CharField(blank=False,  default="", max_length=101, verbose_name="Ссылка")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")
    imageOld = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка",
                                 upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '50x50', help_text="Выберите область для отображения картинки", verbose_name="Отображение картинки")

    def __str__(self):
        return str(self.url)

    class Meta(object):
        verbose_name = "Организатор"
        verbose_name_plural = "Организаторы"
        ordering = ['customOrder']
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
        return super(Organizer, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.model_name,self.id)
        if os.path.exists(path):
            shutil.rmtree(path)
        return super(Organizer, self).delete(*args, **kwargs)


class Stage(models.Model):
    typeGroupStage = "G"
    typeCupStage = "C"
    TypeStage = (
        (typeGroupStage, "Чемпионат"),
        (typeCupStage, "Кубок")
    )
    id_fk = models.ForeignKey(Rules, on_delete=models.CASCADE, related_name='stages')
    groups = models.PositiveIntegerField(validators=[MinValueValidator(1),],default=1, blank=False, null=False, verbose_name="Количество групп")
    next = models.PositiveIntegerField(validators=[MinValueValidator(1),],default=1, blank=False, null=False, verbose_name="Количество команд, выходящих далее")
    yellowcards = models.PositiveIntegerField(validators=[MinValueValidator(0),],default=0, blank=False, null=False, verbose_name="Количество желтых карточек, необходимых для дискалификации")
    matches = models.PositiveIntegerField(validators=[MinValueValidator(0),],default=0, blank=False, null=False, verbose_name="Количество матчей, пропускаемых дисквалифицированным игроком")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")
    type = models.CharField(max_length=25, verbose_name="Тип стадии", blank=False, choices=TypeStage,default="Чемпионат")

    def __str__(self):
        return str(self.customOrder)+")"+str(self.id_fk.__str__())

    class Meta(object):
        verbose_name = "Стадия"
        verbose_name_plural = "Стадии"
        ordering = ['customOrder']

class Competitor(models.Model):
    id_fk = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='competitors')
    points = models.PositiveIntegerField(validators=[MinValueValidator(0),],default=0, blank=False, null=False, verbose_name="Количество очков")
    place = models.PositiveIntegerField(validators=[MinValueValidator(1),],default=1, blank=False, null=False, verbose_name="Место в турнире")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")

    def __str__(self):
        return str(self.team.title)+"-"+str(self.id_fk.__str__())+"("+str(self.id_fk.end.year)+"г.)"

    class Meta(object):
        verbose_name = "Участник соревнований"
        verbose_name_plural = "Участники соревнований"

class StatsPlayer(models.Model):
    id_fk = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='statsplayers')
    matches = models.PositiveIntegerField(validators=[MinValueValidator(0),],default=0, blank=False, null=False, verbose_name="Игры")
    goals = models.PositiveIntegerField(validators=[MinValueValidator(0),], default=0, blank=False, null=False,
                                         verbose_name="Голы")
    assists = models.PositiveIntegerField(validators=[MinValueValidator(0),], default=0, blank=False, null=False,
                                        verbose_name="Голевые передачи")
    yellowcards = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Желтые карточки")
    redcards = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Красные карточки")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Игрок")

    def __str__(self):
        return str(self.player.fullname)+")"+str(self.id_fk.__str__())

    class Meta(object):
        verbose_name = "Статистика Игрока"
        verbose_name_plural = "Статистики игроков"

class Award(models.Model):
    id_fk = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='awards')
    type = models.ForeignKey(AwardsType, on_delete=models.CASCADE, verbose_name='Тип награды')
    count = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Количество действий")
    player = models.ForeignKey(StatsPlayer, on_delete=models.CASCADE, verbose_name="Игрок")

    def __str__(self):
        return str(self.type.title) + " " + str(self.id_fk.title)

    class Meta(object):
        verbose_name = "Индивидуальная награда"
        verbose_name_plural = "Индивидуальные награды"

class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Турнир')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='Стадия')
    number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1),], blank=False, null=False,verbose_name="Номер тура")

    def __str__(self):
        return str(self.number)+" тур. "+str(self.tournament.__str__())

    class Meta(object):
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

class Game(models.Model):
    resultHome = "1"
    resultDraw = "="
    resultAway = "2"
    resultPenaltyHome = "+"
    resultPenaltyAway = "-"
    TypeResult = (
        (resultHome, "Победа хозяев"),
        (resultDraw, "Ничья"),
        (resultAway, "Победа гостей"),
        (resultPenaltyHome, "Победа хозяев(пен)"),
        (resultPenaltyAway, "Победа гостей(пен)")
    )
    round = models.ForeignKey(Round, on_delete=models.CASCADE, verbose_name='Тур')
    home = models.ForeignKey(Competitor, on_delete=models.CASCADE, verbose_name='Домашняя команда', related_name='homegames')
    away = models.ForeignKey(Competitor, on_delete=models.CASCADE, verbose_name='Гостевая команда', related_name='awaygames')
    homeGoals = models.PositiveIntegerField(validators=[MinValueValidator(0),],default=0, blank=False, null=False, verbose_name="Забито домашней командой")
    awayGoals = models.PositiveIntegerField(validators=[MinValueValidator(0),], default=0, blank=False, null=False,
                                         verbose_name="Забито гостевой командой")
    homePenalty = models.PositiveIntegerField(validators=[MinValueValidator(0),], default=0, blank=False, null=False,
                                            verbose_name="Забито домашней командой(пен)")
    awayPenalty = models.PositiveIntegerField(validators=[MinValueValidator(0),], default=0, blank=False, null=False,
                                            verbose_name="Забито гостевой командой(пен)")
    result = models.CharField(max_length=25, verbose_name="Результат", blank=False, choices=TypeResult)


    def __str__(self):
        return str(self.round.__str__())+" - "+str(self.home.team.title)+" : "+str(self.away.team.title)

    class Meta(object):
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

class Protocol(models.Model):
    id_fk = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='protocols')
    player = models.ForeignKey(StatsPlayer, on_delete=models.CASCADE, verbose_name='Игрок')

    def __str__(self):
        return str(self.player.player.fullname)+". "+str(self.id_fk.__str__())

    class Meta(object):
        verbose_name = "Протокол"
        verbose_name_plural = "Протоколы"


class Card(models.Model):
    yellowCard = "Y"
    redCard = "R"
    TypeCard = (
        (yellowCard, "Желтая карточка"),
        (redCard, "Красная карточка")
    )
    type = models.CharField(max_length=25, verbose_name="Тип карточки", blank=False, choices=TypeCard,default="Желтая карточка")
    id_fk = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='cards')
    minute = models.PositiveIntegerField(validators=[MinValueValidator(1),],default=1, blank=False, null=False, verbose_name="Минута")


    class Meta(object):
        verbose_name = "Действие"
        verbose_name_plural = "Действия"


class Goal(models.Model):
    id_fk = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='goals')
    minute = models.PositiveIntegerField(validators=[MinValueValidator(1),], default=1, blank=False, null=False,
                                         verbose_name="Минута")
    assist = models.ForeignKey(StatsPlayer, on_delete=models.CASCADE, verbose_name='Ассистент', blank=True, null=True)

    class Meta(object):
        verbose_name = "Действие"
        verbose_name_plural = "Действия"