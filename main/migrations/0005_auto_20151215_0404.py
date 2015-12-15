# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151130_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='content',
            field=ckeditor.fields.RichTextField(default='This episode is empty'),
        ),
    ]
