import json
import urllib

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from minitter import settings
from twitter import information_gathering
from .forms import ImageUploadForm, SignUpForm
from .models import FailedLogInAttempt, Tweet


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def login_validation(request):
    if request.method == 'GET':
        show_captcha = has_reached_max_attempt(information_gathering.get_client_ip(request))
        return render(request, 'login.html', {'show_captcha': show_captcha})
    if request.method == 'POST':
        show_captcha = has_reached_max_attempt(information_gathering.get_client_ip(request))
        username = request.POST['username']
        password = request.POST['password']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response,
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        user = User.objects.filter(username=username)
        if not user:
            add_failed_attempt(information_gathering.get_client_ip(request))
            return render(request, 'login.html', {'errors': 'invalid username', 'show_captcha': show_captcha})
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                add_failed_attempt(information_gathering.get_client_ip(request))
                email = EmailMessage('WARNING', 'there has been a security problem!', to=[request.user.email])
                email.send()
                return render(request, 'login.html', {'errors': 'invalid password', 'show_captcha': show_captcha})
            else:
                if not result['success'] and show_captcha:
                    return render(request, 'login.html', {'errors': 'invalid captcha', 'show_captcha': show_captcha})
                else:
                    login(request, user)
                    return HttpResponseRedirect('/twitter')


# def login_validation_secondary(request):
#     if request.method == 'GET':
#         if not has_reached_max_attempt(information_gathering.get_client_ip(request)):
#             return render(request, 'login.html', {'show_captcha': False})
#         else:
#             HttpResponse('Request blocked')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = User.objects.filter(username=username)
#         if not user:
#             add_failed_attempt(information_gathering.get_client_ip(request))
#             return render(request, 'login.html', {'errors': 'invalid username', 'show_captcha': False})
#         else:
#             user = authenticate(request, username=username, password=password)
#             if user is None:
#                 add_failed_attempt(information_gathering.get_client_ip(request))
#                 send_mail('WARNING', "there might be a security problem!", '', request.user.email)
#                 return render(request, 'login.html', {'errors': 'invalid password', 'show_captcha': False})
#             else:
#                 login(request, user)
#                 return HttpResponseRedirect('/twitter')


def add_failed_attempt(ip):
    attempt = FailedLogInAttempt.objects.filter(ip_address=ip)
    if attempt:
        attempt = FailedLogInAttempt.objects.get(ip_address=ip)
        attempt.num_of_requests += 1
        print(attempt.num_of_requests)
        attempt.save()
    else:
        failed = FailedLogInAttempt(ip_address=ip)
        failed.save()


def has_reached_max_attempt(ip):
    attempt = FailedLogInAttempt.objects.filter(ip_address=ip)
    if attempt:
        attempt = FailedLogInAttempt.objects.get(ip_address=ip)
        if attempt.num_of_requests >= 5:
            return True
    return False


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
