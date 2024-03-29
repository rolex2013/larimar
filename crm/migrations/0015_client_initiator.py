# Generated by Django 3.1.5 on 2021-01-27 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_remove_client_initiator'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='initiator',
            field=models.ForeignKey(default=1, limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='client_initiator_client', to='crm.dict_clientinitiator', verbose_name='Инициатор клиента'),
            preserve_default=False,
        ),
    ]
