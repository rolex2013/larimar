# Generated by Django 3.0.4 on 2020-04-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_auto_20200330_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Стоимость'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Стоимость'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskcomment',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Стоимость'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskcomment',
            name='time',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Время работы, час.'),
            preserve_default=False,
        ),
    ]