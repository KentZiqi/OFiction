# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151215_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='summary',
            field=models.CharField(null=True, blank=True, max_length=1000),
        ),
    ]
