# Generated by Django 3.1.5 on 2021-07-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20210716_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackticket',
            name='id_local',
            field=models.PositiveIntegerField(default=1, verbose_name='Локальный ID'),
            preserve_default=False,
        ),
    ]