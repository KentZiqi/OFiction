from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
  user = models.OneToOneField(User,null=True)
  display_name = models.CharField(blank=True,max_length=50)
  description = models.TextField(blank=True,null=True)
  subscriptions = models.ManyToManyField("Fiction",related_name="subscribers")

  def __str__(self):
      return self.display_name

class Section(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
      return self.name

class Fiction(models.Model):
  section = models.ForeignKey(Section, related_name='fictions')

  title = models.CharField(max_length=200)
  starters = models.ManyToManyField(Profile)
  created_date = models.DateTimeField(default=datetime.datetime.now)
  root = models.ForeignKey("main.Episode", related_name="start", null=True)

  # TODO: Make it so that it doesn't print a comma and space after the last author
  def __str__(self):
      return self.title + " by " + ([str(author) + ", " for author in self.starters.all()][0])

class Episode(models.Model):
  fiction = models.ForeignKey(Fiction)

  parent = models.ForeignKey("self", null=True)
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Profile)
  stars = models.ManyToManyField(Profile,related_name="likers")
  created_date = models.DateTimeField(default=datetime.datetime.now)
  summary = models.TextField()

  def __str__(self):
      return self.title + " by " + str(self.author)

class EpisodeVersion(models.Model):
  episode = models.ForeignKey(Episode)

  content = models.TextField()
  created_date = models.DateTimeField(default=datetime.datetime.now)

  # TODO: Add query to recover version
  def __str__(self):
      return "Episode " + str(self.episode) + " version X"

class Comment(models.Model):
  commenter = models.ForeignKey(Profile)
  chapter = models.ForeignKey(Episode)
  body = models.TextField()
  created_date = models.DateTimeField(default=datetime.datetime.now)

  def __str__(self):
      return self.body + " by " + self.commenter