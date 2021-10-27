from django.db import models
from django.db.models.fields import DateField

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Tweet(models.Model):
    html = models.TextField()
    date = models.DateField()
    username = models.TextField()

    def __str__(self):
        return "Tweet"

class User(models.Model):
    username = models.TextField()
    need_hashtag = models.BooleanField()
