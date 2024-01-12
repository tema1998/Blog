# Generated by Django 4.1.2 on 2023-10-24 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_postlikes_post_id_remove_postlikes_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlikes',
            name='username',
        ),
        migrations.AddField(
            model_name='commentlikes',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.post'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
