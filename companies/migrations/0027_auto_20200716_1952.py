# Generated by Django 3.0.6 on 2020-07-16 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0026_auto_20200716_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='dateend',
            field=models.DateField(blank=True, null=True, verbose_name='Окончание работы'),
        ),
    ]
