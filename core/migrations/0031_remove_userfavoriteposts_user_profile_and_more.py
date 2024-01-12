# Generated by Django 4.1.2 on 2023-12-16 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0030_remove_userfavoriteposts_posts_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfavoriteposts',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='userfavoriteposts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
