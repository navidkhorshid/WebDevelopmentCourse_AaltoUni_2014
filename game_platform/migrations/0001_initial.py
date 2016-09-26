# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(related_name='developers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('picture_url', models.URLField(null=True, blank=True)),
                ('game_url', models.URLField()),
                ('price', models.FloatField(default=0)),
                ('description', models.TextField(null=True, blank=True)),
                ('category', models.ForeignKey(to='game_platform.Category', related_name='games')),
                ('developer', models.ForeignKey(to='game_platform.Developer', related_name='games')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(related_name='players', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player_Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('score', models.FloatField(null=True, blank=True, default=0)),
                ('playerItems', models.TextField(null=True, blank=True)),
                ('purchaseTime', models.DateTimeField(auto_now_add=True)),
                ('purchasePrice', models.FloatField(default=0)),
                ('game', models.ForeignKey(to='game_platform.Game', related_name='player_games')),
                ('player', models.ForeignKey(to='game_platform.Player', related_name='player_games')),
            ],
            options={
                'ordering': ['purchaseTime'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('activation_key', models.CharField(blank=True, max_length=40)),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2015, 2, 4, 19, 14, 14, 393439))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
            bases=(models.Model,),
        ),
    ]
