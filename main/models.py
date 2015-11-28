from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm

class Profile(models.Model):
  user = models.OneToOneField(User,null=True)
  display_name = models.CharField(blank=True,max_length=50)
  description = models.TextField(blank=True,null=True)
  subscriptions = models.ManyToManyField("Fiction",related_name="subscribers",blank=True)

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

  # TODO: Make it so that it doesn't print a comma and space after the last author
  def __str__(self):
      return self.title + " by " + ([str(author) + ", " for author in self.starters.all()][0])

class Episode(models.Model):
  fiction = models.ForeignKey(Fiction)
  parent = models.ForeignKey("self", null=True, blank=True)
  after = models.BooleanField(default=True)
  duplicate = models.ForeignKey("self", related_name="duplicates", null=True, blank=True)
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Profile)
  content = models.TextField(default="This episode is empty")
  stars = models.ManyToManyField(Profile,related_name="likers", null=True, blank=True)
  created_date = models.DateTimeField(default=datetime.datetime.now)
  summary = models.TextField()

  def __str__(self):
      return self.title + " by " + str(self.author)

class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = ['title', 'content']

class Comment(models.Model):
  commenter = models.ForeignKey(Profile)
  chapter = models.ForeignKey(Episode)
  body = models.TextField()
  created_date = models.DateTimeField(default=datetime.datetime.now)

  def __str__(self):
      return self.body + " by " + self.commenter