# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20151215_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episodeversion',
            name='episode',
        ),
        migrations.DeleteModel(
            name='EpisodeVersion',
        ),
    ]
