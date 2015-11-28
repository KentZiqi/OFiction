# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151128_0114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='chapter',
            new_name='episode',
        ),
    ]
