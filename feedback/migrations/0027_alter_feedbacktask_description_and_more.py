# Generated by Django 5.0.2 on 2024-02-15 07:37

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0026_alter_dict_feedbacktaskstatus_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbacktask',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='feedbacktaskcomment',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='feedbackticketcomment',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание'),
        ),
    ]