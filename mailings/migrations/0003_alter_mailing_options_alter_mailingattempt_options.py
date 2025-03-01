# Generated by Django 5.1.6 on 2025-02-15 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailings", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "permissions": [("can_disable_mailing", "Can disble mailing")],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="mailingattempt",
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылок",
            },
        ),
    ]
