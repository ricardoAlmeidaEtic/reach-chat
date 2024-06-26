# Generated by Django 5.0.4 on 2024-05-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatting", "0002_message_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="likes",
            field=models.IntegerField(default=0, help_text="Number of Likes"),
        ),
        migrations.AlterField(
            model_name="message",
            name="image",
            field=models.FileField(blank=True, help_text="Sent Image", upload_to=""),
        ),
    ]
