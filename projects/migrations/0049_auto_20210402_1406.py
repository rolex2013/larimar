# Generated by Django 3.1.5 on 2021-04-02 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0048_auto_20210401_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='uname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Уникальное наименование'),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='pfile',
            field=models.FileField(blank=True, null=True, upload_to='uploads/docs/project', verbose_name='Файл'),
        ),
    ]