# Generated by Django 3.0.3 on 2020-02-29 15:11

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20200225_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Описание'),
        ),
    ]
