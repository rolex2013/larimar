# Generated by Django 3.0.5 on 2020-04-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0010_auto_20200409_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='is_forprofile',
            field=models.BooleanField(default=False, verbose_name='Только для профиля'),
        ),
        migrations.AddField(
            model_name='content',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Приватно'),
        ),
    ]
