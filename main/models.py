from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
  user = models.OneToOneField(User, null=True)
  display_name = models.CharField(blank=True, max_length=50)
  description = models.TextField(blank=True, null=True)
  subscriptions = models.ManyToManyField("Fiction",related_name="subscribers", blank=True)
  picture = models.OneToOneField("ProfilePhoto", null=True)

  def __str__(self):
      return self.display_name

class Genre(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
      return self.name

class ProfilePhoto(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        if file_size > 4096*4096:
            raise ValidationError("Max file size is 4MB")
    image = models.ImageField(upload_to='photo/', height_field = 'height',
                              width_field = 'width', validators=[validate_image],
                              default='default_profile.png')
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbs/',blank=True,null=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    # Adapted from http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
    def create_thumbnail(self):

        if not self.image:
            return

        from io import BytesIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (500,500)

        from mimetypes import MimeTypes
        mime = MimeTypes()
        mime_type = mime.guess_type(self.image.url)

        DJANGO_TYPE = mime_type
        if DJANGO_TYPE[0] == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE[0] == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        else:
            return

        self.image.open()
        r = BytesIO(self.image.read())
        fullsize_image = Image.open(r)
        image = fullsize_image.copy()

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
        self.thumbnail.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self, **kwargs):
        self.create_thumbnail()
        force_update = False
        if self.id:
            force_update = True
        super(ProfilePhoto, self).save(force_update=force_update)

    def __str__(self):
        return self.image.url

class Fiction(models.Model):
  genre = models.ForeignKey(Genre, related_name='fictions')

  title = models.CharField(max_length=200)
  starters = models.ManyToManyField(Profile)
  created_date = models.DateTimeField(default=datetime.datetime.now)
  root = models.ForeignKey("main.Episode", related_name="start", null=True)

  # TODO: Make it so that it doesn't print a comma and space after the last author
  def __str__(self):
      return self.title + " by " + ([str(author) + ", " for author in self.starters.all()][0])

class Episode(models.Model):
  fiction = models.ForeignKey(Fiction)

  parent = models.ForeignKey("self", related_name="children", null=True, blank=True)
  after = models.BooleanField(default=True)
  duplicate = models.ForeignKey("self", related_name="duplicates", null=True, blank=True)
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Profile)
  content = models.TextField(default="This episode is empty")
  stars = models.ManyToManyField(Profile,related_name="favorites")
  created_date = models.DateTimeField(default=datetime.datetime.now)
  summary = models.TextField(blank=True, null=True)
  popularity = models.IntegerField(default=0)

  def getID(self):
      episodes = self.fiction.episode_set.all()
      return list(episodes).index(self) + 1

  def star(self, profile):
      self.stars.add(profile)
      self.popularity = len(self.stars.all())

  def unstar(self, profile):
      self.stars.remove(profile)
      self.popularity = len(self.stars.all())

  def __str__(self):
      return "#" + str(self.getID())+": " + self.fiction.title+"/" + self.title

class EpisodeVersion(models.Model):
  episode = models.ForeignKey(Episode)

  content = models.TextField()
  created_date = models.DateTimeField(default=datetime.datetime.now)

  # TODO: Add query to recover version
  def __str__(self):
      return "Episode " + str(self.episode) + " version X"

class Comment(models.Model):
  commenter = models.ForeignKey(Profile)
  episode = models.ForeignKey(Episode)
  body = models.TextField()
  created_date = models.DateTimeField(default=datetime.datetime.now)

  def __str__(self):
      return self.body + " by " + self.commenter