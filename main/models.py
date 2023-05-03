from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from disciplinary_practice import settings
from pytils.translit import slugify
from uuid import uuid4

from mptt.models import MPTTModel, TreeForeignKey


class CustomUser(AbstractUser):
    LS = 1
    KO = 2
    KG = 3
    KOF = 4
    ST = 5
    NK = 6

    ROLE_CHOICES = (
        (LS, 'Курсант'),
        (KO, 'Командир отделения'),
        (KG, 'Командир группы'),
        (KOF, 'Курсовой офицер'),
        (ST, 'Старшина курса'),
        (NK, 'Начальник курса')
    )
    RANG_CHOICES = (
        ('ряд.', 'Рядовой'),
        ('мл.с-т', 'Мл.Сержант'),
        ('с-т', 'Сержант'),
        ('ст.с-т', 'Ст.Сержант'),
        ('пр-к', 'Прапорщик'),
        ('ст.пр-к', 'Ст.Прапорщик'),
        ('л-т', 'Лейтенант'),
        ('ст.л-т', 'Ст.Лейтенант'),
        ('к-н', 'Капитан'),
        ('м-р', 'Майор'),
        ('п/п-к', 'Подполковник'),
        ('п-к', 'Полковник')
    )
    PLATOON_CHOICES = (
        (1, '1 взвод'),
        (2, '2 взвод')
    )
    GROUP_CHOICES = (
        (311, '311 группа'),
        (312, '312 группа'),
        (313, '313 группа'),
        (314, '314 группа')
    )
    UNIT_CHOICES = (
        (1, '1 отделение'),
        (2, '2 отделение'),
        (3, '3 отделение')
    )

    role = models.PositiveSmallIntegerField('Должность', choices=ROLE_CHOICES, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    surname = models.CharField('Отчество', max_length=50, blank=True, null=True)
    rang = models.CharField('Воинское звание', choices=RANG_CHOICES, max_length=50, blank=True, null=True)
    platoon = models.PositiveSmallIntegerField('Взвод', choices=PLATOON_CHOICES, blank=True, null=True)
    group = models.IntegerField('Номер группы', choices=GROUP_CHOICES, blank=True, null=True)
    unit = models.PositiveSmallIntegerField('Отделение', choices=UNIT_CHOICES, blank=True, null=True)

    def get_FIO(self):
        if self.last_name:
            return str(self.rang) + ' ' + str(self.last_name) + ' ' + str(self.first_name[0].upper()) + '.' + str(
                self.surname[0].upper()) + '.'
        else:
            return "'unknown'"


class Note(models.Model):
    TYPENOTE_CHOICES = (
        ('Поощрение', 'Поощрение'),
        ('Взыскание', 'Взыскание'),
        ('Снятие ранее применённого взыскания', 'Снятие ранее применённого взыскания'),
    )
    cadet = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_for_cadet',
                              verbose_name='Кому')
    type = models.CharField('Вид записи', choices=TYPENOTE_CHOICES, max_length=40)
    who_gave = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_who_gave',
                                 verbose_name='Кем дано')
    text = models.TextField('Текст записи')
    date = models.DateField('Дата')
    check_active = models.BooleanField('Активно', default=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def __str__(self):
        return self.cadet.last_name + ' ' + self.cadet.first_name[0] + '.' + self.cadet.surname[
            0] + '.' + ' | ' + self.type

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def save(self, **kwargs):
        super(Note, self).save()
        if not self.slug:
            self.slug = slugify(self.type) + '-' + slugify(self.text) + '-' + uuid4().hex[:8]
            super(Note, self).save()


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название позразделения')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title
