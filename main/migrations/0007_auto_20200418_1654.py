# Generated by Django 3.0.5 on 2020-04-18 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_dict_protocoltype_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dict_protocoltype',
            options={'ordering': ('sort',), 'verbose_name': 'Протокол оповещения', 'verbose_name_plural': 'Протоколы оповещений'},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Оповещение', 'verbose_name_plural': 'Оповещения'},
        ),
        migrations.AddField(
            model_name='notification',
            name='response',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Ответ'),
        ),
    ]
