# Generated by Django 3.1.5 on 2021-05-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0007_auto_20210505_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docver',
            name='is_actual',
            field=models.BooleanField(default=False, verbose_name='Актуальность'),
        ),
    ]
