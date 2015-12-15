# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20151215_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fiction',
            name='starters',
        ),
        migrations.AddField(
            model_name='fiction',
            name='starter',
            field=models.ForeignKey(default=1, to='main.Profile'),
            preserve_default=False,
        ),
    ]
