# Generated by Django 5.0.2 on 2024-03-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
