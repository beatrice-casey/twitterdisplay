from django.db import models
from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Tweet(models.Model):
    username = models.TextField()
    html = models.TextField(help_text="This is the HTML snippet stored for each tweet")
    date = models.TextField(help_text="Day number/ month number/ year. i.e (oct 10 2021 = 1/10/2021)")

    def __str__(self):
        return "Tweet"

