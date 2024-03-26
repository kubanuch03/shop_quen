# Generated by Django 5.0.2 on 2024-03-26 15:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app_product", "0002_product_is_favorite"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Deliver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("types", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.PositiveIntegerField()),
                ("lastname", models.CharField(max_length=255)),
                ("firstname", models.CharField(max_length=255)),
                ("payment_type", models.CharField(max_length=255)),
                (
                    "deliver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_account.deliver",
                    ),
                ),
                ("products", models.ManyToManyField(to="app_product.product")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
