# Generated by Django 3.0.5 on 2020-05-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_auto_20200518_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Стоимость'),
        ),
    ]