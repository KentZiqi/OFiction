# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('body', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('episode', models.ForeignKey(to='main.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='Fiction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('display_name', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(height_field='height', upload_to='photo/', validators=[main.models.ProfilePhoto.validate_image], width_field='width', default='default_profile.png')),
                ('width', models.PositiveIntegerField(blank=True, null=True)),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbs/')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.OneToOneField(null=True, to='main.ProfilePhoto'),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to='main.Fiction'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fiction',
            name='genre',
            field=models.ForeignKey(related_name='fictions', to='main.Genre'),
        ),
        migrations.AddField(
            model_name='fiction',
            name='root',
            field=models.ForeignKey(related_name='start', null=True, to='main.Episode'),
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
            field=models.ForeignKey(blank=True, null=True, to='main.Episode', related_name='duplicates'),
        ),
        migrations.AddField(
            model_name='episode',
            name='fiction',
            field=models.ForeignKey(to='main.Fiction'),
        ),
        migrations.AddField(
            model_name='episode',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, to='main.Episode', related_name='children'),
        ),
        migrations.AddField(
            model_name='episode',
            name='stars',
            field=models.ManyToManyField(related_name='likers', to='main.Profile'),
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
