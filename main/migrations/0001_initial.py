# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('body', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('after', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(default='This episode is empty')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EpisodeVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('episode', models.ForeignKey(to='main.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='Fiction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('root', models.ForeignKey(to='main.Episode', null=True, related_name='start')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('display_name', models.CharField(max_length=50, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('image', models.ImageField(validators=[main.models.ProfilePhoto.validate_image], upload_to='photo/', height_field='height', width_field='width', default='default_profile.png')),
                ('width', models.PositiveIntegerField(null=True, blank=True)),
                ('height', models.PositiveIntegerField(null=True, blank=True)),
                ('thumbnail', models.ImageField(upload_to='thumbs/', null=True, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.OneToOneField(to='main.ProfilePhoto', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscriptions',
            field=models.ManyToManyField(to='main.Fiction', related_name='subscribers', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='fiction',
            name='section',
            field=models.ForeignKey(to='main.Section', related_name='fictions'),
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
            name='duplicate',
            field=models.ForeignKey(to='main.Episode', blank=True, null=True, related_name='duplicates'),
        ),
        migrations.AddField(
            model_name='episode',
            name='fiction',
            field=models.ForeignKey(to='main.Fiction'),
        ),
        migrations.AddField(
            model_name='episode',
            name='parent',
            field=models.ForeignKey(to='main.Episode', blank=True, null=True, related_name='children'),
        ),
        migrations.AddField(
            model_name='episode',
            name='stars',
            field=models.ManyToManyField(to='main.Profile', related_name='likers', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(to='main.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='episode',
            field=models.ForeignKey(to='main.Episode'),
        ),
    ]
