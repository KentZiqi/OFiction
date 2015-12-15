# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_episode_sentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='sentiment',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
    ]
