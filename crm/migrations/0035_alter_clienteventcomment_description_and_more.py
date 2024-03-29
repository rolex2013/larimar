# Generated by Django 5.0.2 on 2024-02-15 07:37

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0034_alter_client_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienteventcomment',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='clienttask',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='clienttaskcomment',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание'),
        ),
    ]
