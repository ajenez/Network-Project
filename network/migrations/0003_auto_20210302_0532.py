# Generated by Django 3.1.6 on 2021-03-02 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_followers_likes_posts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]
