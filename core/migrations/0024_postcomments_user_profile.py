# Generated by Django 4.1.2 on 2023-10-29 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_rename_comment_id_commentlikes_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomments',
            name='user_profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='PostComments', to='core.profile'),
            preserve_default=False,
        ),
    ]
