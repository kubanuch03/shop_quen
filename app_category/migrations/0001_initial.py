# Generated by Django 5.0.2 on 2024-02-24 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("image", models.ImageField(upload_to="app_category/Category_images/")),
            ],
            options={
                "indexes": [
                    models.Index(fields=["title"], name="app_categor_title_566db1_idx"),
                    models.Index(fields=["id"], name="app_categor_id_a4d880_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="SubCategory",
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
                ("title", models.CharField(max_length=255)),
                (
                    "image",
                    models.ImageField(upload_to="app_category/SubCategory_images"),
                ),
                ("creted_at", models.DateField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_category.category",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["title"], name="app_categor_title_2072ca_idx"),
                    models.Index(fields=["id"], name="app_categor_id_dedc4b_idx"),
                ],
            },
        ),
    ]
