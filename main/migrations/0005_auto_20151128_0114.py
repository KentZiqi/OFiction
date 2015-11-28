# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_fiction_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='duplicate',
            field=models.ForeignKey(related_name='duplicates', to='main.Episode', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='parent',
            field=models.ForeignKey(to='main.Episode', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='stars',
            field=models.ManyToManyField(related_name='likers', to='main.Profile', null=True, blank=True),
        ),
    ]
