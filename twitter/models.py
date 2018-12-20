from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_title = models.CharField(max_length=50)
    tweet_text = models.CharField(max_length=280)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.author}: {self.tweet_title}"
