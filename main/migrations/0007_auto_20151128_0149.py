# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20151128_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='parent',
            field=models.ForeignKey(null=True, to='main.Episode', blank=True, related_name='children'),
        ),
    ]
