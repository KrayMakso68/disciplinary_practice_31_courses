# Generated by Django 4.2 on 2023-04-15 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='surname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество'),
        ),
    ]
