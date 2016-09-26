# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game_platform', '0006_auto_20150210_1643'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player_game',
            options={'ordering': ['-score']},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 13, 16, 14, 25, 554641)),
            preserve_default=True,
        ),
    ]
