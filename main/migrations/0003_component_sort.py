# Generated by Django 3.0.4 on 2020-03-21 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200321_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='sort',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
