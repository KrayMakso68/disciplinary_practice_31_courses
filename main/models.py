from django.contrib.auth.models import AbstractUser
from django.db import models


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
    rang = models.CharField('Воинское звание', choices=RANG_CHOICES, max_length=50, blank=True, null=True)
    platoon = models.PositiveSmallIntegerField('Взвод', choices=PLATOON_CHOICES, blank=True, null=True)
    group = models.IntegerField('Номер группы', choices=GROUP_CHOICES, blank=True, null=True)
    unit = models.PositiveSmallIntegerField('Отделение', choices=UNIT_CHOICES, blank=True, null=True)
