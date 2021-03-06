# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 08:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(blank=True, upload_to=b'')),
                ('bio', models.TextField(blank=True, max_length=150)),
                ('posts_num', models.PositiveIntegerField(default=0)),
                ('followers_num', models.PositiveIntegerField(default=0)),
                ('following_num', models.PositiveIntegerField(default=0)),
                ('following', models.ManyToManyField(blank=True, related_name='followed_by', to='InstagramApp.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'')),
                ('caption', models.TextField()),
                ('likes', models.PositiveIntegerField(default=0)),
                ('comments_num', models.PositiveIntegerField(default=0)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('comments', models.ManyToManyField(blank=True, to='InstagramApp.Comment')),
                ('like_users', models.ManyToManyField(to='InstagramApp.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by_user', to='InstagramApp.Account')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='on_picture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstagramApp.Picture'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstagramApp.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='picture_library',
            field=models.ManyToManyField(blank=True, to='InstagramApp.Picture'),
        ),
    ]
