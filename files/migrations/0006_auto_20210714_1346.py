# Generated by Django 3.1.5 on 2021-07-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_folderfile_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folderfile',
            name='size',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
    ]
