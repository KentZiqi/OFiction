# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_episode_popularity'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='episode',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
