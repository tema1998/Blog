# Generated by Django 4.1.2 on 2023-12-14 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_profile_following_userfavouriteposts'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavoritePosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts', models.ManyToManyField(related_name='user_favorite_posts', to='core.post', verbose_name='User favorite posts')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_posts', to='core.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='UserFavouritePosts',
        ),
    ]