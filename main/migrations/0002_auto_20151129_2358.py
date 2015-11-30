# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='episode',
            name='stars',
            field=models.ManyToManyField(to='main.Profile', related_name='favorites'),
        ),
    ]
