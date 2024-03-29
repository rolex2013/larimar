# Generated by Django 3.1.5 on 2022-01-13 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0034_company_is_support'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('description', models.CharField(max_length=512, verbose_name='Описание')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('dateclose', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats_chat_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats_company', to='companies.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Чат Компании',
                'verbose_name_plural': 'Чаты компаний',
            },
        ),
        migrations.CreateModel(
            name='Dict_ChatType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('name_lang', models.CharField(blank=True, max_length=64, null=True, verbose_name='Перевод')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Тип чата',
                'verbose_name_plural': 'Типы чатов',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2048, verbose_name='Наименование')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats_message_autor', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('chat', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='chats_chat', to='chats.chat', verbose_name='Чат')),
            ],
            options={
                'verbose_name': 'Сообщение пользователя',
                'verbose_name_plural': 'Сообщения пользователей',
            },
        ),
        migrations.CreateModel(
            name='ChatMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('dateclose', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats_chatmember_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('chat', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='chats_chatmember_chat', to='chats.chat', verbose_name='Чат')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_chatmember_member', to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Участник Чата',
                'verbose_name_plural': 'Участники чатов',
            },
        ),
        migrations.AddField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(related_name='chat_members', through='chats.ChatMember', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='chat',
            name='type',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='chats_chattype', to='chats.dict_chattype', verbose_name='Тип'),
        ),
    ]
