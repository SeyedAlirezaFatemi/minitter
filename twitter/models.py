from django.contrib.auth.models import User
from django.db import models
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends import google
from urllib3 import PoolManager, exceptions
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default='avatar.png')


def new_users_handler(sender, user, response, details, **kwargs):
    user.is_new = True
    if user.is_new:
        if "id" in response:

            try:
                url = None
                if sender == FacebookOAuth2:
                    url = "http://graph.facebook.com/%s/picture?type=large" \
                          % response["id"]
                elif sender == google.GoogleOAuth2 and "picture" in response:
                    url = response["picture"]

                if url:
                    avatar = PoolManager().request('GET', url)
                    profile = Profile(user=user)

                    profile.avatar.save(slugify(user.username + " social") + '.jpg',
                                        ContentFile(avatar.read()))

                    profile.save()

            except exceptions.HTTPError:
                pass

    return False


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_title = models.CharField(max_length=50)
    tweet_text = models.CharField(max_length=280)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.author}: {self.tweet_title}"


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Request(models.Model):
    ip_address = models.GenericIPAddressField()
    last_request_time = models.TimeField()
    num_of_requests = models.IntegerField(default=1)
    black_list = models.BooleanField(default=False)

    def __str__(self):
        return self.ip


class UnAuthorizedRequests(models.Model):
    ip_address = models.GenericIPAddressField()
    num_of_requests = models.IntegerField(default=1)
    black_list = models.BooleanField(default=False)
    user = models.OneToOneField(User, related_name='requested_user', on_delete=models.CASCADE)
