# Generated by Django 3.1.5 on 2021-04-16 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_clientfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientfile',
            old_name='project',
            new_name='client',
        ),
        migrations.AddField(
            model_name='clientfile',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clientevent_file', to='crm.clientevent', verbose_name='Событие'),
        ),
        migrations.AddField(
            model_name='clientfile',
            name='eventcomment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clienteventcomment_file', to='crm.clienteventcomment', verbose_name='Комментарий события'),
        ),
    ]