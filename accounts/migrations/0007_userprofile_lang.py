# Generated by Django 4.1.7 on 2023-03-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210707_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lang',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Язык'),
        ),
    ]