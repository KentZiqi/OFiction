# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20151215_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='sentiment',
            field=models.IntegerField(default=0),
        ),
    ]
