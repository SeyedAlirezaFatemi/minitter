from django.shortcuts import render

from .models import Tweet


def twitter(request):
    if request.user.is_authenticated:
        tweets = list(Tweet.objects.all())
    return render(request, 'home.html', {'tweets': tweets})
