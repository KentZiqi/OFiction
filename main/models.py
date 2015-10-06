from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Section(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,null=True)
    display_name = models.CharField(blank=True,max_length=50)
    description = models.TextField(blank=True,null=True)
    stars = models.ManyToManyField(Episode,related_name="likers")
    subscription = models.ManyToManyField(Fiction,related_name="subscribers")
    def __str__(self):
        return self.display_name

class EpisodeVersion(models.Model):
    chapter = models.ForeignKey(Episode)
    fiction = models.ForeignKey(Fiction)
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)

class Episode(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Profile)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey(EpisodeVersion)
    summary = models.TextField()

class Comment(models.Model):
    commenter = models.ForeignKey(Profile)
    chapter = models.ForeignKey(Episode)
    body = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)

class Fiction(models.Model):
    title = models.CharField(max_length=200)
    section = models.ForeignKey(Section, related_name='fictions')
    starters = models.ManyToManyField(Profile)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    root = models.ForeignKey(Episode)
    def __str__(self):
        return self.title


