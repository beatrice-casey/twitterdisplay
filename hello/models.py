from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Tweet(models.Model):
    num = models.IntegerField()
    html = models.TextField()
    
    def __str__(self):
        return "Tweet"

