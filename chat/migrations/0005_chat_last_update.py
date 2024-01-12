# Generated by Django 4.1.2 on 2023-12-18 10:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
