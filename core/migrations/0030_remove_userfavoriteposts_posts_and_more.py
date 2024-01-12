# Generated by Django 4.1.2 on 2023-12-16 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_userfavoriteposts_delete_userfavouriteposts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfavoriteposts',
            name='posts',
        ),
        migrations.AlterField(
            model_name='userfavoriteposts',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile'),
        ),
        migrations.AddField(
            model_name='userfavoriteposts',
            name='posts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post'),
            preserve_default=False,
        ),
    ]
