# Generated by Django 4.1.7 on 2023-05-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_rename_dict_listfieldtype_dict_ylistfieldtype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ylist',
            name='dateclose',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
    ]