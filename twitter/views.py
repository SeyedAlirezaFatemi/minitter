from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import ImageUploadForm, SignUpForm
from .models import Tweet


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def twitter(request):
    tweets = []
    current_user = request.user
    if current_user.is_authenticated:
        tweets = list(Tweet.objects.all())
    return render(request, 'twitter.html', {'tweets': tweets})


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        current_user = request.user
        if form.is_valid():
            current_user.profile.avatar = form.cleaned_data['avatar']
            current_user.save()
            return HttpResponseRedirect(reverse('twitter'))
    return HttpResponseForbidden('Allowed only via POST.')


@login_required
def new_tweet(request):
    current_user = request.user
    tweet_title = request.POST.get('tweet_title')
    tweet_text = request.POST.get('tweet_text')
    tweet = Tweet(author=current_user, tweet_title=tweet_title, tweet_text=tweet_text, pub_date=timezone.now())
    tweet.save()
    return HttpResponseRedirect(reverse('twitter'))
