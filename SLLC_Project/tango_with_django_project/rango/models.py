from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


'''new model here'''
'''
from django.db import models
from django.db.models.base import Model
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import time

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # slug = models.SlugField(unique=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Question(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=time.time())

    def __str__(self):
        return self.title

class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=time.time())

    def __str__(self):
        return self.content

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    like_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
'''