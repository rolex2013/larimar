# Generated by Django 3.1.5 on 2021-07-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0053_auto_20210708_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfile',
            name='psize',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
    ]
