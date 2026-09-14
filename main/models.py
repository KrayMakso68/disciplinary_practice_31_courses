from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils import timezone
from disciplinary_practice import settings
from pytils.translit import slugify
from uuid import uuid4

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    COURSE_TYPE = "course"
    PLATOON_TYPE = "platoon"
    GROUP_TYPE = "group"
    UNIT_TYPE = "unit"

    type_choices = [
        (COURSE_TYPE, "Филиал / Департамент"),
        (PLATOON_TYPE, "Управление"),
        (GROUP_TYPE, "Отдел"),
        (UNIT_TYPE, "Группа / Команда"),
    ]

    title = models.CharField(max_length=50, unique=True, verbose_name='Название подразделения')
    type = models.CharField(choices=type_choices, max_length=25, default=COURSE_TYPE, verbose_name="Тип подразделения")
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Вышестоящее подразделение')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    EMPLOYEE = 1
    TEAM_LEAD = 2
    UNIT_HEAD = 3
    DIVISION_HEAD = 4
    OPS_MANAGER = 5
    DIRECTOR = 6

    # Legacy aliases
    LS = EMPLOYEE
    KO = TEAM_LEAD
    KG = UNIT_HEAD
    KOF = DIVISION_HEAD
    ST = OPS_MANAGER
    NK = DIRECTOR

    ROLE_CHOICES = (
        (EMPLOYEE, 'Сотрудник'),
        (TEAM_LEAD, 'Тимлид группы'),
        (UNIT_HEAD, 'Руководитель направления'),
        (DIVISION_HEAD, 'Куратор подразделения'),
        (OPS_MANAGER, 'Операционный менеджер'),
        (DIRECTOR, 'Руководитель департамента')
    )
    RANG_CHOICES = (
        ('Junior', 'Junior'),
        ('Junior+', 'Junior+'),
        ('Middle', 'Middle'),
        ('Middle+', 'Middle+'),
        ('Senior', 'Senior'),
        ('Lead', 'Team Lead'),
        ('Principal', 'Principal Expert'),
        ('Manager', 'Manager'),
        ('Head', 'Head of Department'),
        ('Director', 'Director'),
        ('VP', 'Vice President'),
        ('Executive', 'Executive')
    )

    role = models.PositiveSmallIntegerField('Роль / Должность', choices=ROLE_CHOICES, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    surname = models.CharField('Отчество', max_length=50, blank=True, null=True)
    rang = models.CharField('Корпоративный грейд', choices=RANG_CHOICES, max_length=50, blank=True, null=True)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='staff', verbose_name='Подразделение',
                              blank=True, null=True)
    slug = models.SlugField(max_length=255, help_text='Заполняется автоматически!', db_index=True, blank=True)

    def save(self, **kwargs):
        super(CustomUser, self).save()
        if not self.slug:
            self.slug = slugify(self.last_name) + '-' + slugify(self.first_name[0]) + slugify(self.surname[0]) + '-' + uuid4().hex[:8]
            super(CustomUser, self).save()

    def get_FIO(self):
        if self.last_name:
            first = f"{self.first_name[0].upper()}." if self.first_name else ""
            sur = f"{self.surname[0].upper()}." if self.surname else ""
            return f"{self.last_name} {first}{sur}".strip()
        return self.username or "Сотрудник"


class Note(models.Model):
    TYPE_ACHIEVEMENT = 'Достижение'
    TYPE_WARNING = 'Замечание'
    TYPE_RESOLVED = 'Устранение замечания'

    TYPENOTE_CHOICES = (
        (TYPE_ACHIEVEMENT, 'Достижение / Благодарность'),
        (TYPE_WARNING, 'Замечание / Инцидент'),
        (TYPE_RESOLVED, 'Устранение замечания / Закрыто'),
    )
    cadet = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes',
                              verbose_name='Сотрудник')
    type = models.CharField('Вид записи', choices=TYPENOTE_CHOICES, max_length=50)
    who_gave = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='written_notes',
                                 verbose_name='Кем назначено')
    text = models.TextField('Текст записи')
    date = models.DateTimeField('Дата', default=timezone.now)
    check_active = models.BooleanField('Активно', default=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def __str__(self):
        first = f"{self.cadet.first_name[0]}." if self.cadet.first_name else ""
        sur = f"{self.cadet.surname[0]}." if self.cadet.surname else ""
        return f"{self.cadet.last_name} {first}{sur} | {self.type}"

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def save(self, **kwargs):
        super(Note, self).save()
        if not self.slug:
            self.slug = slugify(self.type) + '-' + slugify(self.text[:20]) + '-' + uuid4().hex[:8]
            super(Note, self).save()
