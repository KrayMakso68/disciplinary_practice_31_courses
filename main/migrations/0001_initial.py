# Generated by Django 4.2 on 2023-04-14 06:31

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Курсант'), (2, 'Командир отделения'), (3, 'Командир группы'), (4, 'Курсовой офицер'), (5, 'Старшина курса'), (6, 'Начальник курса')], null=True, verbose_name='Должность')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('rang', models.CharField(blank=True, choices=[('ряд.', 'Рядовой'), ('мл.с-т', 'Мл.Сержант'), ('с-т', 'Сержант'), ('ст.с-т', 'Ст.Сержант'), ('пр-к', 'Прапорщик'), ('ст.пр-к', 'Ст.Прапорщик'), ('л-т', 'Лейтенант'), ('ст.л-т', 'Ст.Лейтенант'), ('к-н', 'Капитан'), ('м-р', 'Майор'), ('п/п-к', 'Подполковник'), ('п-к', 'Полковник')], max_length=50, null=True, verbose_name='Воинское звание')),
                ('platoon', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1 взвод'), (2, '2 взвод')], null=True, verbose_name='Взвод')),
                ('group', models.IntegerField(blank=True, choices=[(311, '311 группа'), (312, '312 группа'), (313, '313 группа'), (314, '314 группа')], null=True, verbose_name='Номер группы')),
                ('unit', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1 отделение'), (2, '2 отделение'), (3, '3 отделение')], null=True, verbose_name='Отделение')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]