# Generated by Django 3.1.5 on 2021-07-16 10:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_feedbackticket_id_local'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackticket',
            name='dateclose',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AddField(
            model_name='feedbackticket',
            name='datecreate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создана'),
            preserve_default=False,
        ),
    ]
