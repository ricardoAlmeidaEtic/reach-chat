# Generated by Django 5.0.4 on 2024-04-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatting", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="image",
            field=models.CharField(blank=True, help_text="Sent Image", max_length=100),
        ),
    ]