# Generated by Django 3.0.6 on 2020-05-30 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_currencyrate_datecreate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyrate',
            name='date',
            field=models.DateTimeField(verbose_name='Дата'),
        ),
    ]
