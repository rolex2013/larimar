# Generated by Django 3.1.5 on 2021-05-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0012_docver_vernumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='docver',
            name='is_act',
            field=models.BooleanField(default=True, verbose_name='Акт'),
        ),
    ]