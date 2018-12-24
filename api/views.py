from rest_framework import viewsets

from .serializers import GroupSerializer, UserSerializer
from rest_framework import permissions
from rest_framework.authtoken.models import Token

def login(request):
    Token.generate_key()
    print(token.key)

