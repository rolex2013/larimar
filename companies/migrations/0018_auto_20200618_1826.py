# Generated by Django 3.0.6 on 2020-06-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0017_dict_positiontype_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]