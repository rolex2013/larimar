# Generated by Django 3.0.4 on 2020-04-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_content_dict_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='datebegin',
            field=models.DateTimeField(verbose_name='Начало'),
        ),
        migrations.AlterField(
            model_name='content',
            name='dateend',
            field=models.DateTimeField(verbose_name='Окончание'),
        ),
    ]
