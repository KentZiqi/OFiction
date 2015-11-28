# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151128_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscriptions',
            field=models.ManyToManyField(to='main.Fiction', blank=True, related_name='subscribers'),
        ),
    ]
