# Generated by Django 4.2.11 on 2024-03-31 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_product", "0004_product_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="location",
        ),
    ]