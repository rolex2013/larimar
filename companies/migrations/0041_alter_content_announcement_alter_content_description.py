# Generated by Django 5.0.2 on 2024-02-12 09:27

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0040_alter_content_datebegin_alter_content_dateend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='announcement',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=10240, null=True, verbose_name='Анонс'),
        ),
        migrations.AlterField(
            model_name='content',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Текст'),
        ),
    ]