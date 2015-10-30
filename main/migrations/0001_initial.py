# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EpisodeVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('episode', models.ForeignKey(to='main.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='Fiction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('root', models.ForeignKey(related_name='start', to='main.Episode', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=50, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('subscriptions', models.ManyToManyField(related_name='subscribers', to='main.Fiction')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='fiction',
            name='section',
            field=models.ForeignKey(related_name='fictions', to='main.Section'),
        ),
        migrations.AddField(
            model_name='fiction',
            name='starters',
            field=models.ManyToManyField(to='main.Profile'),
        ),
        migrations.AddField(
            model_name='episode',
            name='author',
            field=models.ForeignKey(to='main.Profile'),
        ),
        migrations.AddField(
            model_name='episode',
            name='fiction',
            field=models.ForeignKey(to='main.Fiction'),
        ),
        migrations.AddField(
            model_name='episode',
            name='parent',
            field=models.ForeignKey(to='main.Episode', null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='stars',
            field=models.ManyToManyField(related_name='likers', to='main.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='chapter',
            field=models.ForeignKey(to='main.Episode'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(to='main.Profile'),
        ),
    ]
