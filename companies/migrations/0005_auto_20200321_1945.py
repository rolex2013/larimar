# Generated by Django 3.0.4 on 2020-03-21 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
        ('companies', '0004_auto_20200318_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCompanyComponentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_company', to='companies.Company', verbose_name='Организация')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_component', to='main.Component', verbose_name='Компонент')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_group', to='auth.Group', verbose_name='Группа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь и Группа Организации и Компонента',
                'verbose_name_plural': 'Пользователи и Группы Организаций и Компонентов',
                'ordering': ('user', 'company', 'component', 'group'),
                'unique_together': {('user', 'company', 'component', 'group')},
            },
        ),
        migrations.DeleteModel(
            name='UserCompany',
        ),
    ]
