# Generated by Django 3.0.6 on 2020-06-18 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20200530_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currencyrate',
            options={'ordering': ('-date', 'currency'), 'verbose_name': 'История курса валют', 'verbose_name_plural': 'Истории курсов валют'},
        ),
    ]
