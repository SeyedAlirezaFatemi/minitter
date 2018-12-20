from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render

from .forms import ImageUploadForm
from .models import Tweet, Profile


def twitter(request):
    tweets = []
    current_user = request.user
    if current_user.is_authenticated:
        tweets = list(Tweet.objects.all())
    return render(request, 'home.html', {'tweets': tweets})


def upload_avatar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        current_user = request.user
        if form.is_valid():
            current_user.profile.avatar = form.cleaned_data['avatar']
            current_user.save()
            return HttpResponse('Image upload success.')
    return HttpResponseForbidden('Allowed only via POST.')
