# Generated by Django 3.0.5 on 2020-04-28 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_auto_20200401_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Процент выполнения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Процент выполнения'),
            preserve_default=False,
        ),
    ]