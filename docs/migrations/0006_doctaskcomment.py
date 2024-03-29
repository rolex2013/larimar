# Generated by Django 3.1.5 on 2021-05-04 14:53

# import ckeditor_uploader.fields
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docs', '0005_auto_20210504_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name="DocTaskComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="Наименование")),
                (
                    "description",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="Описание"),
                ),
                (
                    "time",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=6,
                        verbose_name="Время работы, час.",
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=9,
                        verbose_name="Стоимость",
                    ),
                ),
                (
                    "datecreate",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создан"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активность"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resultdoctask",
                        to="docs.doctask",
                        verbose_name="Задача",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
    ]
