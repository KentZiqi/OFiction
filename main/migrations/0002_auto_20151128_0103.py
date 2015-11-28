# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episodeversion',
            name='episode',
        ),
        migrations.AddField(
            model_name='episode',
            name='after',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='content',
            field=models.TextField(default='This episode is empty'),
        ),
        migrations.AddField(
            model_name='episode',
            name='duplicate',
            field=models.ForeignKey(to='main.Episode', related_name='duplicates', null=True),
        ),
        migrations.DeleteModel(
            name='EpisodeVersion',
        ),
    ]
