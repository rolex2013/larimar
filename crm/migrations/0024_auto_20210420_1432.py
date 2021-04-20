# Generated by Django 3.1.5 on 2021-04-20 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0023_auto_20210416_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientevent',
            name='type',
            field=models.ForeignKey(default=1, limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='event_type', to='crm.dict_clienteventtype', verbose_name='Тип события'),
            preserve_default=False,
        ),
    ]
