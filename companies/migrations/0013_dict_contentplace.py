# Generated by Django 3.0.5 on 2020-05-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0012_content_is_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dict_ContentPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('name_lang', models.CharField(blank=True, max_length=64, null=True, verbose_name='Перевод')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Место отображения контента',
                'verbose_name_plural': 'Места отображения контента',
                'ordering': ('sort',),
            },
        ),
    ]
