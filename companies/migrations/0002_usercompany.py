# Generated by Django 3.0.4 on 2020-03-14 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_company', to='companies.Company', verbose_name='Организация')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь Организации',
                'verbose_name_plural': 'Пользователи Организаций',
            },
        ),
    ]