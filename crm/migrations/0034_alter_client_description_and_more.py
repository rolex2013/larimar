# Generated by Django 5.0.2 on 2024-02-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0033_alter_clienttask_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='clientevent',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
