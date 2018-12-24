from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twitter.models import Tweet


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def update_auth_token(request):
    Token.objects.get(user=request.user).delete()
    token = Token.objects.create(user=request.user)
    return Response({
        'token': token.key,
    })


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def new_tweet(request):
    current_user = request.user
    tweet_title = request.data.get('tweet_title')
    tweet_text = request.data.get('tweet_text')
    tweet = Tweet(author=current_user, tweet_title=tweet_title, tweet_text=tweet_text, pub_date=timezone.now())
    tweet.save()
    return Response(status=status.HTTP_201_CREATED)
