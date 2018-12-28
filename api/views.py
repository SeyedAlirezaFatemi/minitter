from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import FailedTokenAttempt
from twitter import information_gathering
from twitter.models import Tweet


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        if has_reached_max_attempt(information_gathering.get_client_ip(request)):
            return Response({
                'error': 'Request Blocked',
            })
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            print(user.email)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            })
        else:
            add_failed_attempt(information_gathering.get_client_ip(request))
            serializer.is_valid(raise_exception=True)


def add_failed_attempt(ip):
    attempt = FailedTokenAttempt.objects.filter(ip_address=ip)
    if attempt:
        attempt = FailedTokenAttempt.objects.get(ip_address=ip)
        attempt.num_of_requests += 1
        print(attempt.num_of_requests)
        attempt.save()
    else:
        failed = FailedTokenAttempt(ip_address=ip)
        failed.save()


def has_reached_max_attempt(ip):
    attempt = FailedTokenAttempt.objects.filter(ip_address=ip)
    if attempt:
        attempt = FailedTokenAttempt.objects.get(ip_address=ip)
        if attempt.num_of_requests >= 5:
            return True
    return False


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
