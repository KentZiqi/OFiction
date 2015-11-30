# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import main.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('episode', models.ForeignKey(to='main.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='Fiction',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('image', models.ImageField(default='default_profile.png', validators=[main.models.ProfilePhoto.validate_image], upload_to='photo/', width_field='width', height_field='height')),
                ('width', models.PositiveIntegerField(null=True, blank=True)),
                ('height', models.PositiveIntegerField(null=True, blank=True)),
                ('thumbnail', models.ImageField(null=True, blank=True, upload_to='thumbs/')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
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
            field=models.ManyToManyField(related_name='subscribers', blank=True, to='main.Fiction'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
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
            field=models.ForeignKey(related_name='duplicates', blank=True, null=True, to='main.Episode'),
        ),
        migrations.AddField(
            model_name='episode',
            name='fiction',
            field=models.ForeignKey(to='main.Fiction'),
        ),
        migrations.AddField(
            model_name='episode',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, null=True, to='main.Episode'),
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
