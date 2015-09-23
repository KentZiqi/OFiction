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
    stars = models.ManyToManyField(Chapter,related_name="likers")
    def __str__(self):
        return self.display_name

class ChapterVersion(models.Model):
    chapter = models.ForeignKey(Chapter)
    fiction = models.ForeignKey(Fiction)
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Profile)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey(ChapterVersion)

class Fiction(models.Model):
    title = models.CharField(max_length=200)
    section = models.ForeignKey(Section, related_name='fictions')
    starters = models.ManyToManyField(Profile)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    root = models.ForeignKey(Chapter)
    def __str__(self):
        return self.title


