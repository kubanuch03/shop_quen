# Generated by Django 4.2.11 on 2024-03-30 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_product", "0002_product_is_favorite"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="images1",
            field=models.ImageField(blank=True, null=True, upload_to="text/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="images2",
            field=models.ImageField(blank=True, null=True, upload_to="text/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="images3",
            field=models.ImageField(blank=True, null=True, upload_to="text/"),
        ),
    ]
